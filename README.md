# Fantasy Football App

This is an application for the Fantasy Premier League, a game based on the English Premier League. Fantasy football allows participants to create a virtual team of real life football players. These teams then earn points based on the actual performances of players in premier league matches. The application displays sorted fixtures and player statistics for up to 5 weeks. It also shows the goalscorcer and clean sheet odds for the upcoming gameweek.

![image](https://github.com/user-attachments/assets/2a6d0303-9afe-4efb-bdaa-42e607e92261)

## Background to project

I decided to undertake this personal project because I was unsatisfied with how fixtures and statistics were presented in the official fantasy football app. Although fixtures and their difficultly for each team were shown, there was no way to sort the fixtures by difficulty, except by individual gameweek. I couldn't easily see which teams had the best or worst fixtures for the next x number of weeks. The same thing applied to player statistics which, although can be seen for each indiviual player and compared between players, cannot be used to sort players to see who has best of those statistics in the past x number of weeks. Another resource which I rely on is odds generated from bookies, which some websites already present, but it made things easier having these presented alongside the sorted fixtures and statistics.

## About project
- To present the fixtures, first the official FPL API is queried to obtain a list of fixture with their associated fixture difficulty rating. This data in then stored in a SQL database. The data is then sorted and presented accordingly. 
- For the player statistics, there is python script seperate to the main file which when run creates a database with the player data gathered from the FPL API. Then when the main file is run the sorted players are displayed. The statistics displayed are xG, xA and xG + xA.
- Using Selenium I webscape the goalscorer and clean sheet odds, these are then displayed alongside the fixtures and player statistics.

## dependentcies
- python
- sqlite3
- seleniun
- pyqt6
- requests

## getting started
download files
downlaod geckdriver
pip install those 3 libraries
run db file
then can run file

## useful links
- https://fantasy.premierleague.com
- https://www.fantasyfootballreports.com/premier-league-clean-sheet-odds/
- https://www.fantasyfootballreports.com/premier-league-goalscoring-odds/
- https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19
