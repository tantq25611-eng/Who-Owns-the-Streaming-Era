import streamlit as st
import pandas as pd


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Who Owns the Streaming Era?",
    page_icon="🎧",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    artist = pd.read_csv("data/artist_ranking.csv")
    genre = pd.read_csv("data/genre_ranking.csv")
    country = pd.read_csv("data/country_ranking.csv")
    country_artist = pd.read_csv("data/country_artist_top5.csv")

    return artist, genre, country, country_artist


artist, genre, country, country_artist = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("🎧 Who Owns the Streaming Era?")

st.markdown(
    """
    **A data-driven look at who dominates Spotify streaming —
    across artists, genres and markets.**
    """
)

st.divider()


# =========================================================
# SECTION 1 — ARTIST DOMINANCE
# =========================================================

st.header("👑 Who Owns the Streaming Era?")

# Find dominance score column
dominance_col = None

for col in artist.columns:
    if col.lower().replace(" ", "_") in [
        "dominance_score",
        "dominance"
    ]:
        dominance_col = col
        break

if dominance_col is not None:

    top_artists = (
        artist
        .sort_values(dominance_col, ascending=False)
        .head(10)
        .copy()
    )

    st.subheader("Top 10 Artists by Dominance Score")

    st.bar_chart(
        top_artists.set_index("artist")[dominance_col]
    )

    winner = top_artists.iloc[0]["artist"]
    score = top_artists.iloc[0][dominance_col]

    st.success(
        f"🏆 **{winner}** is the leading artist with a "
        f"Dominance Score of **{score:.2f}**."
    )

else:
    st.warning("Dominance Score column was not found.")


# =========================================================
# SECTION 2 — STREAMING POWER
# =========================================================

st.divider()

st.header("💿 The Streaming Powerhouse")

# Detect stream column
stream_col = None

for col in artist.columns:
    if col.lower().replace(" ", "_") == "total_streams":
        stream_col = col
        break

if stream_col is not None:

    top_streams = (
        artist
        .sort_values(stream_col, ascending=False)
        .head(10)
        .copy()
    )

    st.subheader("Top 10 Artists by Attributed Streams")

    st.bar_chart(
        top_streams.set_index("artist")[stream_col]
    )

    st.caption(
        "Streams are attributed across artists on multi-artist tracks "
        "to reduce double-counting."
    )


# =========================================================
# SECTION 3 — GENRE
# =========================================================

st.divider()

st.header("🎵 What Does the World Listen To?")

genre_stream_col = None

for col in genre.columns:
    if col.lower().replace(" ", "_") == "total_streams":
        genre_stream_col = col
        break

if genre_stream_col is not None:

    top_genres = (
        genre
        .sort_values(genre_stream_col, ascending=False)
        .head(10)
        .copy()
    )

    st.subheader("Top 10 Genres by Attributed Streams")

    st.bar_chart(
        top_genres.set_index("genre")[genre_stream_col]
    )


# =========================================================
# SECTION 4 — COUNTRY
# =========================================================

st.divider()

st.header("🌎 Where Does the Streaming Power Come From?")

country_stream_col = None

for col in country.columns:
    if col.lower().replace(" ", "_") == "total_streams":
        country_stream_col = col
        break

if country_stream_col is not None:

    top_countries = (
        country
        .sort_values(country_stream_col, ascending=False)
        .head(10)
        .copy()
    )

    st.subheader("Top 10 Spotify Markets by Streams")

    st.bar_chart(
        top_countries.set_index("country")[country_stream_col]
    )


# =========================================================
# SECTION 5 — COUNTRY × ARTIST
# =========================================================

st.divider()

st.header("🗺️ Who Owns Each Market?")

countries = sorted(
    country_artist["country"].dropna().unique()
)

selected_country = st.selectbox(
    "Select a market",
    countries
)

selected_data = (
    country_artist[
        country_artist["country"] == selected_country
    ]
    .sort_values("rank")
    .copy()
)

st.subheader(
    f"Top 5 Artists in {selected_country.upper()}"
)

st.dataframe(
    selected_data[
        [
            "rank",
            "artist",
            "total_streams",
            "chart_appearances",
            "avg_position"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# Chart for selected country

st.bar_chart(
    selected_data.set_index("artist")["total_streams"]
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Data source: Spotify Charts dataset (2013–2023). "
    "Analysis performed using PySpark."
)
