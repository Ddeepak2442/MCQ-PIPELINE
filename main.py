import streamlit as st
import base64
import requests
import json
import pandas as pd
from io import BytesIO

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(uploaded_file):
    # Check if an image is uploaded
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        return base64.b64encode(image_bytes).decode('utf-8')

# Function to get structured data from OpenAI
def get_openai_response(image_bytes, prompt, api_key):
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 600
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()['choices'][0]['message']['content']

    # Convert JSON string to dictionary
    data = json.loads(response_data)
    return data

# Streamlit App
def main():
    st.title("OpenAI Image-to-Text App")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        prompt = st.text_area("Enter your prompt:", '''
        Create a structured dictionary based on a multiple-choice question screenshot, including the question, options (a-d), the correct option, an explanation for the question, and reference links related to the question. Please provide the necessary details from the screenshot for each of these elements. 

        Example Format:
        {
          "Question": "[Question Text]",
          "Options": {
            "a": "[Option A]",
            "b": "[Option B]",
            "c": "[Option C]",
            "d": "[Option D]"
          },
          "Correct Option": "[Correct Option]",
          "Explanation": "[Explanation Text]",
          "Reference Links": [
            "[Reference Link 1]",
            "[Reference Link 2]",
            "[Reference Link 3]"
          ]
        }
        ''')

        if st.button("Generate"):
            image_bytes = uploaded_file.read()
            data = get_openai_response(image_bytes, prompt, api_key)

            # Process and display the results
            st.subheader("Generated Data:")
            st.json(data)

if __name__ == "__main__":
    main()
