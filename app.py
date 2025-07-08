from torchvision.io import read_image
from torchvision.models import mobilenet_v3_large, MobileNet_V3_Large_Weights
from openai import OpenAI
import os
import simpleaudio as sa
import json

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
                    }
                },
                "required": ["translated_word", "spelling"]
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

PATH = r"C:\Users\Yoel\Documents\Calvin_AI_Youth_Camp\StaySharp\download (1).jpeg"
img = read_image(PATH)

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

spell_data = get_spelling_structured(category_name)
spelling_sentence = f"Lets Spell Together: {' - '.join(spell_data['spelling'])}. {spell_data['word'].capitalize()}"

print("Generated TTS text:", spelling_sentence)

AUDIO_FILENAME = "spelling.mp3"

response = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="nova",
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