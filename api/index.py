import os
import pypdf
import io
import json
import re
import time
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'templates'))

app = Flask(__name__, template_folder=TEMPLATE_DIR)

def extract_text_from_pdf(pdf_bytes):
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

api_key_val = os.getenv("GOOGLE_API_KEY")
if not api_key_val:
    print("CRITICAL: GOOGLE_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key_val)
# MODEL_ID = "gemini-2.5-flash"
MODEL_ID = "gemini-flash-latest"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    try:
        files = request.files.getlist('cv')
        if not files or files[0].filename == '':
            return jsonify({"error": "No files uploaded"}), 400
        
        jd = request.form.get('jd', 'Software Engineer')
        blind_mode = request.form.get('blindMode') == 'true'
        
        base_instruction = ""
        if blind_mode:
            base_instruction = "BLIND SCREENING MODE ENABLED: Completely ignore the candidate's name, gender, college name, university, and geographic location. Evaluate strictly based on skills, experience, and projects. "

        results = []

        for file in files:
            pdf_data = file.read()
            cv_text = extract_text_from_pdf(pdf_data)
            
            if not cv_text.strip():
                continue 
            
            agent_prompt = f"{base_instruction}Analyze this Resume against the JD: {jd}\n\nResume: {cv_text}\n\nYou MUST return ONLY a valid JSON object with this exact schema, without any markdown formatting or backticks: {{'match_percentage': <int 0-100>, 'matching_skills': [<list of strings>], 'missing_skills': [<list of strings>], 'analysis': '<detailed markdown string of the full report>'}}"
            
            response = client.models.generate_content(
                model=MODEL_ID, 
                contents=agent_prompt
            )
            
            try:
                # NEW FIX: Robust Regex JSON Extraction
                raw_text = response.text
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                
                if json_match:
                    clean_json_string = json_match.group(0)
                    result_data = json.loads(clean_json_string)
                    result_data['filename'] = file.filename
                    results.append(result_data)
                else:
                    raise ValueError("No JSON object found in response")
                    
            except Exception as parse_err:
                print(f"Failed to parse JSON for {file.filename}. Raw response: {response.text}")
                results.append({
                    'filename': file.filename,
                    'match_percentage': 0,
                    'matching_skills': [],
                    'missing_skills': [],
                    'analysis': "Error: AI response could not be parsed. Please try analyzing this candidate again."
                })
            
            # NEW FIX: Let the free-tier API breathe for 2 seconds before the next resume
            time.sleep(2)

        # Sort the leaderboard
        results.sort(key=lambda x: x.get('match_percentage', 0), reverse=True)
        
        return jsonify({"status": "Success", "data": results})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/generate-questions', methods=['POST'])
def generate_questions():
    try:
        data = request.json
        analysis = data.get('analysis')
        missing_skills = data.get('missing_skills')
        jd = data.get('jd')

        prompt = f"""
        Act as a technical interviewer. Based on the following Job Description and the AI Analysis of a candidate, 
        generate 5-7 sophisticated interview questions. 
        Focus heavily on the 'Missing Skills' to determine if the candidate has transferable knowledge 
        or the ability to learn them quickly.
        
        Job Description: {jd}
        Candidate Analysis: {analysis}
        Missing Skills: {missing_skills}
        
        Return the questions as a clean, bulleted list.
        """
        
        response = client.models.generate_content(
            model=MODEL_ID, 
            contents=prompt
        )
        
        return jsonify({"status": "Success", "questions": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/compare', methods=['POST'])
def compare_candidates():
    try:
        data = request.json
        c1 = data.get('candidate1')
        c2 = data.get('candidate2')
        jd = data.get('jd')

        prompt = f"""
        Act as an expert HR Hiring Manager. Compare these two candidates against the provided Job Description.
        
        Job Description: {jd}
        
        Candidate 1 ({c1['filename']}):
        - Match Score: {c1.get('match_percentage', 0)}%
        - Matching Skills: {', '.join(c1.get('matching_skills', []))}
        - Missing Skills: {', '.join(c1.get('missing_skills', []))}
        
        Candidate 2 ({c2['filename']}):
        - Match Score: {c2.get('match_percentage', 0)}%
        - Matching Skills: {', '.join(c2.get('matching_skills', []))}
        - Missing Skills: {', '.join(c2.get('missing_skills', []))}
        
        Please provide:
        1. A brief summary of how they stack up against each other.
        2. A clean Markdown table comparing their Strengths and Weaknesses side-by-side.
        3. A final, definitive recommendation on who to move forward with first and why.
        """
        
        response = client.models.generate_content(
            model=MODEL_ID, 
            contents=prompt
        )
        
        return jsonify({"status": "Success", "comparison": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)