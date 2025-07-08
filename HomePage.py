import streamlit as st

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet">

<style>
    .texttitle{
            font-size: 135px;
            font-weight: bold;
            margin: 0;
            padding: 0;
            color: #000000;
            text-shadow: 0px 1.75px 4px black;
    }
        .textslogan{
            font-size: 35px;
            font-weight: bold;
    }
        .textsubslogan{
            font-size: 30px;
    }
            
    @media only screen and (max-width: 600px) {
        .texttitle{
            font-size: 60px;
            font-weight: bold;
            margin: 0;
            padding: 0;
            color: #000000;
            text-shadow: 0px 1.75px 4px black;
        }
        .textslogan{
            font-size: 15px;
             font-weight: bold;
        }
        .textsubslogan{
            font-size: 13px;
        }
    }
            
            
    html, body, .page {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
    }

    .barlow-semibold {
        font-family: "Barlow", sans-serif;
        font-weight: 600;
        font-style: normal;
        text-shadow: 0px 1px 2px black;
    }        
    
    .mainbg {
        width: 100%;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        //background-image: url('GradientMesh.png')
        //background-image: linear-gradient(to right, #2da1d6 , #66dbff);
        background: radial-gradient(at 30% 20%, #f06acb, transparent 60%),
            radial-gradient(at 70% 25%, #6f5cff, transparent 60%),
            radial-gradient(at 30% 80%, #c6ffc6, transparent 60%),
            radial-gradient(at 90% 90%, #6a84b5, transparent 60%);
        background-color: #d4d9ff;
        padding: 0 10vw;
        box-sizing: border-box;
    }

    .titleback {
        //background-image: linear-gradient(to right, #2da1d6 , #66dbff);
        border-radius: 132px;
        //padding: 35px 130px 35px 88px;
        width: 90%;
    }

    .titleheader {

    }
    section.main > div {
        max-width: 98rem;
    }
    .stApp .main .block-container {
        padding: 0rem;
        padding-top: 1.72rem;
    }
    [data-testid=stSidebar] {
        background-image: linear-gradient(#000b14, #001627);
        color: white;
    }
</style>

<body class='page'>
    <div class='mainbg' background='GradientMesh.png'>
        <div class='titleback'>
            <p class='texttitle'>PixPlore</p>
            <p class = 'barlow-semibold, textslogan', style='margin-top: 0px; margin-bottom: 5px; padding: 0; color: #000000; font-style:barlow;'>Learning through lenses, growing through curiosity.</p>
            <p class = 'barlow-semibold, textsubslogan', style='margin-top: 10px; padding: 0;color: #000000;'>
                Where ordinary objects become valuable lessons, simply through a lens.
            </p>
        </div>
    </div>
</body>
""", unsafe_allow_html=True)