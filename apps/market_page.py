import streamlit as st
from streamlit import session_state as state
from collections import defaultdict
import pandas as pd
import subprocess
import datetime
    
from xdataframe import *    

tag = "AI"

def main():

    st.title(f"Content Maker")

    st.subheader("Daily News") 
    if "date" not in state:
        state.date = None
    if 'chosen_dfs' not in state:
        state.chosen_dfs = defaultdict(pd.DataFrame)
    if 'user_dfs' not in state:
        state.user_dfs = defaultdict(pd.DataFrame)

    state.date = st.date_input("Current Date", value=datetime.date.today()).strftime("%m-%d-%Y")

    df = read_user_df(tag, state.date)
    if df is None:
        return
    
    dfs = {topic: df_group for topic, df_group in df.groupby('category')}
    # Iterate through each category and its DataFrame
    for category, df in dfs.items():

        df = df.sort_values(by='likes', ascending=False)
        df.reset_index(drop=True, inplace=True)
        with st.expander(category):
            st.subheader(category)
            if 'chosen' not in df.columns:
                df.loc[:, 'chosen'] = False
            streamlit_df = df[['username', 'en_title', 'cn_title', 'en_body', 'cn_body', 'likes', 'url','chosen']]
            streamlit_df = st.data_editor(streamlit_df)

            if st.button('Save', key=f"save_{category}"):
                df['chosen'] = streamlit_df['chosen']
                state.user_dfs[category] = df 
                state.chosen_dfs[category] = df[streamlit_df['chosen']]
                st.success(f"Saved {category} successfully!")


    if st.button('Generate'):
        user_df = pd.concat(state.user_dfs.values(), ignore_index=True)
        user_df.reset_index(drop=True, inplace=True)
        save_user_df(user_df, date=state.date)
        
        chosen_df = pd.concat(state.chosen_dfs.values(), ignore_index=True)
        chosen_df.reset_index(drop=True, inplace=True)
        save_final_df(chosen_df)

        process = subprocess.Popen(["python", "launcher_d.py"])
        process.wait()
        st.success(f"Generated successfully!")

    
    st.subheader("Past Week News")
    df = pd.DataFrame()
    for i in range(7):
        date = (datetime.date.today() - datetime.timedelta(days=i+1)).strftime("%m-%d-%Y")
        daily_df = read_user_df(tag, date)
        if daily_df is None:
            continue
        daily_df = daily_df.sort_values(by='likes', ascending=False)
        df = pd.concat([df, daily_df], ignore_index=True)
    
    df.reset_index(drop=True, inplace=True)
    with st.expander("Past Week News"):
        st.subheader("Past Week News")
        streamlit_df = df[['timestamp', 'category', 'username', 'en_title', 'cn_title', 'en_body', 'cn_body', 'likes', 'url']]
        streamlit_df = st.dataframe(streamlit_df)


