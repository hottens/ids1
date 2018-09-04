import csv
import re
import urllib, json

def validTitle(title):
	if len(title)==0: return False
	regex = r"^[0-9a-zA-Z:\-']*$"
	if re.search(regex, title): return True
	return False

def validDate(date):
	return len(date.split('/'))==3

def valid(row):
	return validTitle(row["Title"]) and validDate(row["ReleaseDate"])
	

with open("movievalue.csv") as f:
    reader = csv.DictReader(f)
    data = {}
    for row in reader:
        if(valid(row)):
		data[row["Title"]] = {}
		data[row["Title"]]["CSV"] = row

def getOMDBURL(title, year):
	return "http://www.omdbapi.com/?t="+title+"&y="+year+"&apikey=e121dcf3" 

def getTMDBURL(title, year):
	return "https://api.themoviedb.org/3/search/movie?api_key=3ce50e41bbff335a1a1a7a054f2b141b&language=en-US&query="+title+"&page=1&include_adult=false&primary_release_year="+year

genreById = {}
def getGenres():
	genreTMDBURL = "https://api.themoviedb.org/3/genre/movie/list?api_key=3ce50e41bbff335a1a1a7a054f2b141b&language=en-US"
	genresTMDBResult = urllib.urlopen(genreTMDBURL)
	genres = json.loads(genresTMDBResult.read())["genres"]

	for genre in genres:
		genreById[genre["id"]] = genre["name"]
getGenres()
x = 0
for title, values in data.items():
	csv = values["CSV"]

	# Get from TMDB
	day,month,year = csv["ReleaseDate"].split("/")
	responseTMDB = urllib.urlopen(getTMDBURL(title,year))
	resultTMDB = json.loads(responseTMDB.read())
	for r in resultTMDB["results"]:
		if r["title"]==title or r["original_title"]==title: 
			# Add genres			
			r["genres"] = []
			for g in r["genre_ids"]:
				r["genres"].append(genreById[g])
			values["TMDB"] = r

	# Get from OMDB
	responseOMDB = urllib.urlopen(getOMDBURL(title,year))
	resultOMDB = json.loads(responseOMDB.read())
	values["OMDB"] = resultOMDB

# Save extended dict
with open('moviedata.txt', 'w') as file:
     file.write(json.dumps(data)) # use `json.loads` to do the reverse
