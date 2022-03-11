class Game:

    def __init__(self, home, away, date, hour, league):
        self.home = home
        self.away = away
        self.date = date
        self.hour = hour
        self.league = league
        self.homeFBodd = None
        self.drawFBodd = None
        self.awayFBodd = None
        self.home538odd = None
        self.draw538odd = None
        self.away538odd = None
        self.i538quality = None
        self.i538importance = None
        self.i538rating = None
        self.homeOdd = None
        self.drawOdd = None
        self.awayOdd = None
        self.bet = None
        self.betOdd = None
        self.betOddP = None
        self.result = None
        self.won=None

    def setFBodds(self, homeFBodd, drawFBodd, awayFBodd):
        self.homeFBodd = homeFBodd
        self.drawFBodd = drawFBodd
        self.awayFBodd = awayFBodd

    def set538odds(self, home538odd, draw538odd, away538odd, i538quality, i538importance, i538rating):
        self.home538odd = home538odd
        self.draw538odd = draw538odd
        self.away538odd = away538odd
        self.i538quality = i538quality
        self.i538importance = i538importance
        self.i538rating = i538rating

    def setOddsAndBet(self):
        try:
            self.homeOdd = str((int((float(self.homeFBodd) + float(self.home538odd)) / 2)))
            self.drawOdd = str((int((float(self.drawFBodd) + float(self.draw538odd)) / 2)))
            self.awayOdd = str((int((float(self.awayFBodd) + float(self.away538odd)) / 2)))
            if (float(self.homeOdd) >= float(self.drawOdd)) and (float(self.homeOdd) >= float(self.awayOdd)):
                self.bet = "1"
                self.betOddP = str((int((float(self.homeFBodd) + float(self.home538odd)) / 2)))
                self.betOdd = str(1 / (float(self.homeOdd) / 100))
            elif (float(self.homeOdd) < float(self.drawOdd)) and (float(self.drawOdd) >= float(self.awayOdd)):
                self.bet = "X"
                self.betOddP = str((int((float(self.drawFBodd) + float(self.draw538odd)) / 2)))
                self.betOdd = str(1 / (float(self.drawOdd) / 100))
            else:
                self.bet = "2"
                self.betOddP = str((int((float(self.awayFBodd) + float(self.away538odd)) / 2)))
                self.betOdd = str(1 / (float(self.awayOdd) / 100))
            self.betOdd = str(round(float(self.betOdd), 2))
        except:
            print(self.home+"VS"+self.away)
            print(self.homeFBodd)
            print(self.awayFBodd)
            print(self.away538odd)

    def gameToList(self):
        return list(self.date, self.hour, self.league, self.home, self.away,
                    self.homeFBodd, self.drawFBodd,
                    self.awayFBodd, self.home538odd, self.draw538odd,
                    self.away538odd, self.homeOdd, self.drawOdd,
                    self.awayOdd, self.i538quality, self.i538importance,
                    self.i538rating, self.bet, self.betOddP,
                    self.betOdd)

    def gameToString(self):
        return str(
            self.date + "|" + self.hour + "|" + self.league + "|" +
            self.home + "|" + self.away + "|" + self.bet + "|" +
            self.betOddP + "%" + "|" + self.i538rating + "|" + self.betOdd)

    def setResult(self):
        pass

    def getHome(self):
        return self.home

    def getAway(self):
        return self.away

    def getLeague(self):
        return self.league

    @staticmethod
    def test():
        game1 = Game("Estoril", "Arouca", "1/27/2022", "20:15", "Pt1")
        game1.setFBodds(str(46), str(35), str(19))
        game1.set538odds(str(48), str(25), str(27), str(44), str(27), str(35))
        game1.setOddsAndBet()
        print(game1.gameToString())
