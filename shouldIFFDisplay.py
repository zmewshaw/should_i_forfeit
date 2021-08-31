from riotwatcher import LolWatcher
import numpy as np
import matplotlib.pyplot as plt

watcher = LolWatcher("RGAPI-741e14e0-ea7e-4439-a05a-ad4e4bc1bdf2")

class leagueStats:
    def winrate(summonerName):
        summoner = watcher.summoner.by_name("na1", summonerName)
        stats = watcher.league.by_summoner("na1", summoner["id"])
        return round(100 * (stats[0]["wins"] / (stats[0]["wins"] + stats[0]["losses"])))
# function for a player that forfeits every game predetermined to be a loss at 20 minutes
    def runSimForfeit(winrate, gain, lose):
        x = []
        y = []
        time = 0
        lp = 0
# start a loop that ends when the player hits 100 hours
        while time < 6000:
# test if game is predetermined to be a loss
            if winrate < np.random.randint(1,101):
                lp -= lose
                time += 20
# else game is predetermined to be a win
            else:
                lp += gain
                time += np.random.randint(20,56)
# store values to an array
            x.append(time)
            y.append(lp)
        return [x,y]
# function for a player that holds every game hostage for the chance that a predetermined loss is winnable
    def runSimHostage(winrate,winnablePercent,gain,lose):
        x = []
        y = []
        time = 0
        lp = 0
# start a loop that ends when the player hits 100 hours
        while time < 6000:
# test if the game is predetermined to be a loss
            if winrate < np.random.randint(1,101):
# test if the predetermined loss is actually a loss
                if winnablePercent < np.random.randint(1,101):
                    lp -= lose
                    time += 40
# else game is won
                else:
                    lp += gain
                    time += 40
# else game is predetermined to be a win
            else:
                lp += gain
                time += np.random.randint(20,56)
# store values to an array
            x.append(time)
            y.append(lp)
        return [x,y]
# function for graphing subplots
    def graph(totalForfeit, totalHostage, totalPForfeit, totalPHostage, simCount):
        cols = 3
        count = 0
        rows = simCount // cols
        rows += simCount % cols
        position = range(1, simCount + 1)
        print("position = " + str(position))
        fig = plt.figure()
        fig.suptitle("Results: (only 1 in 10 simulations are displayed)")
        for i in range(simCount):
            ax = fig.add_subplot(rows, cols, position[i])
            ax.scatter(totalForfeit[i][0], totalForfeit[i][1], s = .5, c="red", alpha = .05)
            ax.scatter(totalHostage[i][0], totalHostage[i][1], s = .5, c="blue", alpha = .05)
#            ax.plot(totalPForfeit[i], c="red")
#            ax.plot(totalPHostage[i], c="blue")
        print(totalPForfeit)
        print(totalPHostage)
        plt.show()

#        fig.subplots_adjust(hspace = 1)
#        for i in range():
#            for j in range(cols):
#                axs[i, j].scatter(totalForfeit[i][0], totalForfeit[i][1], s = .5, c="red", alpha = .1)
#                axs[i, j].scatter(totalHostage[i][0], totalHostage[i][1], s = .5, c="blue", alpha = .1)
#                axs[i, j].plot(totalPForfeit[i], c="red")
#                axs[i, j].plot(totalPHostage[i], c="blue")
#                axs[i, j].set_title("{count}% Winnable".format(count = count))
#                count += 1

# main function
    def main():
# prompt user input
        summonerName = input("Summoner Name? ")
        gain = int(input("What are your LP gains? "))
        lose = int(input("What are your LP losses? "))
        winrate = leagueStats.winrate(summonerName)
        print("winrate = " + str(winrate))
        totalForfeit = []
        totalHostage = []
        totalPForfeit = []
        totalPHostage = []
        maxForfeit = 0
        maxHostage = 0
        count = 0
        print("Simulating games")
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
            print("{count}: maxForfeit = {maxForfeit} | maxHostage = {maxHostage}".format(count = count, maxForfeit = maxForfeit, maxHostage = maxHostage))
        leagueStats.graph(totalForfeit, totalHostage, totalPForfeit, totalPHostage, count)
        print("{totalHours} hours were simulated to determine that you should FF unless your game is winnable {winnablePercent}% of the time".format(totalHours = count * 100, winnablePercent = count))
leagueStats.main()