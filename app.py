import streamlit as st
from apps.business import business_market, business_dashboard
from apps.influencer import influencer_market, influencer_dashboard


def main():
    with st.sidebar:
        st.title("Sharelinks")
        role = st.selectbox(options=["Business", "Influencer"], label="Choose your role")
    
    # Currently, both roles lead to the same page. This might need to be updated in the future.
    if role == "Business":
        page = st.selectbox(options=["Marketplace", "Dashboard"], label="Choose your page")
        if page == "Marketplace":
            business_market()
        else:
            business_dashboard()
    else:  # Influencer
        page = st.selectbox(options=["Marketplace", "Dashboard"], label="Choose your page")
        if page == "Marketplace":
            influencer_market()
        else:
            influencer_dashboard()
    
if __name__ == "__main__":
    st.set_page_config(
        page_title="Sharelinks",
        page_icon=":star:",
        layout='wide'
    )
    main()