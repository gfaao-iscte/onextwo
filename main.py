from onextwo.FiveThirtyEight import FiveThirtyEight
from onextwo.Forebet import Forebet
from onextwo.Game import Game
import pymongo
from pymongo import MongoClient

cluster=MongoClient("mongodb+srv://clt:1235@cluster0.qr3in.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["onextwo"]
collection_opengames=db["opengames"]

def main():



    print("___FootballBot___")
    while True:
        menu()
        option = int(input("Selected Option: "))
        if option == 0:
            break
        if option == 2:
            opengames=getGamesAndOdds()
            insertOpenGames(opengames)
    print("________\nGoodbye\n________")


def menu():
    print("Choose an option:")
    print("1.Get today's games and odds")
    print("2.Update games and results")
    print("3.Check Stats")
    print("0.Exit")


def getGamesAndOdds():
    games = list()
    results = list()
    fb = Forebet()
    fte = FiveThirtyEight()
    results_fb = fb.get_games_and_odds()
    results_fte = fte.get_games_and_probs()
    for game_fb in results_fb:
        game_fb = game_fb.split("|")
        game = Game(game_fb[3], game_fb[4], game_fb[0], game_fb[1], game_fb[2])
        game.setFBodds(game_fb[5], game_fb[6], game_fb[7])
        games.append(game)

    for game in games:
        try:
            for i, s in enumerate(results_fte):
                if game.getHome() in s and game.getAway() in s and game.getLeague() in s:
                    game_fte = results_fte[i].split("|")
                    game.set538odds(game_fte[3], game_fte[4], game_fte[5], game_fte[6], game_fte[7], game_fte[8])
                    game.setOddsAndBet()
                    results_fte.pop(i)
                    if (int(game.betOddP) > 49) and (int(game.i538rating) > 40):
                        print(game.gameToString())
                    results.append(game)
                    break

        except:
            print("Not Found")

    return results

def insertOpenGames(opengames):
    #collection_opengames.delete_many({})
    for game in opengames:
        db_game_id=None
        try:
            db_game_id=collection_opengames.find_one({"date":game.date,
                                                      "hour":game.hour,
                                                      "league":game.league,
                                                      "home":game.home,
                                                      "away":game.away}).get('_id')
        except:
            pass
        if db_game_id is None:
            collection_opengames.insert_one({"date":game.date,
                                                 "hour":game.hour,
                                                 "league":game.league,
                                                 "home":game.home,
                                                 "away":game.away,
                                                 "homeFB": game.homeFBodd,
                                                 "drawFB":game.drawFBodd,
                                                 "awayFB":game.awayFBodd ,
                                                 "home538":game.home538odd ,
                                                 "draw538":game.draw538odd ,
                                                 "away538":game.away538odd ,
                                                 "quality":game.i538quality,
                                                 "importance":game.i538importance ,
                                                 "rating":game.i538rating ,
                                                 "homeOdd":game.homeOdd ,
                                                 "drawOdd":game.drawOdd ,
                                                 "awayOdd":game.awayOdd ,
                                                 "bet":game.bet ,
                                                 "betOdd":game.betOdd ,
                                                 "betOddP":game.betOddP
                                                 })

main()
