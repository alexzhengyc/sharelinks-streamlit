import streamlit as st
import apps 
from apps.allpages import page_group


def main():
    page = page_group("p")
    
    with st.sidebar:
        st.title(f"Sharelinks")

        page.item("Marketplace", apps.market_page, default=True)
        page.item("Business Dashboard", apps.business_page)
        page.item("Influencer Dashboard", apps.influencer_page)

    page.show()
    
if __name__ == "__main__":
    
    st.set_page_config(
        page_title="Sharelinks",
        page_icon=":star:",
        layout='wide'
    )
    main()