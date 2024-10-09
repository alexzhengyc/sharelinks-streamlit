import streamlit as st
from apps.business import business_market_page
from apps.influencer import influencer_market_page


def main():
    with st.sidebar:
        st.title("Sharelinks")
        role = st.selectbox(options=["Business", "Influencer"], label="Choose your role")
    
    # Currently, both roles lead to the same page. This might need to be updated in the future.
    if role == "Business":
        business_market_page()
    else:  # Influencer
        influencer_market_page()
    
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sharelinks",
        page_icon=":star:",
        layout='wide'
    )
    main()