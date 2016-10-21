import sys
from soccer_toolbox import TSR, TSoTt, PDO, rating
from csv_tools import loadData, getTeams

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
    nGoalsFor = 0
    nGoalsAgainst = 0
    nShotsFor = 0
    nShotsAgainst = 0 
    nShotsTargetFor = 0
    nShotsTargetAgaianst = 0
    nGames = 0 

    for data in listRawData:
        if data[dictCol['nColHomeTeam']] == team:
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
        else:
            continue


        nGoalsFor += int(data[nColGoalsFor])
        nGoalsAgainst += int(data[nColGoalsAgainst])
        nShotsFor += int(data[nColShotsFor])
        nShotsAgainst += int(data[nColShotsAgainst])
        nShotsTargetFor += int(data[nColShotsTargetFor])
        nShotsTargetAgaianst += int(data[nColShotsTargetAgainst])
        nGames += 1
 

    tsr = TSR(nShotsFor, nShotsAgainst)
    tsott = TSoTt(nShotsTargetFor, nShotsFor, (nShotsAgainst - nShotsTargetAgaianst), nShotsAgainst)
    pdo = PDO(nGoalsFor, nShotsTargetFor, nShotsTargetAgaianst, nGoalsAgainst)

    return { 'TSR': tsr,
             'TSoTt': tsott,
             'PDO': pdo,
             'rating': rating(tsr, tsott, pdo, nGames),
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

    print '{0:<15} {1:<8} {2:<5} {3:<5} {4:<5}'.format('Club', 'Rating', 'TSR', 'TSoTt', 'PDO')
    print '-' * 40

    for name, val in sorted(dictTeamStats.items(), key=lambda x: -x[1]['rating']):
        print '{0:<15} {1:.4f} {2:.3f} {3:.3f} {4:.1f}'.format(name, val['rating'], val['TSR'], val['TSoTt'], val['PDO'])


if __name__ == "__main__":
    main()
