import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid
from ..config import OFFER_COLUMNS

# Initialize or load offers
def load_offers():
    if "offers" not in st.session_state:
        if os.path.exists("data/offers.csv"):
            st.session_state.offers = pd.read_csv("data/offers.csv")
        else:
            st.session_state.offers = pd.DataFrame(columns=OFFER_COLUMNS)
    return st.session_state.offers

def load_business():
    if "business_id" not in st.session_state:
        st.session_state.business_id = "1"


# Post a new offer
def post_offer():
    st.title("Post a New Offer")
    
    with st.form("offer_form"):
        product_name = st.text_input("Brand / Product")
        product_description = st.text_area("Description")
        product_url = st.text_input("URL")
        payment_per_100_click = st.number_input("Payment per 100 Clicks", min_value=1.0)
        payment_per_purchase = st.number_input("Payment per Purchase", min_value=1.0)
        start_date = st.date_input("Campaign Start Date", value=datetime.today())
        maximum_budget = st.number_input("Maximum Budget", min_value=100, step=50)
        influencer_profile = st.text_input("Preferred Influencer Profile")

        submitted = st.form_submit_button("Submit Offer")
        
        if submitted:
            offers = load_offers()
            new_offer = pd.DataFrame({
                "offer_id": [str(uuid.uuid4())],
                "business_id": [st.session_state.business_id],
                "Brand / Product": [product_name],
                "Brand / Product Description": [product_description],
                "Brand / Product URL": [product_url],
                "Payment per 100 Clicks": [payment_per_100_click],
                "Payment per Purchase": [payment_per_purchase],
                "Start Date": [start_date],
                "Maximum Budget": [maximum_budget],
                "Preferred Influencer Profile": [influencer_profile]
            })
            st.session_state.offers = pd.concat([offers, new_offer], ignore_index=True)
            st.session_state.offers.to_csv("data/offers.csv", index=False)
            st.success("Offer Posted Successfully!")
            st.session_state.posting = False
            st.rerun()

# Browse offers created by other businesses
def main():
    st.title("Marketplace")

    offers = load_offers()
    load_business()
    if len(offers) == 0:
        st.write("No offers available at the moment.")
    else:
        st.dataframe(offers)

    if st.button("Post an offer"):
        st.session_state.posting = True

    if "posting" in st.session_state and st.session_state.posting:
        post_offer()

if __name__ == "__main__":
    main()