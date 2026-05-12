import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Netflix Analytics", layout="wide")

# Custom CSS (Premium UI)
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
    }
    .main {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎬 Netflix Analytics Dashboard")

# =========================
# FILE UPLOAD (IMPORTANT)
# =========================
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file)
    st.sidebar.success("File uploaded successfully!")
else:
    df = pd.read_csv("netflix.csv")

# =========================
# DATA CLEANING
# =========================
df = df.dropna(subset=["type", "release_year", "country"])

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

type_filter = st.sidebar.multiselect(
    "Content Type",
    df["type"].unique(),
    default=df["type"].unique()
)

year_filter = st.sidebar.slider(
    "Release Year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2000, 2021)
)

country_filter = st.sidebar.multiselect(
    "Country",
    df["country"].unique(),
    default=df["country"].unique()[:5]
)

filtered_df = df[
    (df["type"].isin(type_filter)) &
    (df["release_year"].between(year_filter[0], year_filter[1])) &
    (df["country"].isin(country_filter))
]

# =========================
# KPI CARDS
# =========================
total_titles = filtered_df.shape[0]
movies = filtered_df[filtered_df["type"] == "Movie"].shape[0]
shows = filtered_df[filtered_df["type"] == "TV Show"].shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", shows)

st.markdown("---")

# =========================
# CHARTS ROW 1
# =========================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(filtered_df, names="type", title="Content Distribution")
    fig1.update_layout(template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    year_data = filtered_df["release_year"].value_counts().sort_index()
    fig2 = px.line(
        x=year_data.index,
        y=year_data.values,
        labels={'x': 'Year', 'y': 'Count'},
        title="Content Growth Over Time"
    )
    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# CHARTS ROW 2
# =========================
col1, col2 = st.columns(2)

with col1:
    top_countries = filtered_df["country"].value_counts().head(10)
    fig3 = px.bar(
        x=top_countries.values,
        y=top_countries.index,
        orientation="h",
        title="Top Countries"
    )
    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    genre_series = filtered_df["listed_in"].str.split(", ").explode()
    top_genres = genre_series.value_counts().head(10)
    
    fig4 = px.bar(
        x=top_genres.values,
        y=top_genres.index,
        orientation="h",
        title="Top Genres"
    )
    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# DATA PREVIEW
# =========================
st.markdown("---")
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head(20))