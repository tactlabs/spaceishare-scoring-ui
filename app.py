from typing import Dict
import streamlit as st
import pandas as pd 
import numpy as np 
from pipeline import get_features
from scoring import get_score
from scrape import scrape_details


st.write('''
    # Spacieshare Ad Score
''')

def create_df(data : Dict):
    n = [[data[col] for col in data]]
    return pd.DataFrame(n, columns = data.keys())

def compute_score(df):
    validate = get_features(df)
    score = get_score(validate)[0]
    return score

def main():
    url = st.text_input('Spaceishare URL :')
    my_bar = st.progress(0)
    if 'https://spaceishare.com/listing/parking-space' not in url:
        st.error('it only accepts spaceishare ad-listings url ...')
        url = None
    if url:
        my_bar.progress(5)
        my_bar.progress(20)
        data = scrape_details(url)

        my_bar.progress(25)
        df = create_df(data)

        my_bar.progress(85)
        score = compute_score(df)

        my_bar.progress(100)
        # score = 100
        st.markdown(f'''
        
        #### score : {score}
        
        ''')

        st.write('')
        st.markdown(f"#### title : {data['name']}")
        st.markdown(f"#### price : {data['price']}")
        st.markdown(f"#### type of space : {data['type of space']}")
        st.markdown(f"#### hosted by : {data['hosted by']}")


main()

