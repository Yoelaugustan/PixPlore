import streamlit as st

st.markdown(
    """
    <style>
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
    </style>

    <body>
    </body>
    """,
    unsafe_allow_html=True
)

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)

st.markdown("""<span style='color: black;'>This is black text</span>""")
st.write("f:black[Hey apple! Hey Apple!]")