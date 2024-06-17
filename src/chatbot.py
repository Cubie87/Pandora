import requests
import json


def chatgptBot(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer " + api_key
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response['choices'][0]['message']['content']
    else:
        print(f"Request failed with status code {response.status_code}")
        return "I'm sorry, I am unable to access OpenAI's API at the moment. Please try again later."

        