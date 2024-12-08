import sys
import requests
import sqlite3
from PyQt6.QtWidgets import (QApplication, QWidget, QComboBox, QTabWidget, QLabel, QTableWidget, QTableWidgetItem,
                             QHeaderView, QVBoxLayout)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


class Window(QWidget):
    """A class to display fixtures, player stats and odds in a GUI"""
    def __init__(self):
        """Initialize Window class"""
        super().__init__()
        self.resize(1300, 650)
        self.setWindowTitle("Fantasy Football Tool")

        self.combo1 = QComboBox(self)
        self.combo1.addItems(['1', '2', '3', '4', '5'])
        self.combo1.move(45, 20)
        self.combo1.setCurrentIndex(-1)  # makes the dropdown blank initially
        self.combo1.activated.connect(self.populate_table_with_fixtures)

        self.label1 = QLabel("Weeks:", self)
        self.label1.move(0, 20)

        self.table1 = QTableWidget(self)
        self.table1.move(0, 50)
        self.table1.setRowCount(20)
        self.table1.setColumnCount(5)
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # fits table to size
        self.table1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table1.setFixedSize(475, 525)

        fix = Fixtures(1)
        teams = fix.retrieve_teams()
        self.curr = fix.get_current_gameweek()
        self.table1.setVerticalHeaderLabels([team[0] for team in teams])
        self.table1.setHorizontalHeaderLabels([f'GW{i}' for i in range(self.curr, self.curr + 6)])
        self.table1.horizontalHeader().setDisabled(True)  # make headers read-only
        self.table1.verticalHeader().setDisabled(True)
        self.make_table_read_only(self.table1)

        self.combo2 = QComboBox(self)
        self.combo2.addItems(['1', '2', '3', '4', '5'])
        self.combo2.move(550, 20)
        self.combo2.setCurrentIndex(-1)
        self.combo2.activated.connect(self.populate_table_with_stats)

        self.label2 = QLabel("Weeks:", self)
        self.label2.move(500, 20)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.move(500, 50)
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab_widget.addTab(self.tab1, "xG")
        self.tab_widget.addTab(self.tab2, "xA")
        self.tab_widget.addTab(self.tab3, "xG+xA")

        self.table2 = QTableWidget(self)
        self.table2.setColumnCount(5)
        self.table2.setRowCount(20)
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.table2)
        self.tab1.setLayout(self.layout1)
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table2.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table2.setHorizontalHeaderLabels([f'GW{self.curr - i}' for i in range(5, 0, -1)])
        self.table2.horizontalHeader().setDisabled(True)
        self.table2.verticalHeader().setDisabled(True)
        self.table2.setFixedSize(450, 475)
        self.make_table_read_only(self.table2)

        self.table3 = QTableWidget(self)
        self.table3.setColumnCount(5)
        self.table3.setRowCount(20)
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.table3)
        self.tab2.setLayout(self.layout2)
        self.table3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table3.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table3.setHorizontalHeaderLabels([f'GW{self.curr - i}' for i in range(5, 0, -1)])
        self.table3.horizontalHeader().setDisabled(True)
        self.table3.verticalHeader().setDisabled(True)
        self.make_table_read_only(self.table3)

        self.table4 = QTableWidget(self)
        self.table4.setColumnCount(5)
        self.table4.setRowCount(20)
        self.layout3 = QVBoxLayout()
        self.layout3.addWidget(self.table4)
        self.tab3.setLayout(self.layout3)
        self.table4.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table4.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table4.setHorizontalHeaderLabels([f'GW{self.curr - i}' for i in range(5, 0, -1)])
        self.table4.horizontalHeader().setDisabled(True)
        self.table4.verticalHeader().setDisabled(True)
        self.make_table_read_only(self.table4)

        self.table5 = QTableWidget(self)
        self.table5.move(1000, 75)
        self.table5.setRowCount(20)
        self.table5.setColumnCount(2)
        self.table5.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table5.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table5.setFixedSize(225, 240)
        self.table5.verticalHeader().hide()
        self.table5.setHorizontalHeaderLabels([f'GW{i}' for i in range(self.curr, self.curr + 6)])
        self.table5.setHorizontalHeaderLabels(["Team", "Clean Sheet Odds"])
        self.make_table_read_only(self.table5)

        self.table6 = QTableWidget(self)
        self.table6.move(1000, 330)
        self.table6.setRowCount(30)
        self.table6.setColumnCount(2)
        self.table6.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table6.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table6.setFixedSize(225, 240)
        self.table6.verticalHeader().hide()
        self.table6.setHorizontalHeaderLabels(["Player", "Goalscorer Odds"])
        self.make_table_read_only(self.table6)

        self.populate_table_with_odds()

    def make_table_read_only(self, table):
        """Make table cells read-only"""
        for col in range(table.columnCount()):
            for row in range(table.rowCount()):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                table.setItem(row, col, item)

    def clear_table(self, table):
        """Clear any values in the table cells"""
        for col in range(5):
            for row in range(20):
                table.setItem(row, col, QTableWidgetItem(""))

    def populate_table_with_odds(self):
        """Populate tables with cleansheet and goalscorer odds"""
        odds = Odds()
        cs = odds.clean_sheet_odds()
        for i in range(0, 20):
            for j in range(0, 2):
                item = QTableWidgetItem(str(cs[i][j]))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # make cells read-only
                self.table5.setItem(i, j, item)
        
        gs = odds.goalscorer_odds()
        for i in range(0, 30):
            for j in range(0, 2):
                item = QTableWidgetItem(str(gs[i][j]))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table6.setItem(i, j, item)

    def populate_table_with_stats(self):
        """Populate tables with xG, xA and xG+xA stats for players"""
        self.clear_table(self.table2)
        self.clear_table(self.table3)
        self.clear_table(self.table4)

        header_labels = [f"GW{i}" for i in range(self.curr - int(self.combo2.currentText()), self.curr)]
        while len(header_labels) < 5:
            header_labels += " "

        self.table2.setHorizontalHeaderLabels(header_labels)
        self.table3.setHorizontalHeaderLabels(header_labels)
        self.table4.setHorizontalHeaderLabels(header_labels)

        stats = PlayerStats()

        xg_list = stats.get_xg(int(self.combo2.currentText()))
        self.table2.setVerticalHeaderLabels([element[1] for element in xg_list])

        for i in range(0, 20):
            for j in range(0, int(self.combo2.currentText())):
                item = QTableWidgetItem(str(xg_list[i][j + 2]))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table2.setItem(i, j, item)
                self.table2.item(i, j).setTextAlignment(0x0080 | 0x0004)

        xa_list = stats.get_xa(int(self.combo2.currentText()))
        self.table3.setVerticalHeaderLabels([element[1] for element in xa_list])

        for i in range(0, 20):
            for j in range(0, int(self.combo2.currentText())):
                item = QTableWidgetItem(str(xa_list[i][j + 2]))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table3.setItem(i, j, item)
                self.table3.item(i, j).setTextAlignment(0x0080 | 0x0004)

        xgxa_list = stats.get_xgxa(int(self.combo2.currentText()))
        self.table4.setVerticalHeaderLabels([element[1] for element in xgxa_list])

        for i in range(0, 20):
            for j in range(0, int(self.combo2.currentText())):
                item = QTableWidgetItem(str(xgxa_list[i][j + 2]))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table4.setItem(i, j, item)
                self.table4.item(i, j).setTextAlignment(0x0080 | 0x0004)

    def populate_table_with_fixtures(self):
        """Populate table with fixtures for each team"""
        self.clear_table(self.table1)

        fixtures = Fixtures(int(self.combo1.currentText()))
        fixture_list = fixtures.retrieve_fixtures()
        self.table1.setVerticalHeaderLabels([element[3] for element in fixture_list])

        for i in range(0, 20):
            for j in range(0, int(self.combo1.currentText())):
                item = QTableWidgetItem(fixture_list[i][j+4])
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table1.setItem(i, j, item)
                self.table1.item(i, j).setTextAlignment(0x0080 | 0x0004)

                try:
                    if len(fixture_list[i][j+4]) > 6:  # dgw scenario
                        num = round((int(fixture_list[i][j + 4][4]) + int(fixture_list[i][j+4][11]))/2)
                        self.colour_fixtures(i, j, num)
                    else:
                        self.colour_fixtures(i, j, int(fixture_list[i][j+4][4]))
                except ValueError:
                    self.colour_fixtures(i, j, 6)

    def colour_fixtures(self, row, col, num):
        """Each cell for the fixtures is coloured depending on the difficulty of the fixture"""
        if num == 1:  # dark green
            self.table1.item(row, col).setBackground(QColor(0, 100, 0))
        elif num == 2:  # lime green
            self.table1.item(row, col).setBackground(QColor(50, 205, 50))
        elif num == 3:  # grey
            self.table1.item(row, col).setBackground(QColor(192, 192, 192))
        elif num == 4:  # red
            self.table1.item(row, col).setBackground(QColor(255, 0, 0))
            self.table1.item(row, col).setForeground(QColor("white"))
        elif num == 5:  # maroon
            self.table1.item(row, col).setBackground(QColor(128, 0, 0))
            self.table1.item(row, col).setForeground(QColor("white"))
        else:  # white
            self.table1.item(row, col).setBackground(QColor(255, 255, 255))


