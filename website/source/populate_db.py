from db import *
import requests, json
from SPARQLWrapper import SPARQLWrapper, JSON
URL = "https://dbpedia.org/sparql"
SEPARATOR = "|||"
MAX_SONGS = 10

query = f"""
SELECT ?song ?songName (GROUP_CONCAT(DISTINCT ?artistName; separator="{SEPARATOR}") AS ?artistNames)
       (GROUP_CONCAT(DISTINCT ?genreName; separator="{SEPARATOR}") AS ?genreNames)
       (GROUP_CONCAT(DISTINCT ?albumName; separator="{SEPARATOR}") AS ?albumNames)
       (MAX(?releaseYear) AS ?releaseYear)
WHERE {{
  ?song a dbo:Song ;
        rdfs:label ?songName ;
        dbo:artist ?artist ;
        dbo:genre ?genre ;
        dbo:album ?album .

  ?artist rdfs:label ?artistName .
  ?genre rdfs:label ?genreName .
  ?album rdfs:label ?albumName ;
         dbo:releaseDate ?releaseDate .

  # Extract the year from the release date
  BIND(year(?releaseDate) AS ?releaseYear)

  FILTER (lang(?songName) = 'en' || lang(?songName) = '')
  FILTER (lang(?artistName) = 'en' || lang(?artistName) = '')
  FILTER (lang(?genreName) = 'en' || lang(?genreName) = '')
  FILTER (lang(?albumName) = 'en' || lang(?albumName) = '')
}}
GROUP BY ?song ?songName
LIMIT {MAX_SONGS}
"""
def populate_db():
    sparql = SPARQLWrapper(URL)
    print("Setting query...")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and convert the results to JSON
    print("querying...")
    results = sparql.query()
    print(results)
    url = results.geturl()

    response = requests.get(url)
    results = response.json()

    # Parse and print the results
    for result in results["results"]["bindings"]:
        print(result)
        print(result["songName"])
        song_name = result["songName"]["value"]
        print(song_name)
        artist_names = result["artistNames"]["value"].split(SEPARATOR)
        genre_names = result["genreNames"]["value"].split(SEPARATOR)
        album_name = result["albumNames"]["value"]
        release_year = result["releaseYear"]["value"]
        add_song(song_name, artist_names, genre_names, album_name, release_year)

if __name__ == "__main__":
    answer = input("Populate DB? (y/n)")
    if answer == "y":
        populate_db()
    else:
        ...
