import csv
import json

# dictionary that will store movie info
movies_info = {}

# read file containing movie info, genres
with open('movies.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movie_id = row["movieId"]
        genres = row["genres"].split("|")
        row["genres"]  = genres
        try:
            row["year"] = int(row["title"].strip()[-5:-1])
        except:
            print ("Failed to parse year from {} ".format(row["title"]))
            pass
        movies_info[movie_id] = dict(row)

# store imdbId and tmdbId        
with open('links.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movie_id = row["movieId"]
        movies_info[movie_id].update(dict(row))

# store count of ratings
with open('ratings.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movie_id = row["movieId"]
        movies_info[movie_id]["numRatings"] =  movies_info[movie_id].get("numRatings",0)+1

# store unique tags associated with movie        
with open('tags.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movie_id = row["movieId"]
        tags = movies_info[movie_id].get("tags",set())
        tags.add(row["tag"])
        movies_info[movie_id]["tags"]=tags
    for (movie_id,movie_info) in movies_info.items():
        if "tags" in movie_info:
            movie_info["tags"] = list(movie_info["tags"])

# save movie info in json new line format            
with open('movies.json', 'w') as outfile:
    for movie in movies_info.values():
        json.dump(movie, outfile)
        outfile.write('\n')            