import streamlit as st
from streamlit import session_state as state
from collections import defaultdict
import pandas as pd
import json
import datetime
    
from xdataframe import *   
from xmongo.search_data import * 

def main():

    st.title(f"Ranking")
    with st.expander("User", expanded=True):
        column_name = "user"
        
        start_date = st.date_input(key=f"Begin date {column_name}", label="Begin date", value=datetime.date.today() - datetime.timedelta(days=14))
        end_date= st.date_input(key=f"End date {column_name}", label="End date", value=datetime.date.today())
        filtered = st.checkbox(key=f"Filtered as AI {column_name}", label="Filtered as AI", value=True)

        categories = st.multiselect(key=f"Category {column_name}", label="Category", options=("Company News", "Product News", "Research News"), default=["Company News", "Product News", "Research News"])
        min_likes = st.number_input(key=f"Minimum likes {column_name}", label="Minimum likes", value=50)

        df = search(filter=filtered, category=categories, min_likes=min_likes, start_date=start_date, end_date=end_date)
        # group by user
        username_counts = df['username'].value_counts()
        username_counts  = username_counts.head(500)
        usernames = username_counts.keys()
        usernames = [f"{username}" for username in usernames]
        st.write(json.dumps(usernames))

    with st.expander("Search Term", expanded=True):
        column_name = "search term"
        st.subheader(f"Search {column_name}")

        start_date = st.date_input(key=f"Begin date {column_name}", label="Begin date", value=datetime.date.today() - datetime.timedelta(days=14))
        end_date= st.date_input(key=f"End date {column_name}", label="End date", value=datetime.date.today())
        filtered = st.checkbox(key=f"Filtered as AI {column_name}", label="Filtered as AI", value=True)

        categories = st.multiselect(key=f"Category {column_name}", label="Category", options=("Company News", "Product News", "Research News"), default=["Company News", "Product News", "Research News"])
        min_likes = st.number_input(key=f"Minimum likes {column_name}", label="Minimum likes", value=50)

        df = search(filter=filtered, category=categories, min_likes=min_likes, start_date=start_date, end_date=end_date)
        # group by user
        query_counts = df['query'].value_counts()
        top_queries = query_counts.head(20)
        st.bar_chart(top_queries)
        st.write(top_queries)

