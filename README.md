# Fantasy Football App

This is an application for the Fantasy Premier League, a game based on the English Premier League. Fantasy football allows participants to create a virtual team of real life football players. These teams then earn points based on the actual performances of players in premier league matches. The application displays sorted fixtures and player statistics for up to 5 weeks. It also shows the goalscorcer and clean sheet odds for the upcoming gameweek.

![image](https://github.com/user-attachments/assets/2a6d0303-9afe-4efb-bdaa-42e607e92261)

## Background to project

I decided to undertake this personal project because I was unsatisfied with how fixtures and statistics were presented in the official fantasy football app. Although fixtures and their difficultly for each team were shown, there was no way to sort the fixtures by difficulty, except by individual gameweek. I couldn't easily see which teams had the best or worst fixtures for the next x number of weeks. The same thing applied to player statistics which, although can be seen for each indiviual player and compared between players, cannot be used to sort players to see who has best of those statistics in the past x number of weeks. Another resource which I rely on is odds generated from bookies, which some websites already present, but it made things easier having these presented alongside the sorted fixtures and statistics.

## about project
- fixture query official fpl API, then sorted within a SQL db (alongside team name is fixture idfficult, I then sorted using that and presented in table accordingly and then presented in GUI (Pyqt6). Also color coded to illustrate fixture difficult, this was made to be the same as the official FPL app
- Player stats, need db file to run in order to gather data which take ~15min. Then when run main it sorts and displays top 20 players. Has xG and xA and xG + xA.
- To get odds and goalscorer odds use selenium to webscape and then present in table

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
fpl link
API blog
fpl reports 2 pages
