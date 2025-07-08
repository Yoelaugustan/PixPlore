import streamlit as st

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <div class="topbox" style="font-size:20px;">
        <p class="texttitle">Pix-it!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# enable = st.checkbox("Enable camera")
picture = st.camera_input("", disabled=False, label_visibility="hidden")

if picture:
    # st.image(picture)


    ### Prediction Output Goes Here ###
    ImagePredict = "BEE"
    ImageDescription = "According to all known laws of aviation, there is no way a bee should be able to fly."

    st.markdown(
        f"""
        <div class="textbox">
            <p class="text, texttitle">{ImagePredict}</p>
            <p class="text, textdescribe">{ImageDescription}</p>
        </div>
        """,
        unsafe_allow_html=True
    )