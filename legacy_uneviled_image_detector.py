import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import wikipedia

# Streamlit App Title
st.title("LEGACY UNEVILED")

# Camera input
img_data = st.camera_input("Take a picture")

# Question input
question = "What was the paint name or art name or temple name or monument name in that image otherwise give prompt 'found nothing' ? in one word"

if img_data:
    # Convert the image to a base64 string
    img = Image.open(img_data)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Create the data URI
    img_url = f"data:image/jpeg;base64,{img_base64}"

    # Display the captured image
    st.image(img, caption="Captured Image", use_column_width=True)

    # Button to send the request
    if st.button("Ask"):
        url = "https://chatgpt-42.p.rapidapi.com/matagvision"
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                    "img_url": img_url
                }
            ]
        }
        headers = {
            "x-rapidapi-key": "c6ba32bcb3msh593e6a01310ba00p1a9df7jsn70cea4e4e115",
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()  # Already a dict, no need for json.loads()
            st.write("Summary:")

            # Extract the 'result' value from the response
            result_value = result['result']

            # Display summary from Wikipedia based on the result value
            try:
                summary = wikipedia.summary(result_value)
                st.write(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                st.write("NOT FOUND")
                st.write(e.options)
            except wikipedia.exceptions.PageError:
                st.write("NOT FOUND")
        else:
            st.write("Failed to get a response from the API.")
            st.write(f"Status Code: {response.status_code}")
