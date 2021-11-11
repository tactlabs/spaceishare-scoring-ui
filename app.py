from typing import Dict
import streamlit as st
import pandas as pd 
import numpy as np 
from pipeline import get_features
from scoring import get_score


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
    url = st.text_input('url')

    my_bar = st.progress(0)
    my_bar.progress(5)
    if url:

        my_bar.progress(20)
        # data = scrape_details(url)

        my_bar.progress(25)
        # df = create_df(data)

        my_bar.progress(85)
        # score = compute_score(validate)

        my_bar.progress(100)
        score = 100
        st.markdown(f'''
        
        #### score : {score}
        
        ''')


main()

