import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# CSS untuk flip card saat diklik
card_css = """
<style>
section.main > div {
    max-width:98rem;
    }
    .stApp .main .block-container{
        padding: 0rem;
        padding-top: 1.72rem;
    }
    .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2){
        padding-top: 0.5rem
    }
    img[data-testid="stLogo"] {
            height: 3.5rem;
    }
    .stRadio div[role='radiogroup']>label{
        margin-right:5px
        padding-top: 0.1rem
    }
    
    div[data-testid="stSidebarHeader"] {
  justify-content: center;
  align-items: start;
  height: 1px;
  padding: 1.2em;
  padding-left: 2.6rem;

}

.card-container {
    display: grid;
    grid-template-columns: repeat(3, 200px);
    justify-content: center;
    gap: 30px;
    padding: 20px;
    border-style: solid;
    border-width: medium;
}

.flip-card {
    background-color: transparent;
    width: 200px;
    height: 200px;
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

# Tambahkan JavaScript supaya flip bisa saat diklik
card_js = """
<script>
document.querySelectorAll('.flip-card').forEach(card => {
    card.addEventListener('click', () => {
        card.classList.toggle('clicked');
    });
});
</script>
"""

# Daftar kartu
df = pd.read_csv('D:\Github\PixPlore\PixPlore\history.csv')
cards = [{"label": row['word'], "img": row['image']} for _, row in df.iterrows()]

# Buat kartu HTML
html = '<div class="card-container">'
if (cards):
    for card in cards:
        html += f'''
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <img src="{card["img"]}" alt="{card["label"]}">
                </div>
                <div class="flip-card-back">
                    {card["label"]}
                </div>
            </div>
        </div>
        '''
    html += '</div>'

    # Gabungkan semua dan tampilkan
    components.html(card_css + html + card_js, height=1000)
else:
    st.title("Please snap one picture first!")

#     col1, col2, col3, col4, col5 = st.columns([1, 3, 3, 3, 1])

# for i in range(0, len(image_urls), 3):
#     with col2:
#         if i < len(image_urls):
#             st.image(image_urls[i], use_column_width=True)
#     with col3:
#         if i+1 < len(image_urls):
#             st.image(image_urls[i+1], use_column_width=True)
#     with col4:
#         if i+2 < len(image_urls):
#             st.image(image_urls[i+2], use_column_width=True)