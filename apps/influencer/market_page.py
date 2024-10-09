import streamlit as st
import pandas as pd
from datetime import datetime
import os
from ..config import OFFER_COLUMNS
# Initialize or load offers
def load_offers():
    if "offers" not in st.session_state:
        if os.path.exists("data/offers.csv"):
            st.session_state.offers = pd.read_csv("data/offers.csv", dtype={"business_id": str})
        else:
            st.session_state.offers = pd.DataFrame(columns=OFFER_COLUMNS)
    return st.session_state.offers


def load_influencer():
    if "influencer_id" not in st.session_state:
        st.session_state.influencer_id = "1"

    if "shopping_cart" not in st.session_state:
        if os.path.exists("data/shopping_cart.csv"):
            all_shopping_cart = pd.read_csv("data/shopping_cart.csv", dtype={"influencer_id": str, "business_id": str})
            st.session_state.shopping_cart = all_shopping_cart[all_shopping_cart["influencer_id"] == st.session_state.influencer_id]
        else:
            st.session_state.shopping_cart = pd.DataFrame(columns=["influencer_id"] + OFFER_COLUMNS)

# Browse offers created by other businesses
def main():
    st.title("Marketplace")

    load_offers()
    load_influencer()

    if len(st.session_state.offers) == 0:
        st.write("No offers available at the moment.")
    else:
        # Add a new column for the "Pick" button if it doesn't exist
        if 'Pick' not in st.session_state.offers.columns:
            st.session_state.offers['Pick'] = False
        
        # Display the dataframe with editable checkbox column
        edited_df = st.data_editor(
            st.session_state.offers,
            column_config={
                "Pick": st.column_config.CheckboxColumn(
                    "Pick",
                    help="Select to add to cart",
                    default=False,
                )
            },
            disabled=OFFER_COLUMNS,
            hide_index=True,
        )
        
        # Handle selections
        for index, row in edited_df.iterrows():
            if row['Pick'] and not st.session_state.offers.at[index, 'Pick'] and row['offer_id'] not in st.session_state.shopping_cart['offer_id'].values:
                new_item = row.to_dict()
                new_item["influencer_id"] = st.session_state.influencer_id
                st.session_state.shopping_cart = pd.concat([st.session_state.shopping_cart, pd.DataFrame([new_item])], ignore_index=True)
                st.success(f"Added {row['Brand / Product']} to your cart!")
                st.session_state.shopping_cart.to_csv("data/shopping_cart.csv", index=False)
                st.session_state.offers.at[index, 'Pick'] = True
        
        # Update the offers in session state
        st.session_state.offers = edited_df

    st.subheader("Shopping Cart")
    if len(st.session_state.shopping_cart) == 0:
        st.write("Empty cart.")
    else:

        st.dataframe(st.session_state.shopping_cart)

if __name__ == "__main__":
    main()