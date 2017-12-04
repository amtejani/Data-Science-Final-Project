import requests
import json
import pandas as pd
from urllib.request import urlretrieve
from os.path import isfile

url = 'https://api.themoviedb.org/3/discover/movie?api_key=3b6df7438e6ca12251c94739d6c3d594&language=en-US&page={}&with_keywords=10183'
img = 'https://image.tmdb.org/t/p/w500'
meta = 'https://api.themoviedb.org/3/movie/{}?api_key=3b6df7438e6ca12251c94739d6c3d594&language=en-US'
credits = 'https://api.themoviedb.org/3/movie/{}/credits?api_key=3b6df7438e6ca12251c94739d6c3d594'
actor_pop = 'https://api.themoviedb.org/3/person/{}?api_key=3b6df7438e6ca12251c94739d6c3d594&language=en-US'

def get_id():
    id = []
    for i in range(1,163):
        success = False
        while not success:
            res = requests.get(url.format(i))
            print(url.format(i))
            jData = json.loads(res.text)
            print(jData)
            if not 'status_code' in jData:
                success = True
                for j in jData['results']:
                    id.append(j['id'])
    return id

def get_imgs(df):
    imgs = ['poster','backdrop']
    for i in imgs:
        s = i + '_path'
        for j in df[s]:
            if(type(j) == str ):
                print(type(j))
                u = img + j
                a = 'data/'+ i + j
                print(u)
                if(not isfile(a)):
                    urlretrieve(u, a)

def get_metadata(id):
    movies = []
    for i in id:
        success = False
        while not success:
            res = requests.get(meta.format(i))
            print(meta.format(i))
            jData = json.loads(res.text)
            if not 'status_code' in jData:
                movies.append(jData)
                success = True
    d = pd.DataFrame(movies)
    d = d.set_index('id')
    print(d)
    d.to_csv('data/mov.csv')

def get_credits(id):
    credits_arr = []
    if isfile('data/credits.csv'):
        c = pd.read_csv('data/credits.csv')
        id = set(id) - set(c['id'].values)
    try:
        for i in id:
            success = False
            while not success:
                res = requests.get(credits.format(i))
                print(credits.format(i))
                jData = json.loads(res.text)
                if not 'status_code' in jData:
                    credits_arr.append(jData)
                    success = True
    finally:
        d = pd.DataFrame(credits_arr)
        if isfile('data/credits.csv'):
            c = pd.read_csv('data/credits.csv')
            c = c.append(d)
            d.to_csv('data/credits.csv')
        else:
            d = d.set_index('id')
            print(d)
            d.to_csv('data/credits.csv')

def get_actor_popularity(id):
    actors = set()
    directors = []
    producers = []
    if isfile('data/movie_actors.csv'):
        c = pd.read_csv('data/movie_actors.csv',index_col=0)
        print(c.values[:,0])
        actors = set(c.values[:,0])
    else:
        try:
            for i in id[:5]:
                success = False
                while not success:
                    res = requests.get(credits.format(i))
                    print(credits.format(i))
                    jData = json.loads(res.text)
                    if not 'status_code' in jData:
                        for j in jData['cast']:
                            actors.add(j['id'])
                        success = True
        finally:
            pd.Series(list(actors)).to_csv('data/movie_actors.csv')


    popularities = []
    # if isfile('data/actors.csv'):
    #     d = pd.read_csv('data/actors.csv',index_col='id')
        
    #     actors = actors - set(d.index.values)
    try:
        for i in actors:
            success = False
            while not success:
                res = requests.get(actor_pop.format(i))
                print(actor_pop.format(i))
                jData = json.loads(res.text)
                if not 'status_code' in jData:
                    popularities.append([i,jData['popularity']])
                    success = True
    finally:
        d = pd.DataFrame(popularities)
        d.to_csv('data/actors.csv',index=False)
        print(d)


if __name__ == "__main__":
    # id = get_id()
    # df = pd.read_csv('data/movies.csv')
    # id = df['id'].values
    # print(id)
    # get_metadata(id)
    df = pd.read_csv('data/mov.csv')
    id = df['id'].values
    # get_credits(id)
    # get_imgs(df)
    get_actor_popularity(id)
