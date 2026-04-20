import streamlit as st
import pandas as pd
import numpy as np

# page setup
st.set_page_config(page_title="BookBestie", page_icon="📚", layout="wide")

# load the colab data
@st.cache_data
def load_data():
    # Points to the folder you downloaded
    df = pd.read_parquet("book_master_data_parquet")
    return df

df = load_data()

# ui header
st.title("BookBestie")
st.markdown("### *Find 'Under the Radar' books based on vibe, not just popularity.*")

# sidebar for the discovery filters
st.sidebar.header("Discovery Settings")
# allow user to choose number of books displayed
num_to_show = st.sidebar.slider("Number of books to show", min_value=5, max_value=100, value=10)

# sorting options (to find lower rated or niche bocks)
sort_order = st.sidebar.selectbox(
    "Sort results by:",
    options=["Highest Rated", "Lowest Rated", "Random / Discovery"]
)

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0)

# search logic
user_query = st.text_input("Describe the vibe you're looking for")

if user_query:
    keywords = user_query.lower().split()
    mask = df['description'].str.contains('|'.join(keywords), case=False, na=False)
    results = df[mask & (df['average_rating'] >= min_rating)]
    
    # apply sorting
    if sort_order == "Highest Rated":
        results = results.sort_values(by="average_rating", ascending=False)
    elif sort_order == "Lowest Rated":
        results = results.sort_values(by="average_rating", ascending=True)
    else:
        results = results.sample(frac=1) # randomize for discovery

    total_found = len(results)
    st.write(f"Found {total_found} 'Besties'. Showing the top {min(num_to_show, total_found)} based on your sort.")

    # use the user-defined num_to_show instead of a hardcoded 10
    for _, row in results.head(num_to_show).iterrows():
        with st.expander(f"{row['Title']} — ⭐ {row['average_rating']}"):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**Author(s):** {row['authors']}")
                st.write(f"**Category:** {row['categories']}")
            with col2:
                st.write("**Description:**")
                st.write(row['description'])