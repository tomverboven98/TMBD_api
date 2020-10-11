#!/usr/bin/env python3
import json
import requests as req

# Parameters
token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzIxZTllMGNlZDE3ZGU1YTQ5ZGMwMzZlNzlmODQwOSIsInN1YiI6IjVmNzg2ODRkMzQyOWZmMDAzN2I0NjcwOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mjU3MyoGL75Y6_e-hJ-9a_X4Bn1tCxAbd0hm6nl9tZE"
#token = input("Wat is uw v4Read Access Token?: ")

# Setup header for auth.
header = {'Authorization': f'Bearer {token}',
          'Content-Type': 'application/json;charset=utf-8'}


#Search for movie.
#reference: https://developers.themoviedb.org/3/search/search-movies
#:param search: search keyword
#:param page: page number default 1
#:return: JSON response as dict
def search_movie(search, page=1):
    r = req.get(f"https://api.themoviedb.org/3/search/movie?query={search}&page={page}", headers=header)
    return json.loads(r.text)


#Loops all the pages if more than 1, else just return results dict.
#:param parsetext: Json parsed form search_movie()
#:param search: search keyword
#:return: JSON dict with all the results
def pages(parsetext, search):
    results = []
    if int(parsetext['total_pages']) > 1:
        for i in range(int(parsetext['total_pages'])):
            if i != 0:
                a = search_movie(search, i)
                results = results + a['results']
        return results
    else:
        return search_movie(search)['results']


#Get dutch genre names.
#reference: https://developers.themoviedb.org/3/genres/get-movie-list
#:return: All genre names in Dutch as dict.
def genre_names():
    r = req.get("https://api.themoviedb.org/3/genre/movie/list?language=nl-BE", headers=header)
    return json.loads(r.text)['genres']


search = input("Op welk keyword wil je zoeken ?: ")
movies = search_movie(search)
genre_name = genre_names()
movies = pages(movies, search)
for i in movies:
    # If vote_count lower than 50 don't show.
    if int(i['vote_count']) > 50:
        genres = ""
        for genre in i['genre_ids']:
            for name in genre_name:
                if name['id'] == genre:
                    genres = genres + name['name'] + " "
        print("Title: " + i['title'] + "\t\tGenre(s): " + genres + "\tuitgave: " + i['release_date'])
