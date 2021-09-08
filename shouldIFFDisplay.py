from riotwatcher import LolWatcher
import numpy as np
import matplotlib.pyplot as plt

watcher = LolWatcher("RGAPI-e9a54b72-1052-49e2-8774-e9e6ce4d0d54")

class leagueStats:
# function to query winrate from riotAPI
    def winrate(region, summonerName):
# regions are currently hard coded
        if region == ('KR1' or 'RU1'):
            region = region.strip('1')
# query summoner and stats dictionaries
        summoner = watcher.summoner.by_name("na1", summonerName)
        stats = watcher.league.by_summoner("na1", summoner["id"])
        if "RANKED_SOLO_5x5" in stats[0].values():
            return round(100 * (stats[0]["wins"] / (stats[0]["wins"] + stats[0]["losses"])))
        else:
            return round(100 * (stats[1]["wins"] / (stats[1]["wins"] + stats[1]["losses"])))
# function for a player that forfeits every game predetermined to be a loss at 20 minutes
    def runSimForfeit(winrate, gain, lose):
        x = []
        y = []
        time = 0
        lp = 0
# start a loop that ends when the player hits 100 hours
        while time < 6000:
# test if game is predetermined to be a loss
            if winrate < np.random.randint(1, 101):
                lp -= lose
                time += 20
# else game is predetermined to be a win
            else:
                lp += gain
                time += np.random.randint(20, 56)
# store values to an array
            x.append(time)
            y.append(lp)
        return [x, y]
# function for a player that holds every game hostage for the chance that a predetermined loss is winnable
    def runSimHostage(winrate, winnablePercent, gain, lose):
        x = []
        y = []
        time = 0
        lp = 0
# start a loop that ends when the player hits 100 hours
        while time < 6000:
# test if the game is predetermined to be a loss
            if winrate < np.random.randint(1, 101):
# test if the predetermined loss is actually a loss
                if winnablePercent < np.random.randint(1, 101):
                    lp -= lose
                    time += 40
# else game is won
                else:
                    lp += gain
                    time += 40
# else game is predetermined to be a win
            else:
                lp += gain
                time += np.random.randint(20, 56)
# store values to an array
            x.append(time)
            y.append(lp)
        return [x, y]
# function for graphing subplots
    def graph(totalForfeit, totalHostage, totalPForfeit, totalPHostage, simCount):
        cols = 3
        rows = simCount // cols
        rows += simCount % cols
        position = range(1, simCount + 1)
        fig = plt.figure()
        fig.suptitle("{totalHours} hours were simulated to determine that you should FF if your odds of winning are less than or equal to {winnablePercent}%".format(totalHours = simCount * 1000, winnablePercent = simCount - 1))
        for i in range(simCount):
            ax = fig.add_subplot(rows, cols, position[i])
            ax.scatter(totalForfeit[i][0], totalForfeit[i][1], s = .5, c = "red", alpha = .05)
            ax.scatter(totalHostage[i][0], totalHostage[i][1], s = .5, c = "blue", alpha = .05)
            ax.plot(totalForfeit[i][0], totalPForfeit[i](totalForfeit[i][0]), c = 'red')
            ax.plot(totalHostage[i][0], totalPHostage[i](totalHostage[i][0]), c = "blue")
            ax.set_title("{i}% Winnable".format(i = i))
            ax.set_xlabel("Time (min)")
            ax.set_ylabel("LP")
            ax.legend(["Forfeit Player", "Hostage Player"])
        fig.tight_layout()
        plt.show()
# main function
    def main():
# prompt user input, regions are currently hard coded
        region = input('Region? (NA, EUW, KR, etc.) ') + '1'
        summonerName = input("Summoner Name? ")
        gain = int(input("What are your LP gains? "))
        lose = int(input("What are your LP losses? "))
        winrate = leagueStats.winrate(region, summonerName)
        totalForfeit = []
        totalHostage = []
        totalPForfeit = []
        totalPHostage = []
        maxForfeit = 0
        maxHostage = 0
        count = 0
        while maxForfeit >= maxHostage:
            simForfeit = [[],[]]
            simHostage = [[],[]]
            halfSimForfeit = [[],[]]
            halfSimHostage = [[],[]]
# run a simulation i times and plot each point generated
            for i in range(1000):
                tempForfeit = leagueStats.runSimForfeit(winrate, gain, lose)
                tempHostage = leagueStats.runSimHostage(winrate, count, gain, lose)
                for j in range(2):
                    simForfeit[j] += tempForfeit[j]
                    simHostage[j] += tempHostage[j]
# only append half the simulations to graph
                    if i % 10 == 0:
                        halfSimForfeit[j] += tempForfeit[j]
                        halfSimHostage[j] += tempHostage[j]
            totalForfeit.append(halfSimForfeit)
            totalHostage.append(halfSimHostage)
# calculate the max of each line of best fit
            zForfeit = np.polyfit(simForfeit[0], simForfeit[1],1)
            zHostage = np.polyfit(simHostage[0], simHostage[1],1)
            pForfeit = np.poly1d(zForfeit)
            pHostage = np.poly1d(zHostage)
            totalPForfeit.append(pForfeit)
            totalPHostage.append(pHostage)
            maxForfeit = pForfeit(6000)
            maxHostage = pHostage(6000)
            count += 1
# debug graphs: print("{count}: maxForfeit = {maxForfeit} | maxHostage = {maxHostage}".format(count = count, maxForfeit = maxForfeit, maxHostage = maxHostage))
        leagueStats.graph(totalForfeit, totalHostage, totalPForfeit, totalPHostage, count)
leagueStats.main()