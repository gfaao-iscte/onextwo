import requests
from bs4 import BeautifulSoup
import io
from onextwo.Dict1X2 import leagues_fte, teams, comps


class FiveThirtyEight:

    # gets all games from the leagues on leagues returning the games on a string list
    # game format is League|Date|Hour|Home Team|Away Team|Prob Home|Prob Tie| Prob Away
    def get_games_and_probs(self):

        f = io.open("readme.txt", "w", encoding="utf-32")

        results = list()

        response = requests.get('https://projects.fivethirtyeight.com/soccer-predictions/matches/')
        soup = BeautifulSoup(response.text, 'html.parser')

        games = soup.findAll(class_='sortable-tr')

        for game in games:
            if leagues_fte.__contains__(game.find(class_='league').text.strip()):
                home = game.find(class_='match').find(class_='match-top')
                away = game.find(class_='match').find(class_='match-bottom')
                league = game.find(class_='time-league').text
                game = league + "|" + \
                       home.find(class_='name').text.strip() + "|" + \
                       away.find(class_='name').text.strip() + "|" + \
                       home.find(class_='prob').text.strip() + "|" + \
                       home.find(class_='prob tie-prob').text.strip() + "|" + \
                       away.find(class_='prob').text.strip() + "|" + \
                       game.find(class_='metric').text.strip() + "|" + \
                       game.find(class_='metric').findNext().findNext().text.strip() + "|" + \
                       game.find(class_='metric').findNext().findNext().findNext().findNext().text.strip()
                game = game.replace("%", "")
                try:
                    game = game.replace(home.find(class_='name').text.strip(), teams[home.find(class_='name').text.strip()])
                except:
                        f.write(home.find(class_='name').text.strip()+"\n")

                try:
                    game = game.replace(away.find(class_='name').text.strip(), teams[away.find(class_='name').text.strip()])
                except:
                        f.write(away.find(class_='name').text.strip()+"\n")
                game = game.replace(league, comps[league])
                results.append(game)

        f.close()
        return results
