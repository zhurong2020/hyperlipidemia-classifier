import requests

# Define headers
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": "AIzaSyDB735c_EMe1fcXNTXhCWQyaP26cCyOM18"
}

# Define body
body = {
    "generationConfig": {},
    "safetySettings": [],
    "contents": [
        {
            "role": "user",
            "parts": [
                {
                    "text": "Testing. Just say hi and nothing else."
                }
            ]
        }
    ]
}

# Make the request
response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    headers=headers,
    json=body
)
print(response.json())