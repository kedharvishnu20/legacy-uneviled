import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO
import wikipedia

# Streamlit App Title
st.title("LEGACY UNEVILED ")

# Camera input
img_data = st.camera_input("Take a picture")

# Question to be asked
question = "What was the paint name or art name or temple name or monument name in that image? Otherwise, give prompt 'found nothing' in one word."

if img_data:
    # Convert the image to a base64 string
    img = Image.open(img_data)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

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
                    "img_url": f"data:image/jpeg;base64,{img_base64}"
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
            result = response.json()
            st.write("Summary:")

            # Extract the 'result' value from the response
            result_value = result.get('result', '').strip()
            if result_value and "found nothing" not in result_value.lower():
                try:
                    summary = wikipedia.summary(result_value)
                    st.write(summary)
                except wikipedia.exceptions.DisambiguationError as e:
                    st.write("The result matches multiple pages on Wikipedia:")
                    st.write(e.options)
                except wikipedia.exceptions.PageError:
                    st.write("No Wikipedia page found for the identified item.")
            else:
                st.write("This was  not an art or famous place or mounment or temple. thank u for using this")
        else:
            st.write("Failed to get a response from the API.")
            st.write(f"Status Code: {response.status_code}")
