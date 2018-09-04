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
    data = []
    for row in reader:
        if(valid(row)): data.append(row)

def getURL(title, year):
	return "https://api.themoviedb.org/3/search/movie?api_key=3ce50e41bbff335a1a1a7a054f2b141b&language=en-US&query="+title+"&page=1&include_adult=false&primary_release_year="+year

genreById = {}
def getGenres():
	genreURL = "https://api.themoviedb.org/3/genre/movie/list?api_key=3ce50e41bbff335a1a1a7a054f2b141b&language=en-US"
	genresResult = urllib.urlopen(genreURL)
	genres = json.loads(genresResult.read())

	for genre in genres:
		genreById[genre["id"]] = genre["name"]
getGenres()
x = 0
for d in data:
	title = d["Title"]
	day,month,year = d["ReleaseDate"].split("/")
	response = urllib.urlopen(getURL(title,year))
	print getURL(title,year)
	result = json.loads(response.read())
# Genre, imdbRating, imdbVotes (and optional also Director, Country, PG rating, etc.)
	for r in result["results"]:
		if r["title"]==title or r["original_title"]==title: #print r
			d["genres"] = []
			for g in r["genre_ids"]:
				d["genres"].append(genreById[g])
	print d
			
	x+=1
	if x>3: break