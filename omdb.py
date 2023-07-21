import requests
from typing import Optional, List


class OMDBApi:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://www.omdbapi.com"


    def _images_path(self, title: str) -> Optional[str]:
        params = {
            'apikey': self.api_key,
            't': title,
            'type': 'movie',
            'r': 'json'
        }
        response = requests.get(self.url, params=params)
        movie_image = response.json()
        
        return movie_image['Poster']


    def get_posters(self, titles: List[str]) -> List[str]:
        posters = []
        for title in titles:
            path = self._images_path(title)
            if path:  # If image isn`t exist
                posters.append(path)
            else:
                posters.append('assets/none.jpeg')  # Add plug

        return posters
