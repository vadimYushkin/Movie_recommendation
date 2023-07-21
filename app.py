import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.no_default_selectbox import selectbox
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)


recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE,
)
def main() -> None:
    st.markdown("<h1 style='text-align: center; color: red;'>Movie Recommender Service</h1>",
    unsafe_allow_html=True)
    st.sidebar.image('https://newsib.net/wp-content/uploads/2022/11/1619602660_3-phonoteka_org-p-kinematograf-fon-3-700x433.jpg')
    st.sidebar.image('https://static.javatpoint.com/fullformpages/images/imdb.png')
    st.sidebar.markdown(
        """<h5 style='text-align: center; color: black;'>Free service  </h5>""",
        unsafe_allow_html=True)
if __name__ == "__main__":
    st.set_page_config(
        "Account by Vadim Yushkin",
        "📊",
        initial_sidebar_state="expanded",
        layout="wide")
    main()
st.write("""
    This app allows you to show recommended movies by description, genre and year production.
    """)
selected_movie = st.selectbox("Select a movie you like :",
    recsys.get_title())
selected_genre = selectbox("Select an genre:", recsys.get_genres(),
    no_selection_label="<None>")
selected_year = selectbox("Select year:", recsys.get_years(),
    no_selection_label="<None>")
if st.button('Show Recommendation', help='Click it'):
    st.write("Recommended Movies:")
    if selected_genre == None or selected_year == None:
        recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
        recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
        movies_col = st.columns(TOP_K)
        for index, col in enumerate(movies_col):
            with col:
                st.subheader(recommended_movie_names[index])
                st.image(recommended_movie_posters[index])
    else:
        recommended_movie_names: list[str] = recsys.recommendation_genre_year(selected_movie, selected_genre,
                                                                              selected_year, top_k=TOP_K)
        if len(recommended_movie_names) == 0:
            st.subheader("Couldn't find suitable movies")
        else:
            if len(recommended_movie_names) < 5:
                top_k = len(recommended_movie_names)
            else:
                top_k = TOP_K
            recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)
            movies_col = st.columns(top_k)
            for index, col in enumerate(movies_col):
                with col:
                    st.subheader(recommended_movie_names[index])
                    st.image(recommended_movie_posters[index])

st.markdown(
    "<h5 style='text-align: center; color: red;'>Novosibirsk,Russia 2023</h5>",
    unsafe_allow_html=True
)