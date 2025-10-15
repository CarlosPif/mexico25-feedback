import streamlit as st

Home = st.Page(
    "my_app/Home.py", title="Risk / Reward", icon=":material/dashboard:", default=True
)

General-overview = st.Page(
    "my_app/pages/General-overview.py", title="Details", icon=":material/details:", default=True
)

pg = st.navigation(
    {
        "Menorca 2025": [],
        "Mexico 2025": [Home: {General-overview}],
    }
)

pg.run()