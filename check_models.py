import os
from dotenv import load_dotenv
from google import genai

# Load your existing .env file
load_dotenv()

api_key_val = os.getenv("GOOGLE_API_KEY")

if not api_key_val:
    print("Error: GOOGLE_API_KEY not found.")
    exit()

print("Authenticating with Google API...\n")
client = genai.Client(api_key=api_key_val)

print("Available Models:\n")
print("-" * 50)

try:
    # Fetch the list of models
    models = client.models.list()
    count = 0
    
    for m in models:
        # Just print the raw names, no filtering!
        print(f"Exact MODEL_ID : {m.name}")
        print(f"Display Name   : {m.display_name}")
        print("-" * 50)
        count += 1
            
    print(f"\nTotal models available to your key: {count}")
    
except Exception as e:
    print(f"Failed to retrieve models. Error: {e}")