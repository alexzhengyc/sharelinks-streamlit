import streamlit as st
from apps.business import market_page  # Updated import


def main():
    with st.sidebar:
        st.title("Sharelinks")
        role = st.selectbox(options=["Business", "Influencer"], label="Choose your role")
    
    # Currently, both roles lead to the same page. This might need to be updated in the future.
    if role == "Business":
        market_page()
    else:  # Influencer
        market_page()
    
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sharelinks",
        page_icon=":star:",
        layout='wide'
    )
    main()