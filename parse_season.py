import parse
str_data="Stargate.SG1-s01e01e23.Children.of.the.Gods-part.1&2e14"

import re
t=re.findall(r"[Ss](\d+)",str_data)
#print(t)
print("season")
print(t)
t=re.findall(r"[Ee](\d+)",str_data)
print("episodes")
print(t)

from imdb import IMDb

# create an instance of the IMDb class
ia = IMDb()

# get a movie and print its director(s)
the_matrix = ia.search_movie('Stargate SG1  The Enemy Within')
for movie in the_matrix:
    print(movie["title"])
    print(movie.movieID)
    mv=ia.get_movie(movie.movieID)
    for key in mv.current_info:
        try:
            print(mv[key])
        except Exception as e:
            print("except"+str(e))
            pass
    print()
