from pyairtable import Api
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
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

#=============CONFIG===========================
startup_founders = {
    "ROOK": ["Marco Benitez", "Jonas Ducker", "Daniel Martínez"],
    "Figuro": ["Juan Camilo Gonzalez"],
    "Admina": ["David Gomez", "Andres Gomez"],
    "Thalla": ["Samuel Gomez", "Daniel Salinas"],
    "Ecosis": ["Enrique Arredondo", "Roberto Riveroll"],
    "CALMIO": ["Andrés Ospina", "Camilo Ospina"],
    "Pitz": ["Natalia Salcedo"],
    "BondUp": ["Michelle Schintzer"],
    "Jelt": ["Sergio Ramirez"],
    "Moabits SL": ["Alejandro Ortiz", "David Santibanez", "Juan Martin Pawluszek"],
    "Ximple": ["Daniel Sujo", "Joao Ramos"],
    "Kuri": ["Ludwig Pucha Cofrep"],
    "CROMODATA": ["Juan Pablo  Merea Otermin", "Keila Barral Masri", "Matias  Karlsson"],
    "Ternadia": ["Angel Sanchez", "Raul Merino"],
    "Tu Cambio": ["Luis Saavedra", "Carla Leal"],
    "Airbag": ["Adrian Trucios"],
    "Handit.ai": ["Jose Manuel Ramirez", "Cristhian Camilo Gomez"],
    "Verticcal": ["Santiago Gallo Restrepo", "Pablo Sanchez Villamarin"],
    "Neat": ["Nicolas Chacon", "Javier Benavides"],
    "CIFRATO": ["Yerson Cacua", "Juan Pisco"],
    "Konvex": ["Andres Cristobal", "Sosa Tellez"]
}

risk_reward_fields = {
    "risk_scores": [
        "RISK | State of development_Score",
        "RISK | Momentum_Score",
        "RISK | Management_Score"
    ],
    "risk_flags": [
        "RISK | State of development_Flag",
        "RISK | Momentum_Flag",
        "RISK | Management_Flag"
    ],
    "risk_exp": [
        "RISK | State of development_exp",
        "RISK | Momentum_exp",
        "RISK | Management_exp",
    ],
    "reward_scores": [
        "Reward | Market_Score",
        "Reward | Team_Score",
        "Reward | Pain_Score",
        "Reward | Scalability_Score"
    ],
    "reward_flags": [
        "Reward | Market_Flag",
        "Reward | Team_Flag",
        "Reward | Pain_Flag",
        "Reward | Scalability_Flag"
    ],
    "reward_exp": [
        "Reward | Market_exp",
        "Reward | Team_exp",
        "Reward | Pain_exp",
        "Reward | Scalability_exp"
    ]
}

for subject in ["risk_scores", "reward_scores"]:
    for field in risk_reward_fields[subject]:
        if field not in df_em.columns:
            df_em[field] = np.nan

if "Startup" not in df_em.columns:
    df_em["Startup"] = np.nan

#Vamos con ellooooo
st.set_page_config(
    page_title="Opencall Dashboard Decelera Mexico 2025",
    layout="wide"
)

st.markdown("""
<style>
h5 {
text-align: center;
}
</style>

<h5>Risk - Reward Matrix</h5>
""", unsafe_allow_html=True)

#vamos a darle la vuelta a risk 

df_em[risk_reward_fields["risk_scores"]] = 5 - df_em[risk_reward_fields["risk_scores"]]

#vamosa calcular un par de medias

def grouped_means(df):
    risk_mean = df[risk_reward_fields["risk_scores"]].stack().mean()
    reward_mean = df[risk_reward_fields["reward_scores"]].stack().mean()

    return pd.Series({
        "risk_mean": risk_mean,
        "reward_mean": reward_mean
    })

df_em_means = df_em.groupby("Startup").apply(grouped_means).reset_index()

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_em_means["risk_mean"],
    y=df_em_means["reward_mean"],
    mode='markers+text',
    text=df_em_means["Startup"],
    textposition="top center",
    marker=dict(
        size=10,
        color=df_em_means["risk_mean"],
        colorscale='Viridis',
        showscale=True
    )
))

st.plotly_chart(fig)