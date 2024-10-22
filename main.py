import json, os

import requests

import dotenv

class YoutubeAPIClient(object):

    def __init__(self, google_app_api_key: str):
        self.google_app_api_key = google_app_api_key
        self.url = "https://www.googleapis.com/youtube/v3/search"

    def query(self, string: str, max_results: int = 1):
        return YoutubeSearch(self, query=string, max_results=max_results)

class YoutubeSearch(object):

    def __init__(self, youtube_api_client: YoutubeAPIClient, query: str, max_results: int):
        self.client = youtube_api_client
        self.params = {
            "maxResults": max_results,
            "key": youtube_api_client.google_app_api_key,
            "q": query
        }
        self.testing_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.params and self.testing_count <= 2:
            response = requests.get(url=self.client.url, params=self.params)

            if not response.ok:
                raise Exception(response.status_code, response.text, self.params["pageToken"])

            data = response.json()

            if "nextPageToken" in data:
                self.params["pageToken"] = data["nextPageToken"]
            else:
                self.params = dict()

            self.testing_count = self.testing_count + 1

            return data["items"]
        else:
            raise StopIteration()

def main():
    client = YoutubeAPIClient(google_app_api_key=os.environ["GOOGLE_APP_API_KEY"])

    for results in client.query("mountain bike"):
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    dotenv.load_dotenv()

    main()
