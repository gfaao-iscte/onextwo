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


