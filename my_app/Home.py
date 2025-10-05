from pyairtable import Api
import pandas as pd
import streamlit as st

api_key = st.secrets["airtable"]["api_key"]
base_id = st.secrets["airtable"]["base_id"]

table_id_team = st.secrets["airtable"]["table_id_team"]
table_id_em = st.secrets["airtable"]["table_id_em"]

api = Api(api_key)
table_em = api.table(base_id, table_id_em)
table_team = api.table(base_id, table_id_team)


records_team = table_team.all(view="Mexico 2025")
records_em = table_em.all(view="Mexico 2025")

data_team = [record['fields'] for record in records_team]
data_em = [record['fields'] for record in records_em]

df_team = pd.DataFrame(data_team)
df_em = pd.DataFrame(data_em)

def fix_cell(val):
    if isinstance(val, dict) and "specialValue" in val:
        return float("nan")
    return val

df_team = df_team.map(fix_cell)
df_em = df_em.map(fix_cell)

#Vamos con ellooooo
st.set_page_config(
    page_title="Opencall Dashboard Decelera Mexico 2025",
    layout="wide"
)

#primero quiero poner un titulo 

st.markdown("""
<style>
.outer-container {
    display: flex;
    justify-content: center; /* Centra horizontalmente */
    width: 100%; /* Ocupa todo el ancho disponible */
}
.container {
    display: flex;
    align-items: center;
}
.logo-img {
    width: 80px;
    height: 80px;
    margin-right: 20px;
}
.title-text {
    font-size: 2.5em; /* Tamaño del título */
    font-weight: bold;
}
</style>
<div class="outer-container">
<div class="container">
    <img class="logo-img" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTb_FaT4TLTs0RVC0zxBnYT2pUjrN3JJKIY6Q&s">
    <h1 class="title-text">Program Feedback<br>México 2025</h1>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<h4>Here you will find the most relevant feedback for today</h4>
""",
unsafe_allow_html=True)
