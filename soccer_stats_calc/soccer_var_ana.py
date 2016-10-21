import sys
from collections import deque
import soccer_toolbox
import csv_tools

def fileToStats(csvfile, stat, nbrAgg):
    header, listRawData = csv_tools.loadData(csvfile)
    dictCol = csv_tools.getColumns(header)
    setTeams = csv_tools.getTeams(listRawData, dictCol['nColHomeTeam'], dictCol['nColAwayTeam'])

    resultDict = {team: list() for team in setTeams}
    teamDataDict = {team: list() for team in setTeams}
    for data in listRawData:
        teamDataDict[data[dictCol['nColHomeTeam']]].append(data)
        teamDataDict[data[dictCol['nColAwayTeam']]].append(data)

    for team in teamDataDict:
        currentData = deque()
        for data in teamDataDict[team]:
            currentData.append(data)
            if len(currentData) <= nbrAgg:
                continue
            else:
                currentData.popleft()
                # calc
                statsDict = soccer_toolbox.getStatsForTeam(team, dictCol, list(currentData))
                resultDict[team].append(statsDict[stat])

        if currentData:
            statsDict = soccer_toolbox.getStatsForTeam(team, dictCol, currentData)
            resultDict[team].append(statsDict[stat])

    return resultDict


def main():
    if len(sys.argv) > 1:
        csvfile = sys.argv[1]
    else:
        csvfile = 'D1.csv'

    stat = 'Rating'
    if len(sys.argv) > 2:
        stat = sys.argv[2]

    nbrAgg = 1
    if len(sys.argv) > 3:
        nbrAgg = int(sys.argv[3]) 
            
    dictTeamStats = fileToStats(csvfile, stat, nbrAgg)

    for name, val in sorted(dictTeamStats.items()):
        print ','.join([name] + map(str, val))

if __name__ == "__main__":
    main()
