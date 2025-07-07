import streamlit as st
from operator import imod

for i in range(14):
    st.markdown("")

st.markdown("""
    
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

        .page{
            margin : 0;
            padding : 0;
            background-color : red;
        }

        .titleback{
            background-color : #001f37;
            border-radius : 150px;

            margin-left : 80px;
            margin-right : 80px;

            padding-left : 75px;
            padding-top : 25px;
            padding-bottom: 45px;
            padding-right: 130px;
        }

        .titleheader{
            font-size : 80px;
            padding : 0;
            margin : 0;
        }
        
    </style>
    <body class='page'>
        <div class = 'titleback'>
            <h1 class='titleheader'>StaySharp</h1>
            <p style = 'margin : 0; padding : 0;'>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus rutrum, nibh et vulputate rutrum, est turpis sollicitudin felis, eu pharetra arcu ante vitae justo.</p>
        </div>
    </body>    
""", unsafe_allow_html=True) 