class Odds:
    """A class to webscrape the cleansheet and goalscoring odds for the current gameweek"""
    def clean_sheet_odds(self):
        """Webscrape cleansheet odds"""
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)

        clean_sheet = []

        driver.get("https://www.fantasyfootballreports.com/premier-league-clean-sheet-odds/")

        tbody_element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "row-hover")))
        rows = tbody_element.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            clean_sheet.append([elements[0].text, elements[1].text])

        driver.quit()

        return clean_sheet

    def goalscorer_odds(self):
        """Webscrape goalscorer odds"""
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)

        goalscorers = []

        driver.get("https://www.fantasyfootballreports.com/premier-league-goalscoring-odds/")

        tbody_element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CLASS_NAME, "row-hover")))
        rows = tbody_element.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            goalscorers.append([elements[0].text, elements[1].text])

        driver.quit()

        return goalscorers


class Fixtures:
    """A class to retrieve fixtures and fixture difficulty from the Fantasy Premier League API and sort"""
    def __init__(self, weeks):
        """Initialise Fixtures attributes"""
        self.weeks = weeks

        self.base_url = 'https://fantasy.premierleague.com/api/'
        self.r = requests.get(self.base_url+'bootstrap-static/').json()

        self.create_fixtures_table()
        self.insert_fixtures()

    def create_fixtures_table(self):
        """Create database table which will contain fixtures and fixture difficulty"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        c.execute("DROP TABLE IF EXISTS teams_fixtures")

        c.execute("""CREATE TABLE teams_fixtures (
                     id INTEGER PRIMARY KEY,
                     total INTEGER,
                     count INTEGER,
                     team_name TEXT
                     )""")

        for i in range(0, 20):
            team_name = self.r['teams'][i]["short_name"]
            c.execute("INSERT INTO teams_fixtures VALUES (?, 0, 0, ?)", (i, team_name))

        conn.commit()
        conn.close()

    def get_current_gameweek(self):
        """Returns the current gameweek"""
        for i in range(0, 38):
            curr_gw = self.r['events'][i]['deadline_time'].replace('T', ' ').replace('Z', '')  # format FPL datetime
            if datetime.now().strftime('%Y-%m-%d %H:%M:%S') < curr_gw:
                return self.r['events'][i]['id']

    def get_team_name(self, team_id):
        """Returns team name abbreviation associated with given id"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        c.execute("SELECT team_name FROM teams_fixtures WHERE id = ?", (team_id,))
        name = ''.join(c.fetchone())

        conn.commit()
        conn.close()

        return name

    def insert_fixtures(self):
        """Insert the fixtures for the specified number of weeks into the database table"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        for i in range(self.get_current_gameweek(), self.get_current_gameweek() + self.weeks):
            gw = requests.get(self.base_url + 'fixtures/?event=' + str(i)).json()

            text = f"""ALTER TABLE teams_fixtures ADD COLUMN {'GW' + str(i)} TEXT"""
            c.execute(text)

            for j in range(len(gw)):
                fix1 = str(self.get_team_name(gw[j]['team_h'] - 1)) + '(' + str(gw[j]['team_a_difficulty']) + ')'
                fix2 = str(self.get_team_name(gw[j]['team_a'] - 1)) + '(' + str(gw[j]['team_h_difficulty']) + ')'

                # statement inserts fixture and handles double gameweek scenario
                c.execute(f"""UPDATE teams_fixtures
                              SET {'GW' + str(i)} = 
                                  CASE
                                      WHEN {'GW' + str(i)} IS NULL THEN '{fix1}'
                                      ELSE {'GW' + str(i)} || '|{fix1}'
                                  END,
                                  total = total + {gw[j]['team_a_difficulty']},
                                  count = count + 1
                              WHERE id = {gw[j]['team_a'] - 1}
                              """)

                # statement inserts fixture and handles double gameweek scenario
                c.execute(f"""UPDATE teams_fixtures
                            SET {'GW' + str(i)} = 
                                CASE
                                    WHEN {'GW' + str(i)} IS NULL THEN '{fix2}'
                                    ELSE {'GW' + str(i)} || '|{fix2}'
                                END,
                                total = total + {gw[j]['team_h_difficulty']},
                                count = count + 1
                            WHERE id = {gw[j]['team_h'] - 1}
                            """)

            # statement to deal with blank fixtures
            c.execute(f"""UPDATE teams_fixtures 
                          SET {'GW' + str(i)} = 'BLANK',
                          total = total + 6
                          WHERE {'GW' + str(i)} IS NULL
                          """)

        conn.commit()
        conn.close()

    def retrieve_fixtures(self):
        """Return fixtures sorted by fixture difficulty"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        c.execute("""SELECT *,
                     CAST(total AS REAL) / count AS average
                     FROM teams_fixtures 
                     ORDER BY average ASC
                     """)
        rows = c.fetchall()

        conn.commit()
        conn.close()

        return rows

    def retrieve_teams(self):
        """Return all premier league teams"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        c.execute("SELECT team_name FROM teams_fixtures")

        teams = c.fetchall()

        conn.commit()
        conn.close()

        return teams


