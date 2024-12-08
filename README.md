# Fantasy Football Tool

This is an application for the Fantasy Premier League. It displays the fixtures for each team, up to 5 weeks, and sorts the teams by those which have the best fixtures. Also shows the players with the top xG and xA stats in the past 5 gws. Also shows goalscorer and clean sheets odds.

<img width="974" alt="screenshot" src="https://github.com/user-attachments/assets/5d1de67b-98dd-46d5-98f7-78ff5f410e20">

## Background to project

I decided to undertake this personal projects when, like most FPL managers, I attempted to gain a competitive edge. I wanted to know teams with best fixtures on average for x number of weeks, and although official fpl apps shows fixtures can only sort by fixtures for a particualr game week and not say 'teams with best fixtures in next 3 gameweeks or 5 gameweeks'. Same idea for xG and xA stats which although can be seen for indiviual player cannot be used when sorting players so see who has best of those statis in x past gameweeks. I wanted an application where I could see the fixtures and stats for up 5 gameweeks, and change accordingly. Another resource which I relied was odds genreated from bookies, which some websites already had on the website but have everything in one place I wanted to have those display alongside (goalscorer and clean sheet odds)

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

API blog
fpl reports 2 pages
