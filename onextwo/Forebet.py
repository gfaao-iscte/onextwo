import re

import requests
from bs4 import BeautifulSoup

from onextwo import Dict1X2


class Forebet:

    # gets all games from the leagues on leagues returning the games on a string list
    # game format is League|Date|Hour|Home Team|Away Team|Prob Home|Prob Tie| Prob Away
    def get_games_and_odds(self):
        results = list()

        for link in Dict1X2.links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            games = soup.findAll(class_='rcnt tr_0') + soup.findAll(class_='rcnt tr_1')

            for game in games:
                try:
                    if Dict1X2.leagues.__contains__(game.find(class_='shortTag').text.strip()):
                        game = game.find(class_='date_bah').text.split(" ")[0] + "|" + \
                               game.find(class_='date_bah').text.split(" ")[1] + "|" + \
                               game.find(class_='shortTag').text + "|" + \
                               game.find(class_='homeTeam').text + "|" + \
                               game.find(class_='awayTeam').text + "|" + \
                               game.find(class_='fprc').findNext().text + "|" + \
                               game.find(class_='fprc').findNext().findNext().text + "|" + \
                               game.find(class_='fprc').findNext().findNext().findNext().text
                        results.append(game)
                except:
                    # print("Featured Macth:"+game.find(class_='homeTeam').text+"|"+game.find(class_='awayTeam').text)
                    pass
        return results

    def close_games(self,games):
        results= list()
        for game in games:
            link= Dict1X2.leagues_to_links[game.league]

            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')

            fb_game=soup.find(text=re.compile(game.home))
            s=fb_game.parent.parent.parent.parent.parent.parent
            div=fb_game.parent.parent.parent.parent.parent.parent.text
            if div.__contains__("FT") and div.__contains__(game.home) and  div.__contains__(game.away) and  div.__contains__(game.date):
                res=s.find(class_='l_scr').text.split(" - ")
                if int(res[0]) > int(res[1]):
                    game.result="1"
                elif int(res[0]) < int(res[1]):
                    game.result="2"
                else:
                    game.result="X"
            if game.result == game.bet:
                game.won="1"
            else:
                game.won="0"
            if game.result is not None:
                results.append(game)
        return results