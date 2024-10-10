import streamlit as st
import pandas as pd
import os

from ..config import OFFER_COLUMNS

def load_influencer():
    if "influencer_id" not in st.session_state:
        st.session_state.influencer_id = "1"
    if "deals" not in st.session_state:
        if os.path.exists("data/deals.csv"):
            all_deals = pd.read_csv("data/deals.csv", dtype={"influencer_id": str, "business_id": str})
            st.session_state.deals = all_deals[all_deals["influencer_id"] == st.session_state.influencer_id]
        else:
            st.session_state.deals = pd.DataFrame(columns=["influencer_id", "status"] + OFFER_COLUMNS)


def main():

    load_influencer()
    st.title("Influencer Dashboard")

    st.dataframe(st.session_state.deals)


