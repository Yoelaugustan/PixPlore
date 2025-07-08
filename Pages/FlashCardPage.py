import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import base64
from streamlit.web.server.websocket_headers import _get_websocket_headers
import os

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

st.html("""
<style>
section.main > div {
    max-width: 100vw;
}

html, body, .main, .scroll-container {
    overflow-x: hidden;
    max-width: 100vw;
}

.main {
    width: 100vw;
    overflow-y: auto;
    padding: 2rem;
    box-sizing: border-box;
}

.stApp > header, .stApp > footer {
    display: none;
}

.stApp .main .block-container {
    padding: 0;
    margin: 0;
}

.stApp {

    background: radial-gradient(at 80% 67%, #f06acb, transparent 60%),
        radial-gradient(at 11% 23%, #6f5cff, transparent 60%),
        radial-gradient(at 70% 30%, #c6ffc6, transparent 60%),
        radial-gradient(at 85% 90%, #6a84b5, transparent 60%);
        radial-gradient(at 15% 97%, #f7ff9e, transparent 60%);
    background-color: #d4d9ff;
    background-repeat: no-repeat;
    background-size: cover;
    height: 100vh;
}

section[data-testid="stMain"] {
    overflow: hidden;
    height: 100vh;
}

[data-testid="stSidebar"] {
    background: linear-gradient(#000b14, #001627);
    color: white;
}
[data-testid="stSidebar"] * {
    color: white;
}

</style>
""")

card_css = """
<style>
.card-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    justify-content: center;
    gap: 50px;
    padding: 40px;
    # border-style: solid;
    # border-width: medium;
}

.flip-card {
    background-color: transparent;
    width: 175px;
    height: 225px;
    perspective: 1000px;
}

.flip-card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s;
    transform-style: preserve-3d;
}

.flip-card.clicked .flip-card-inner {
    transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    overflow: hidden;
    text-overflow: ellipsis;
    word-wrap: break-word;
}

.flip-card-back {
    transform: rotateY(180deg);
    backface-visibility: hidden;
    overflow: hidden;
}

.flip-card-front {
    background-color: #fff;
    color: black;
}

.flip-card-front img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 15px;
}

.overlay-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.flip-card-back {
    background-color: #f2f2f2;
    color: black;
    transform: rotateY(180deg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    padding: 10px;
}

</style>
"""

card_js = """
<script>
document.querySelectorAll('.flip-card').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('clicked');
    });
});
</script>
"""

try:
    df = pd.read_csv('./history.csv')
    cards = [{"label": row['word'], "img": row['image']} for _, row in df.iterrows()]

    border_colors = [
        "#A0F8FF", "#FF8CC6", "#F86666", "#90D76B",
        "#CBA3FF", "#FFF685", "#A3DFFF", "#FCA3B7",
        "#D6FF70", "#B5FBC0", "#FFB347", "#FFD8A9",
        "#B3C7FF", "#66CFFF", "#6BD6D3", "#FFE266"
    ]

    html = '<div class="main"><div class="scroll-container"><div class="card-container">'

    for i, card in enumerate(cards):
        border_number = (i % 16) + 1
        border_b64 = image_to_base64(f"flashcard_borders/{border_number}.png")
        border_color = border_colors[i % len(border_colors)]

        html += f'''
            <div class="flip-card">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                        <div style="position: relative; width: 100%; height: 100%;">
                            <img src="{card["img"]}" alt="{card["label"]}" style="width: 100%; height: 100%; object-fit: cover;">
                            <img src="data:image/png;base64,{border_b64}" class="overlay-img">
                        </div>
                    </div>
                    <div class="flip-card-back" style="background-color: {border_color};">
                        <div style="text-align: center; padding: 10px; color: black;">
                            {card["label"]}
                        </div>
                    </div>
                </div>
            </div>
        '''
    html += '</div></div></div>'

    components.html(card_css + html + card_js, height=550, scrolling=True)

except Exception as e:
    st.error("An error occurred:")
    st.error(str(e))
    st.title("Please snap one picture first!")