import streamlit as st
import pandas as pd
from ..config import OFFER_COLUMNS
import os

def load_business():
    if "business_id" not in st.session_state:
        st.session_state.business_id = "1"

    all_deals = pd.read_csv("data/deals.csv", dtype={"business_id": str})
    deals = all_deals[all_deals["business_id"] == st.session_state.business_id]
    return deals


def handle_accept(deals, deal_id):
    deals.loc[deals["deal_id"] == deal_id, "status"] = "accepted"
    st.success(f"Deal {deal_id} accepted!")

def handle_reject(deals, deal_id):
    deals.loc[deals["deal_id"] == deal_id, "status"] = "rejected"
    st.error(f"Deal {deal_id} rejected!")

def main():
    st.title("Business Dashboard")

    deals = load_business()

    # Add column headers
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    col1.subheader("Product | per 100 Clicks | per Purchase")
    col2.subheader("Influencer")
    col3.subheader("Accept")
    col4.subheader("Reject")

    # Add a separator after headers
    st.markdown("---")

    if not deals.empty:
        for index, row in deals.iterrows():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            # Display deal information
            with col1:
                st.write(f"{row['Brand / Product']} | {row['Payment per 100 Clicks']:.2f} | {row['Payment per Purchase']:.2f}")
            
            with col2:
                st.write(f"**Influencer:** {row['influencer_id']}")
            
            # Accept button
            with col3:
                if st.button("Accept", key=f"accept_{index}"):
                    handle_accept(deals, row['deal_id'])
            
            # Reject button
            with col4:
                if st.button("Reject", key=f"reject_{index}"):
                    handle_reject(deals, row['deal_id'])
            
            # Add a separator between deals
            st.markdown("---")
    else:
        st.write("No deals available.")