class PlayerStats:
    """A class to retrieve xG and xA statistics for each player from the Fantasy Premier League API and sort"""
    def get_xg(self, weeks):
        """Return the xG statistics for every player for the specified number of weeks"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        xg_columns = ", ".join(f"xG{i}" for i in range(6 - weeks, 6))
        c.execute(f"""SELECT id, name, {xg_columns},
                      (CAST({'+'.join(f'xG{i}' for i in range(6 - weeks, 6))} AS REAL) / {weeks}) AS xg_average{weeks}
                      FROM player_stats
                      ORDER BY xg_average{weeks} DESC
                      """)
        rows = c.fetchall()

        conn.commit()
        conn.close()

        return rows

    def get_xa(self, weeks):
        """Return the xA statistics for every player for the specified number of weeks"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        xa_columns = ", ".join(f"xA{i}" for i in range(6 - weeks, 6))
        c.execute(f"""SELECT id, name, {xa_columns},
                      (CAST({'+'.join(f'xA{i}' for i in range(6 - weeks, 6))} AS REAL) / {weeks}) AS xa_average{weeks}
                      FROM player_stats
                      ORDER BY xa_average{weeks} DESC
                      """)
        rows = c.fetchall()

        conn.commit()
        conn.close()

        return rows

    def get_xgxa(self, weeks):
        """Return the xG+xA statistics for every player for the specified number of weeks"""
        conn = sqlite3.connect('fantasy_football_data.db')
        c = conn.cursor()

        xgxa_columns = ", ".join(f"xGxA{i}" for i in range(6 - weeks, 6))
        c.execute(f"""SELECT id, name, {xgxa_columns},
                    (CAST({'+'.join(f'xGxA{i}' for i in range(6 - weeks, 6))} AS REAL) / {weeks}) AS xgxa_average{weeks}
                     FROM player_stats
                     ORDER BY xgxa_average{weeks} DESC
                     """)
        rows = c.fetchall()

        conn.commit()
        conn.close()

        return rows


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
