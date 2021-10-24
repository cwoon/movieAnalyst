import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

main_url = 'https://www.mypianku.net/mv/----score-9-{}.html'
directory = r'C:\Users\User\Desktop\webscraping'
movieList = []
ratingList = []
yearList = []
countryList = []
categoryList = []
categoryListFull = []
booleanList = []

def getMovieDetail(movie):
    for x in movie:
        movieName = x.find('a')
        movieList.append(movieName.text.strip())
        rating = x.find('span')
        ratingList.append(rating.text.strip())

def getTag(tags):
    for y in tags:
        tag = y.text.split('/')
        yearList.append(tag[0].strip())
        countryList.append(tag[1].strip())
        category = [str.strip() for str in tag[2:]]
        categoryListFull.append(category)

        for item in category:
            if item not in categoryList:
                categoryList.append(item)

def getBooleanList(l1, l2):
    for i in range(len(l2)):
        l3 = []
        for j in range(len(l1)):
            if l1[j] in l2[i] :
                l3.append(True)
            else:
                l3.append(False)
        booleanList.append(l3)

for i in range(1, 11):
    url = main_url.format(i)
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'lxml')
    movies = bs.find_all("ul" , class_ = 'content-list')

    for i in range(0, len(movies)):
        movie = movies[i].find_all('h3')
        tags = movies[i].find_all('div', class_ = 'tag')

    getMovieDetail(movie)
    getTag(tags)

df = pd.DataFrame(
    {
     'Movie': movieList,
     'Year': yearList,
     'Country': countryList,
     'Rating': ratingList,
    })
df.to_csv(os.path.join(directory,r'movie.txt'), index=False)

getBooleanList(categoryList, categoryListFull)
dictionary = dict(zip(list(range(0,len(booleanList))), booleanList))
df2 = pd.DataFrame.from_dict(dictionary, orient='index', columns= categoryList)
df2['Movie'] = movieList
df_melted = pd.melt(df2, id_vars = ['Movie'], var_name = 'Category', value_name = 'Boolean')
df_cleaned = df_melted[df_melted['Boolean'] == True]
df_cleaned.to_csv(os.path.join(directory,r'category.txt'), index=False)