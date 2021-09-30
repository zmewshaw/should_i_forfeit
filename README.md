# Should_I_Forfeit
## About
Here is a project I started to settle the argument of whether or not it is worth it to forfeit a game in the popular online game: League of Legends, to save time. It can accomplish this through running statistical analysis on data queried from the Riot Games API.

## Purpose
I started this project for two main reasons,
- I have always believed that it is almost always better to not forfeit in any game since **two** games need to be one to equal the opposite outcome of winning the initial game.
    - For those reading that have not played competitive online games, this is a ***very*** unpopular opinion. Most people that believe the contrary will provide the counter-argument "By forfeiting, you can get into the next game faster, putting you closer to a winning opportunity".
    - Although this statement is correct in itself, it ***almost always*** makes the incorrect assumption that the following games have a high enough chance of winning to make up for the lost opportunity in the current one. Given a player's win rate is generally between 40% and 60%, this is simply not the case.
- I have always struggled to understand web development as I have never had curriculum surrounding it in school. I figured that starting a web development project utilizing other subjects and topics that I am interested in would be the best way to get over it.

## Languages
- [Python](https://www.python.org/)
- [HTML](https://html.com/)
- [JavaScript](https://www.javascript.com/)
- [Bootstrap](https://getbootstrap.com/)

## How to Run
Normally an API key is used to query a users summoner name and winrate, but publishing a valid API key here is a security risk. Therefore, the demonstration must run in a separate file with basic user inputs in place of variables that would normally be queried. This still gives you the ability to 

To view an analysis, you must:
- Install Python.
- Install the packages "numpy" and "matplotlib" with pip.
If this is something you are unfamiliar with, refer to the following: https://www.python.org/downloads/.
- Clone the repository and run the Python program "should_i_forfeit_sample.py", located in the main directory.

For the best sample results, use the values 52, 16, 14, 500 as inputs. Maximize the output window for the best viewing experience.

## The Output
The output you get should be a window filled with subplots, the number of which being dependent on the provided input variables. Since the goal of the program is to determine if a player should forfeit a game to save time, 2 simulations are plotted as the amount of points gained or lost over 100 hours.
- The red line (Forfeit Player) corrisponds to a player that forfeits every game that is predetermined to be a loss as soon as possible (20 minutes).
- The blue line corrisponds to a player that, in essence, gives the game another chance in exchange for 20 extra minutes if the game is lost anyways (40 minutes win or loss after this second chance is given).

Wins take a random integer amount of time between 25 and 35 minutes.
