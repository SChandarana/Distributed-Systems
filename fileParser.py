import csv

#initialising the dictionaries

movies = {}
ratings = {}
movieInfo = {}
#reading in all the data from movielens
with open("movies.csv",encoding="utf-8") as file:
    reader = csv.reader(file, delimiter = ",")
    for line in reader:
        if line[0].isdigit(): #ignore first row
            movie = line[1][:-7] #get movie title
            year = line[1][-6:] #get movie year
            #print([movie,year,line[2]]) 
            if line[0] not in movies:
                movies[line[0]] = movie #add movieID: movie
                movieInfo[movie] = [year,line[2]] #add movie: [year,genre]

with open("ratings.csv",encoding="utf-8") as file:
 
    reader = csv.reader(file, delimiter = ",")
    for line in reader:
        if line[0].isdigit(): #ignore first row
            movie = movies[line[1]] #get movie title using movie id
            if movie not in ratings:
                ratings[movie] = {line[0]:float(line[2])} #start dictionary of ratings for movie
            else:
                ratings[movie][line[0]] = float(line[2])
    
              
