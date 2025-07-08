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
import torchvision.transforms as transforms

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

def history(image_path, translated_word, spelled_word, , csv_path='history.csv'):
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

PATH = r"C:\Users\Yoel\Documents\Calvin_AI_Youth_Camp\PixPlore\download (7).jpeg"

img = Image.open(PATH).convert("RGB")

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
global_path = upload_to_cloudinary(PATH)

history(global_path, spell_data['translated_word'], spell_data['spelling'], spell_data['description'])
spelling_sentence = f"Mari Mengejanya Bersama: {' -- '.join(spell_data['spelling']).upper()}. {spell_data['translated_word'].upper()}"

print("Generated TTS text:", spelling_sentence)

AUDIO_FILENAME = "spelling.wav"

response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="onyx",
    input=spelling_sentence,
    response_format="wav"
)

with open(AUDIO_FILENAME, "wb") as f:
    f.write(response.content)

wave_obj = sa.WaveObject.from_wave_file(AUDIO_FILENAME)
play_obj = wave_obj.play()
play_obj.wait_done()

if os.path.exists(AUDIO_FILENAME):
    os.remove(AUDIO_FILENAME)

