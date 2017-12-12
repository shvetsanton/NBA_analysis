# NBA_analysis
NBA Statistical Analysis

![nba_logo](https://user-images.githubusercontent.com/21130799/33872191-b6f66988-deca-11e7-8d83-4d6ead3d1e66.jpg)

For this project I set out to increase my chances in winning my fantasy league this year and next!

Along the way I've spotted and learned some interesting trends that have occured in the NBA over the seasons.

## Outline:
- Preprocessing
- Fitting Distributions
- Interesting Trends
- How to draft the best team
- How to maintain the roster



Data: https://www.kaggle.com/drgilermo/nba-players-stats/data

Dataset Summary:

- Number of Seasons: 37
- Number of Unique Players: 2416
- Number of Players in 1980 season: 227
- Number of Players in 2017 season: 439

### Preprocessing:

- Columns of interest: ['Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'TS%', 'FG', 'FGA', 'FG%', '3P', '3PA', 
        '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'TRB', 'AST', 'STL', 'BLK', 
        'TOV', 'PTS']
        
- Drop all rows that do not contain all of those values

- We are left with 15,107 rows and 26 features in the stats dataset

Data Example:
![screen shot 2017-12-11 at 11 30 57 pm](https://user-images.githubusercontent.com/21130799/33872358-6817c748-decb-11e7-8674-a797355b257d.png)


### Create more features:

  - Average # Points
  - Average # Rebounds
  - Average # Steals
  - Average # Assists 
  - ---" ---" Turnovers
  - ---" ---" Blocks
  
  - Fan Points (1*pts + 1.2*reb + 1.5*ast + 3*blk + 3*st - 1*to)
  - Average Fan Points
  
  - 3 Point Fraction (# of 3 Pointers Attempted / # of Field Goals Attempted)
  
## Fitting a Distribution to the Data

For this task I was interested in finding the best distribution for each one of the statistics in our data set.

One way to ensure the best fit...is to try them all!

Below is an example for the Average Points during the 2017 season:

![all_distributions](https://user-images.githubusercontent.com/21130799/33873094-7e2090ee-dece-11e7-8eb3-7810e1986a2d.png)

![best_distribution](https://user-images.githubusercontent.com/21130799/33873115-8cbf938e-dece-11e7-9049-547f6510b2cb.png)

## Game Progression:

Besides the more obvious progressions such as players peaking at a certain age and then declining linearly lets take a look at how the game has changed as a whole!

Below is a set of distributions outlining the progression in the fraction of 3-Pointers over all FG attempts over the years:

![3ptfraction-joyplot](https://user-images.githubusercontent.com/21130799/33873259-2d9c29e8-decf-11e7-9ef5-e62a06909d00.png)

Now lets take a look at the 3-Point Percentage distributions. These have been Normalized for each year to account for the increase of players in the NBA over the years. The distributions also only include players that have taken over 20 shots during the season.

![3pt -joyplot](https://user-images.githubusercontent.com/21130799/33873361-8590b9c0-decf-11e7-9d11-86d4d92d31aa.png)


## EM (Gaussian Mixture Models):

After looking at the distribution progression of 3-Point Percentages in the league I noticed that it might be possible to descrive the distribution in a more complex way by joining two Gaussian distributions.

This way we obtain a parametric way to describe pdf of the distribution instead of just utilizing a kde to smooth over the distribution: 

Here is one of the results:

![3ptgaussianmixture](https://user-images.githubusercontent.com/21130799/33873558-4e433564-ded0-11e7-8f8c-f0939e237b75.png)

### For Draft Advice refer to functions top_players & first_pick

## How to maintain the Best Roster during the Season:

You need to keep up with the league and try to add the best Free Agents or make good Trades!

### Can we trust early season statistics? Is there enough data in the begining of the season to tell a good overall player apart from a player that just had a rare hot streak?

Sure! But only if we use Empirical Bayes Estimation! 

In Empirical Bayes, we fit a beta distribution to the empirical distribution and use this as our prior prediction for players probability. What this means is that our starting point for estimating a players 3PT% is to just ask "Well, how do most players in the NBA shoot 3PT shots?"

![betaapprox](https://user-images.githubusercontent.com/21130799/33873829-52d6f844-ded1-11e7-9916-50dd760c9e8d.png)

Using this as our starting point, we use each player's 3 point attempts and 3 point made shots as evidence to update our prior belief. This means if a player has made a lot of 3PT shots, we update our estimate of their 3PT% to reflect that.

Using Empirical Bayes we account for the small sample sizes by dialing each players 3PT% towards the league average.

![estimation](https://user-images.githubusercontent.com/21130799/33873925-bc24ebee-ded1-11e7-8613-bee4cfa29b4b.png)

Most players are dialed toward the league average!

Here is an example where we can see how bayes estimate effects a players actual 3PT%:

![best_player_estimation](https://user-images.githubusercontent.com/21130799/33873998-006969a6-ded2-11e7-810e-d87c8093931f.png)

The shadded area represents the 95% credible interval for each player. As the players take more shots the credible interval will get tighter. 



This can be extended to all sorts of statistics, lets watch it in action!

  
  
