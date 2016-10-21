import csv
import sys
from soccer_toolbox import TSR, TSoTt, PDO, rating

def loadData(csvfile):

    listRawData = list()
    with open(csvfile, 'r') as fh:
        csvreader = csv.reader(fh, delimiter=',')
        for nRow, row in enumerate(csvreader):
            if nRow == 0:
                header = row
            else:
                listRawData.append(row)

    return header, listRawData

def getTeams(listData, nColHomeTeam, nColAwayTeam):
    setTeams = set()
    for data in listData:
        setTeams.add(data[nColHomeTeam])
        setTeams.add(data[nColAwayTeam])
    return setTeams

def getColumns(header):
    # CSV columns
    # HomeTeam = Home Team
    # AwayTeam = Away Team
    # FTHG = Full Time Home Team Goals
    # FTAG = Full Time Away Team Goals
    # HS = Home Team Shots
    # AS = Away Team Shots
    # HST = Home Team Shots on Target
    # AST = Away Team Shots on Target

    dictCol = dict()
    dictCol['nColHomeTeam'] = header.index("HomeTeam")
    dictCol['nColAwayTeam'] = header.index("AwayTeam")
    dictCol['nColFTHG'] = header.index("FTHG")
    dictCol['nColFTAG'] = header.index("FTAG")
    dictCol['nColHS'] = header.index("HS")
    dictCol['nColAS'] = header.index("AS")
    dictCol['nColHST'] = header.index("HST")
    dictCol['nColAST'] = header.index("AST")

    return dictCol

def getStatsForTeam(team, dictCol, listRawData):
    nGoalsForH = 0
    nGoalsAgainstH = 0
    nShotsForH = 0
    nShotsAgainstH = 0 
    nShotsTargetForH = 0
    nShotsTargetAgaianstH = 0
    nGamesH = 0 
    nGoalsForA = 0
    nGoalsAgainstA = 0
    nShotsForA = 0
    nShotsAgainstA = 0 
    nShotsTargetForA = 0
    nShotsTargetAgaianstA = 0
    nGamesA = 0

    for data in listRawData:
        if data[dictCol['nColHomeTeam']] == team:
            bHome = True
            nColGoalsFor = dictCol['nColFTHG']
            nColGoalsAgainst = dictCol['nColFTAG']
            nColShotsFor = dictCol['nColHS']
            nColShotsAgainst = dictCol['nColAS']
            nColShotsTargetFor = dictCol['nColHST']
            nColShotsTargetAgainst = dictCol['nColAST']
        elif data[dictCol['nColAwayTeam']] == team:
            nColGoalsFor = dictCol['nColFTAG']
            nColGoalsAgainst = dictCol['nColFTHG']
            nColShotsFor = dictCol['nColAS']
            nColShotsAgainst = dictCol['nColHS']
            nColShotsTargetFor = dictCol['nColAST']
            nColShotsTargetAgainst = dictCol['nColHST']
            bHome = False
        else:
            continue

        if bHome:
            nGoalsForH += int(data[nColGoalsFor])
            nGoalsAgainstH += int(data[nColGoalsAgainst])
            nShotsForH += int(data[nColShotsFor])
            nShotsAgainstH += int(data[nColShotsAgainst])
            nShotsTargetForH += int(data[nColShotsTargetFor])
            nShotsTargetAgaianstH += int(data[nColShotsTargetAgainst])
            nGamesH += 1
        else:
            nGoalsForA += int(data[nColGoalsFor])
            nGoalsAgainstA += int(data[nColGoalsAgainst])
            nShotsForA += int(data[nColShotsFor])
            nShotsAgainstA += int(data[nColShotsAgainst])
            nShotsTargetForA += int(data[nColShotsTargetFor])
            nShotsTargetAgaianstA += int(data[nColShotsTargetAgainst])
            nGamesA += 1

    tsrH = TSR(nShotsForH, nShotsAgainstH)
    tsottH = TSoTt(nShotsTargetForH, nShotsForH, (nShotsAgainstH - nShotsTargetAgaianstH), nShotsAgainstH)
    pdoH = PDO(nGoalsForH, nShotsTargetForH, nShotsTargetAgaianstH, nGoalsAgainstH)

    tsrA = TSR(nShotsForA, nShotsAgainstA)
    tsottA = TSoTt(nShotsTargetForA, nShotsForA, (nShotsAgainstA - nShotsTargetAgaianstA), nShotsAgainstA)
    pdoA = PDO(nGoalsForA, nShotsTargetForA, nShotsTargetAgaianstA, nGoalsAgainstA)

    return { 'TSR_Home': tsrH,
             'TSoTt_Home': tsottH,
             'PDO_Home': pdoH,
             'rating_Home': rating(tsrH, tsottH, pdoH, nGamesH),
             'TSR_Away': tsrA,
             'TSoTt_Away': tsottA,
             'PDO_Away': pdoA,
             'rating_Away': rating(tsrA, tsottA, pdoA, nGamesA)
           }
    

def getStatsDict(setTeams, dictCol, listRawData):
    dictTeamStats = dict()

    for team in setTeams:
        dictTeamStats[team] = getStatsForTeam(team, dictCol, listRawData)
    return dictTeamStats

def fileToStats(csvfile):
    header, listRawData = loadData(csvfile)
    dictCol = getColumns(header)
    setTeams = getTeams(listRawData, dictCol['nColHomeTeam'], dictCol['nColAwayTeam'])
    return getStatsDict(setTeams, dictCol, listRawData)


def main():
    if len(sys.argv) > 1:
        csvfile = sys.argv[1]
    else:
        csvfile = 'D1_2013-14.csv'

    dictTeamStats = fileToStats(csvfile)

    print ','.join(['Club', 'Rating Home', 'Rating Away', 'TSR Home', 'TSR Away', 'TSoTt Home', 'TSoTt Away', 'PDO Home', 'PDO Away'])

    for name, val in sorted(dictTeamStats.items(), key=lambda x: -x[1]['rating_Home']):
        print ','.join(map(str, [name, val['rating_Home'], val['rating_Away'], 
                                       val['TSR_Home'], val['TSR_Away'],
                                       val['TSoTt_Home'], val['TSoTt_Away'],
                                       val['PDO_Home'], val['PDO_Away']]))

if __name__ == "__main__":
    main()
