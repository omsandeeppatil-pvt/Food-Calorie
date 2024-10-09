import os
import requests
import base64
from PIL import Image
import io
import json

GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = "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"

def process_image_with_llama_vision(image_path):
    # Open and encode the image
    with Image.open(image_path) as img:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

    # Prepare the request payload
    payload = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image and provide the name of the food item and an estimate of its calories. Format your response as JSON with 'food_name' and 'calories' keys. If you're uncertain about the exact calories, provide a range or an approximate value."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_str}"
                        }
                    }
                ]
            }
        ]
    }

    # Set up the headers
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    image_path = input("Enter the path to your food image file: ")
    
    if not os.path.exists(image_path):
        print("Error: The specified file does not exist.")
        return

    print("Analyzing image...")
    result = process_image_with_llama_vision(image_path)
    
    try:
        # Parse the JSON response
        food_info = json.loads(result)
        print(f"\nFood Item: {food_info['food_name']}")
        print(f"Estimated Calories: {food_info['calories']}")
    except json.JSONDecodeError:
        print("Error: Unable to parse the response. Here's the raw output:")
        print(result)

if __name__ == "__main__":
    main()
