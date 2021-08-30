from riotwatcher import LolWatcher
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as plb

watcher = LolWatcher('RGAPI-741e14e0-ea7e-4439-a05a-ad4e4bc1bdf2')

class leagueStats:
    def winrate(summonerName):
        summoner = watcher.summoner.by_name('na1',summonerName)
        stats = watcher.league.by_summoner('na1',summoner['id'])
        return round(100*(stats[0]['wins']/(stats[0]['wins']+stats[0]['losses'])))
# function for a player that forfeits every game predetermined to be a loss at 20 minutes
    def runSimForfeit(winrate,gain,lose):
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
    def main():
# prompt user input
        summonerName = input('Summoner Name? ')
        gain = int(input('What are your LP gains? '))
        lose = int(input('What are your LP losses? '))
        winrate = leagueStats.winrate(summonerName)
# run a simulation i times and plot each point generated
        totalForfeit = [[],[]]
        totalHostage = [[],[]]
        graphsForfeit = []
        graphsHostage = []
        maxForfeit = 0
        maxHostage = 0
        winnablePercent = 0
        count = 0
        print('Simulating games')
        while maxForfeit >= maxHostage:
            totalForfeit = [[],[]]
            totalHostage = [[],[]]
            for i in range(100):
                tempForfeit = leagueStats.runSimForfeit(winrate,gain,lose)
                tempHostage = leagueStats.runSimHostage(winrate,winnablePercent,gain,lose)
#                plt.scatter(tempForfeit[0],tempForfeit[1],c='red',s=1,alpha=.1)
#                plt.scatter(tempHostage[0],tempHostage[1],c='blue',s=1,alpha=.1)
# store values for line of best fit
                for j in range(2):
                    totalForfeit[j] += tempForfeit[j]
                    totalHostage[j] += tempHostage[j]
# create and draw lines of best fit
            zForfeit = np.polyfit(totalForfeit[0],totalForfeit[1],1)
            zHostage = np.polyfit(totalHostage[0],totalHostage[1],1)
            pForfeit = np.poly1d(zForfeit)
            pHostage = np.poly1d(zHostage)
            maxForfeit = pForfeit(6000)
            maxHostage = pHostage(6000)
            winnablePercent += 1
            graphsForfeit.append(pForfeit)
            graphsHostage.append(pHostage)
            count += 1
            print('maxForfeit: '+ str(maxForfeit))
            print('maxHostage: '+ str(maxHostage))
        numRows = 0
        if not int(count/2):
            plb.plot(totalForfeit[0], pForfeit(totalForfeit[0]), c = 'red')
            plb.plot(totalHostage[0], pHostage(totalHostage[0]), c = 'blue')
        else:
            subCount = 0
            fig, axs = plt.subplots(2, int(count/2))
            fig.suptitle("Simulation")
            for i in range(2):
                for j in range(int(count/2)):
                    axs[i][j].plot(totalForfeit[subCount][0], totalForfeit[subCount][1])
                    subCount += 1
        print('{totalHours} hours were simulated to determine that you should FF unless your game is winnable {winnablePercent}% of the time'.format(totalHours=count*100,winnablePercent=winnablePercent))
        print(graphsForfeit)
        print(graphsHostage)
        print(winnablePercent)
        plt.xlabel('Time (minutes)')
        plt.ylabel('LP')
        plt.title('Forfeit at 20 Player vs Hostage Player')
        plt.legend(['Forfeit at 20 Player', 'Hostage Player'])
        plt.show()
leagueStats.main()