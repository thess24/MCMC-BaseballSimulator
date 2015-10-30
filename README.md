# MCMC-BaseballSimulator

This is a monte carlo markov chain baseball game simulator to use for daily fantasy sports betting.  In daily fantasy sports, the bettor puts together a team of players and tries to maximize the number of points that the team gets in a single day.   Each action a player takes corresponds with a point value (i.e., a home run is worth 4 points).  Players all cost different prices and you only have a certain amount of money to spend to build your team.

####Tech Overview
- Python 2.7
- Pandas, Numpy
- BeautifulSoup4, Requests
- Matplotlib
 
####Model Overview

######Scraping data
While there was historic baseball data online that I could have used, it was not at the granularity that I needed for my model.  In order to get statistics by hand (right/left/switch), pitcher type (finesse, power), and location (home/away) for the last 3 years for each player, I had to scrape a website. 
Because baseball lineups change every game and are usually only released a few hours before game time, the lineups had to be scraped from a website as well.

######Cleaning data/ Imputation
After scraping the website, I needed to merge and clean the data into a useable form.  Some players were missing data, which needed to be filled in. Others had such a small number of at-bats/pitches thrown, that the data was not significant. By collecting years of data, I was able to create weighed averages for each players batting and pitching percentages. 

######How the model works
The model runs full game simulations (you can change settings to see the play by play) for each team playing that day and outputs statistics on the games, and the points each player is projected to receive.  The model includes the following variables:
- Park factors
- Handedness of pitcher/batter
- Pitcher substitutions
- Individual player statistics
- League batting/pitching statistics
- Home vs Away

Once the simulation has run, the data was put into an excel spreadsheet that included the price of each player.  From here, I tried a number of approaches to create my team, including a mean variance optimization, simple simplex mean score optimization, and hand picking.
