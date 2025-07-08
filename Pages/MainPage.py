import streamlit as st
from torchvision.io import read_image
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights
from openai import OpenAI
import os
import simpleaudio as sa
import json
import pandas as pd
import cloudinary
import cloudinary.uploader
from PIL import Image
import tempfile

cloudinary.config(
    cloud_name = "danlcwpuc",
    api_key = "721559911819599",
    api_secret = "4_VEcsJ8sUvdf1Olb-2ragubE_0",
    secure = True
)

client = OpenAI(api_key="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")

def get_translated_and_spelled_world(word):
    functions = [
        {
            "name": "spell_word_indonesian",
            "description": "Translate an English word into Indonesian and spell the Indonesian word letter by letter for children.",
            "parameters": {
                "type": "object",
                "properties": {
                    "translated_word": {
                        "type": "string",
                        "description": "The translated word in Bahasa Indonesia"
                    },
                    "spelling": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The spelling of the Indonesian word"
                    },
                    "description": {
                        "type": "string",
                        "description": "Describe the word 1 short sentence that is understandable for children in Bahasa Indonesia"
                    }
                },
                "required": ["translated_word", "spelling", "description"]
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for children who speaks in Bahasa Indonesia."},
            {"role": "user", "content": f"Translate the English word '{word}' to Bahasa Indonesia, then spell the translated word letter by letter for children."}
        ],
        functions=functions,
        function_call={"name": "spell_word_indonesian"}
    )

    args = response.choices[0].message.function_call.arguments
    parsed = json.loads(args)
    return parsed

def history(image_path, translated_word, spelled_word, description, csv_path='history.csv'):
    spelled_word = " - ".join(spelled_word).upper()

    data = {
        "word": translated_word.upper(),
        "spelling": spelled_word,
        "description": description,
        "image": image_path
    }

    if os.path.exists(csv_path):
        dataset = pd.read_csv(csv_path)
        dataset = pd.concat([dataset, pd.DataFrame([data])], ignore_index = True)
    else:
        dataset = pd.DataFrame([data])
    
    dataset.to_csv(csv_path, index=False)
    print(f"Data added to {csv_path}")

def upload_to_cloudinary(image_path):
    print("Function Cloudinary Called")
    global_path = cloudinary.uploader.upload(image_path)
    print("Successfully Upload To Cloudinary")
    return global_path['secure_url']

st.html(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">
    <style>
    .texttitle{
        font-size: 70px;
        font-weight: bold;
        margin-bottom: 25px;
    }
    .textdescribe{
        font-size: 22px;
    }

    @media only screen and (max-width: 600px) {
        .texttitle{
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .textdescribe{
            font-size: 14px;
        }
    }

    .stApp {
        background: radial-gradient(at 70% 30%, #f06acb, transparent 60%),
                    radial-gradient(at 30% 20%, #6f5cff, transparent 60%),
                    radial-gradient(at 90% 90%, #c6ffc6, transparent 60%),
                    radial-gradient(at 30% 75%, #6a84b5, transparent 60%);
        background-color: #d4d9ff;
        background-attachment: fixed;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    [data-testid=stSidebar] {
        background-image: linear-gradient(#000b14, #001627);
        color: white;
    }
    .textbox{
        background-image: linear-gradient(#000b14, #0b0b40);
        margin-top: 40px;
        //background-color: #001627;
        border-radius: 35px;
        text-align: center;
        padding: 4.5vw;
        filter: drop-shadow(0px 8px 10px black)
    }
    .topbox{
        background-image: linear-gradient(#000b14, #0b0b40);
        margin-top: 1.5vh;
        border-radius: 40px;
        text-align: center;
        margin-bottom: 0px;
        filter: drop-shadow(0px 4px 5px black)
    }
    .text{
        text-shadow: 0px 0.5px 2px #0000ff;
        margin: 0px;
        padding: 0px;
    }

    .headertext{
        font-weight: bold;
    }
    
    </style>

    <body>
    </body>
    """
)

st.html("""
    <div class="topbox" style="font-size:20px;">
        <p class="texttitle">Pix-it!</p>
    </div>
    """)

# enable = st.checkbox("Enable camera")
picture = st.camera_input("", disabled=False, label_visibility="hidden")

if picture:

    with st.spinner("Analyzing image..."):
        img = Image.open(picture).convert("RGB")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            img.save(tmp_file.name)
            temp_path = tmp_file.name

        weights = MobileNet_V3_Large_Weights.DEFAULT
        model = mobilenet_v3_large(weights=weights)
        model.eval()
        preprocess = weights.transforms()
        batch = preprocess(img).unsqueeze(0)

        prediction = model(batch).squeeze(0).softmax(0)
        class_id = prediction.argmax().item()
        score = prediction[class_id].item()
        category_name = weights.meta["categories"][class_id]

        print(f"Detected: {category_name} ({100 * score:.1f}%)")

        spell_data = get_translated_and_spelled_world(category_name)
        global_path = upload_to_cloudinary(temp_path)

        history(global_path, spell_data['translated_word'], spell_data['spelling'], spell_data['description'])
        spelling_sentence = f"Mari Mengejanya Bersama: {' -- '.join(spell_data['spelling']).upper()}. {spell_data['translated_word'].upper()}"

        print("Generated TTS text:", spelling_sentence)

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="onyx",
            input=spelling_sentence,
            response_format="wav"
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    st.markdown(
        f"""
        <div class="textbox">
            <p class="texttitle text", style="font-size:35px;">{spell_data['translated_word'].upper()}</p>
            <p class="textdescribe text", style="font-size:18px;">{spell_data['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.audio(response.content, format="audio/wav", autoplay=True)
