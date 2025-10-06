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

