#!/usr/bin/env python3
import urllib.request
import requests

def main():
    pokenum= input("Pick a number between 1 and 151!\n>")
    pokeapi= requests.get("https://pokeapi.co/api/v2/pokemon/" + pokenum).json()

    #print(pokeapi)
    #sprites front default
    sprites_f_d = pokeapi['sprites']['front_default']
    print(sprites_f_d)
#    urllib.request.urlretrieve("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
    filename = '/home/student/static/{}.png'.format(pokenum)
    urllib.request.urlretrieve(sprites_f_d, filename)
    #move names
    apimoves = pokeapi['moves']
    movelist = []
    for move in apimoves:
        #print(move)
        movename = move['move']['name']
        movelist.append(movename)
    apimoveS = sorted(apimoves, key =lambda x: x.get('move').get('name'))
    movelist2 = [d.get('move').get('name') for d in apimoveS]
    print("alt method")
    print(movelist2)
    
    print(movelist)

    #countgameappearnce
    gamecount= len(pokeapi['game_indices'])
    print(gamecount)
    #for 

main()

