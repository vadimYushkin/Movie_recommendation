from typing import List, Set
import pandas as pd

from .utils import parse
from typing import Optional, List

class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance = pd.read_csv(distance_filepath, index_col='movie_id')
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return set(genres)
    def get_years(self) -> Set[str]:
        self.movies['release_date'] = pd.to_datetime(self.movies['release_date'], format = '%Y-%m-%d')
        self.movies["year"] = self.movies["release_date"].dt.year
        self.movies['year'] = self.movies['year']. fillna(2000)
        year = self.movies["year"]
        year = year.astype(int)
        return set(year.unique())

    def recommendation(self, title: str, top_k: int ) -> List[str]:
        """
        Returns the names of the top_k most similar movies with the movie "title"
        """
        title_id = self.movies.index[self.movies['title'] == title].item()
        movie_id = self.movies['movie_id'].astype(int)
        # comparison with dataset distance
        cos_columns = [i for i in movie_id if i in self.distance.columns]
        cos_simFiltred = self.distance.loc[:, cos_columns]
        # row in title movie
        row = cos_simFiltred.loc[title_id]
        similarity_scores = [(column, value) for column, value in row.items()]

        # Sort the movies ASC
        sig_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        # Scores of the top_k most similar movies
        sig_scores = sig_scores[1:top_k + 1]
        # Movie indices
        movie_indices = [i[0] for i in sig_scores]
        topMovies = self.movies.loc[movie_indices, 'title'].values.tolist()

        return topMovies



    def recommendation_genre_year(self, title: str, genres: str, year: int,  top_k: int ) -> List[str]:

        # creating a dataset with the selected genre and year
        self.movies['release_date'] = pd.to_datetime(self.movies['release_date'], format='%Y-%m-%d')
        self.movies["year"] = self.movies["release_date"].dt.year
        self.movies['year'] = self.movies['year'].fillna(2000)
        self.movies['year'].astype(int)
        # selection by genre
        self.movies["genresstr"] = self.movies["genres"].apply(lambda x: f'"{x}"')
        self.movies["OneTwo"] = self.movies["genresstr"].apply(lambda x: 1 if genres in x else 0)
        movies_genres = self.movies[self.movies["OneTwo"] == 1]
        movie_selection = movies_genres.loc[(self.movies['year'] == year)]
        idx = self.movies[self.movies['title'] == title]
        # id title movie
        idx_id = idx['movie_id']
        id_title = idx.iloc[0]['movie_id']
        movie_selection_id = movie_selection['movie_id']
        # comparison with dataset dist_new
        dist_copy = self.distance.copy()
        dist_new = dist_copy.loc[movie_selection_id]
        if (movie_selection['movie_id'].eq(id_title)).any() == False:
            movie_selection_idx = pd.concat([movie_selection_id, idx_id])
            dist_new = dist_copy.loc[movie_selection_idx]

        sig_scores = dist_new[idx_id].sort_values(by=id_title, ascending=False)
        sig_scores_loc = sig_scores.iloc[1:top_k+1, :]

        movie_indices = sig_scores_loc.index.to_list()
        top = movie_selection.loc[movie_selection['movie_id'].isin(movie_indices)]
        topMovies = top['title'].to_list()
        return topMovies