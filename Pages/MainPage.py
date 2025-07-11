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
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

cloudinary.config(
    cloud_name = "danlcwpuc",
    api_key = "721559911819599",
    api_secret = "4_VEcsJ8sUvdf1Olb-2ragubE_0",
    secure = True
)
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def get_spelled_and_description_word(word):
    functions = [
        {
            "name": "spell_word",
            "description": f"{option_style}",
            "parameters": {
                "type": "object",
                "properties": {
                    "spelling": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Spell the word letter by letter so children could understand"
                    },
                    "description": {
                        "type": "string",
                        "description": f"Describe the {word} in around 1 to 3 short sentences that is understandable for children"
                    }
                },
                "required": ["spelling", "description"]
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for children to help spell a word"},
            {"role": "user", "content": f"Spell the {word} letter by letter for children to spell."}
        ],
        functions=functions,
        function_call={"name": "spell_word"},
        temperature=0.2
    )

    args = response.choices[0].message.function_call.arguments
    parsed = json.loads(args)
    return parsed

def history(image_path, word, spelled_word, description, csv_path='history.csv'):
    spelled_word = " - ".join(spelled_word).upper()

    data = {
        "word": word.upper(),
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
    [data-testid="stSidebar"] {
        background: linear-gradient(#000b14, #001627);
        color: white;
    }
    [data-testid="stSidebar"] * {
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

    # [data-testid="stSelectbox"] {
    #     background-color: #0b0b40;
    #     border-radius: 12px;
    #     padding: 10px;
    # }

    [data-testid="stSelectbox"] label {
        text-shadow: 0px 0.5px 2px #0000ff;
        margin-bottom: 10px;
    }

    .st-bb{
    background-color:black
    }
    
    .stAppToolbar{
    background-color:#000b14;
    color : white;
    }

    </style>

    <body>
    </body>
    """
)

st.html("""
    <div class="topbox" style="font-size:20px; color: #ffffff;">
        <p class="texttitle">Pix-it!</p>
    </div>
""")

with st.sidebar:   
    chosen_option_voice = st.selectbox(
        'Choose your teacher!',
        ('Friendly and helpful (suggested)', 'Bright, expressive and playful', 'Calm, evenly paced', 'Expressive and engaging', 'Serious', 'Soft and Gentle')
    )
    if chosen_option_voice:
        if chosen_option_voice == 'Friendly and helpful (suggested)':
            option_voice = 'nova'
        elif chosen_option_voice == 'Bright, expressive and playful':
            option_voice = 'shimmer'
        elif chosen_option_voice == 'Calm, evenly paced':
            option_voice = 'echo'
        elif chosen_option_voice == 'Expressive and engaging':
            option_voice = 'fable'
        elif chosen_option_voice == 'Serious':
            option_voice = 'onyx'

    chosen_option_style = st.selectbox(
        'Choose the teaching style!',
        ('Teacher', 'Friend', 'Comedian')
    )
    if chosen_option_style == 'Teacher':
        option_style = 'You are a great and caring kindergarten teacher, Can you explain the word simply in a way which the children could easily understand'
    elif chosen_option_style == 'Friend':
        option_style = 'You are a kindergarten student with above-average intelligence, one of your close friends is asking for your help as he struggles to understand something, can you help them?'
    elif chosen_option_style == 'Comedian':
        option_style = 'You are a great, humerous kindergarten teacher, you often crack jokes to help students have a fun time while learning, while at the same time, still allowing them to learn well.'
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

        spell_data = get_spelled_and_description_word(category_name)
        global_path = upload_to_cloudinary(temp_path)

        if chosen_option_style == 'Teacher':
            thing_to_say = "Are You Ready Kids, Let's Spell This Together."
        elif chosen_option_style == 'Friend':
            thing_to_say = "Are You Ready? Spell this with me!"
        elif chosen_option_style == 'Comedian':
            thing_to_say = "Alright, pay attention! This is how you spell it."

        history(global_path, category_name, spell_data['spelling'], spell_data['description'])
        spelling_sentence = f"{thing_to_say}: {' -- '.join(spell_data['spelling']).upper()}. {category_name.upper()} -- {spell_data['description']}"

        print("Generated TTS text:", spelling_sentence)

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=f"{option_voice}",
            input=spelling_sentence,
            response_format="wav"
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)
    
    st.markdown(
        f"""
        <div class="textbox">
            <p class="texttitle text", style="font-size:35px; color: #ffffff;">{category_name.upper()}</p>
            <p class="textdescribe text", style="font-size:18px; color: #ffffff;">{spell_data['description']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.audio(response.content, format="audio/wav", autoplay=True)
