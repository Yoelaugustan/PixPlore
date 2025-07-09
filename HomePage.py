import streamlit as st

st.set_page_config(layout="wide")

st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@100..900&display=swap" rel="stylesheet">

<style>
section.main > div {
    max-width: 100vw;
}
.stApp > header, .stApp > footer {
    display: none;
}
.stApp .main .block-container {
    padding: 0;
    margin: 0;
}

.stApp {
    background: radial-gradient(at 30% 20%, #f06acb, transparent 60%),
        radial-gradient(at 70% 25%, #6f5cff, transparent 60%),
        radial-gradient(at 30% 80%, #c6ffc6, transparent 60%),
        radial-gradient(at 90% 90%, #6a84b5, transparent 60%);
    background-color: #d4d9ff;
    background-repeat: no-repeat;
    background-size: cover;
    min-height: 100vh;
}

section[data-testid="stMain"] {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}       

[data-testid="stSidebar"] {
    background: linear-gradient(#000b14, #001627);
    color: white;
}
[data-testid="stSidebar"] * {
    color: white;
}
.stAppToolbar{
    background-color:#000b14;
    color : white;
    }
.texttitle {
    font-size: 6vw;
    font-weight: 800;
    color: #000000;
    margin: 0;
    padding: 0;
    text-shadow: 0px 1.75px 4px black;
}
.textslogan {
    font-size: 2vw;
    font-weight: 600;
    color: #000000;
    margin: 0;
    padding: 0;
    text-shadow: 0px 1px 2px black;
}
.textsubslogan {
    font-size: 1.7vw;
    font-weight: 400;
    color: #000000;
    margin: 0;
    padding: 0;
}

@media only screen and (max-width: 600px) {
    .texttitle {
        font-size: 12vw;
    }
    .textslogan {
        font-size: 5vw;
    }
    .textsubslogan {
        font-size: 4vw;
    }
}
</style>

<div style="display: flex; align-items: center; height: 100%;">
    <div class='titleback'>
        <p class='texttitle'>PixPlore</p>
        <p class='textslogan'>Learning through lenses, growing through curiosity.</p>
        <p class='textsubslogan'>
            Where ordinary objects become valuable lessons, simply through a lens.
        </p>
    </div>
</div>
""")
