import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Title
st.title("📊 Netflix Data Analysis Dashboard")
st.write("Interactive analysis of Netflix Movies & TV Shows")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()

# Data Cleaning
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])

df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['date_added'] = df['date_added'].ffill()

df['year_added'] = df['date_added'].dt.year

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Filters")

# Type filter
type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

# Country filter
country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].unique(),
    default=df['country'].unique()[:5]
)

# Year filter
year_filter = st.sidebar.slider(
    "Select Year Range",
    int(df['year_added'].min()),
    int(df['year_added'].max()),
    (2015, 2020)
)

# Search bar
search = st.sidebar.text_input("Search Title")

# Apply filters
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter)) &
    (df['year_added'].between(year_filter[0], year_filter[1]))
]

if search:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search, case=False)]

# ---------------- KPIs ----------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head())

# ---------------- VISUALIZATIONS ----------------
col1, col2 = st.columns(2)

# Movies vs TV Shows
with col1:
    st.subheader("🎬 Movies vs TV Shows")
    fig1, ax1 = plt.subplots()
    sns.countplot(x='type', data=filtered_df, ax=ax1)
    st.pyplot(fig1)

# Ratings
with col2:
    st.subheader("⭐ Ratings Distribution")
    fig2, ax2 = plt.subplots()
    sns.countplot(y='rating', data=filtered_df,
                  order=filtered_df['rating'].value_counts().index, ax=ax2)
    st.pyplot(fig2)

# Top Countries
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌍 Top Countries")
    fig3, ax3 = plt.subplots()
    filtered_df['country'].value_counts().head(10).plot(kind='bar', ax=ax3)
    st.pyplot(fig3)

# Top Genres
with col4:
    st.subheader("🎭 Top Genres")
    fig4, ax4 = plt.subplots()
    filtered_df['listed_in'].value_counts().head(10).plot(kind='barh', ax=ax4)
    st.pyplot(fig4)

# Content over years
st.subheader("📈 Content Added Over Years")
fig5, ax5 = plt.subplots()
filtered_df['year_added'].value_counts().sort_index().plot(ax=ax5)
st.pyplot(fig5)

# ---------------- INSIGHTS ----------------
st.subheader("📌 Key Insights")

st.write("""
- Netflix has more Movies than TV Shows  
- Most content is produced in the United States  
- Drama and International Movies dominate  
- Majority content is rated TV-MA  
- Content increased significantly after 2015  
""")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("Created by Monisha | Netflix EDA Project 🚀")
