import streamlit as st
import os
import torch
import requests

from model import create_model
from helper_func import *


st.title("Pokédex")
st.markdown("for generation one **Pokémon**")

df, df_ = load_df('utils/pokemon.csv', 'utils/moves.csv')

model = create_model()

img = st.file_uploader("Upload your Pokémon Image", type=['jpeg', 'jpg', 'png', 'webp'])

if img:
    images = create_image(img)
    pred = make_pred(model, images[1])

    url_img = get_url(pred)
    response_code = requests.get(url_img).status_code
    
    if response_code == 200:
        st.markdown(f"![Alt Text]({url_img})")
    else:
        st.image(images[0].resize((224, 224)))

    if pred in df['species'].values:
        details = get_pokemon_details(pred, df, df_)

        text = f"-- This is {pred}, a {details[0]} type {details[1]}\n\n-- It has a special move called {details[2]}\n\n-- {details[3]}\n\n_"
        st.text(text)

        audio_bytes = get_audio(text[:-1])
        st.audio(audio_bytes, format='audio/ogg', start_time=0)
    
        os.remove('hello.ogg')
            
    else:
        text = f"This is {pred}\nCurrently, there is not much details about {pred} in my database!!!\n\n_"
        st.text(text)

        audio_bytes = get_audio(text[:-1])
        st.audio(audio_bytes, format='audio/ogg', start_time=0)

        os.remove('hello.ogg')
