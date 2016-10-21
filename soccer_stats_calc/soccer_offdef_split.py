import csv
import sys

dictWeightsByNbrOfGames = {
    0: (0.3, 0, 0),
    5: (0.5, 0.01, 0.01),
    10: (0.65, 0.02, 0.025),
    15: (0.69, 0.05, 0.07),
    20: (0.71, 0.08, 0.1),
    25: (0.72, 0.09, 0.13),
    30: (0.73, 0.1, 0.16),
    35: (0.732, 0.166, 0.176),
    }


def TSR(nShotsFor, nShotsAgainst):
    return float(nShotsFor) / (nShotsFor + nShotsAgainst)

def TSoTt_off(nShotsOnTargetFor, nShotsFor):
    return float(nShotsOnTargetFor) / nShotsFor

def TSoTt_def(nShotsOffTargetAgainst, nShotsAgainst):
    return float(nShotsOffTargetAgainst) / nShotsAgainst

def TSoTt(nShotsOnTargetFor, nShotsFor, nShotsOffTargetAgainst, nShotsAgainst):
    return TSoTt_off(nShotsOnTargetFor, nShotsFor) + TSoTt_def(nShotsOffTargetAgainst, nShotsAgainst)

def PDO_off(nGoalsFor, nShotsOnTargetFor):
    return 1000 * float(nGoalsFor) / nShotsOnTargetFor

def PDO_def(nShotsOnTargetAgainst, nGoalsAgainst):
    return 1000 * float(nShotsOnTargetAgainst - nGoalsAgainst) / nShotsOnTargetAgainst

def PDO(nGoalsFor, nShotsOnTargetFor, nShotsOnTargetAgainst, nGoalsAgainst):
    return PDO_off(nGoalsFor, nShotsOnTargetFor) + PDO_def(nShotsOnTargetAgainst, nGoalsAgainst)
    
def rating(TSR, TSoTt, PDO, nGames):
    nGames = nGames - (nGames % 5)
    return  (0.5 + (TSR - 0.5) * dictWeightsByNbrOfGames[nGames][0]**0.5)\
          * (1.0 + (TSoTt - 1.0) * dictWeightsByNbrOfGames[nGames][1]**2)\
          * (1000 + (PDO - 1000) * dictWeightsByNbrOfGames[nGames][2]**0.5)

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
    nGoalsFor = 0
    nGoalsAgainst = 0
    nShotsFor = 0
    nShotsAgainst = 0 
    nShotsTargetFor = 0
    nShotsTargetAgaianst = 0
    nGames = 0
    nPoints = 0

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
        if int(data[nColGoalsFor]) > int(data[nColGoalsAgainst]):
            nPoints += 3
        elif int(data[nColGoalsFor]) == int(data[nColGoalsAgainst]):
            nPoints += 1
 

    tsr = TSR(nShotsFor, nShotsAgainst)
    tsott = TSoTt(nShotsTargetFor, nShotsFor, (nShotsAgainst - nShotsTargetAgaianst), nShotsAgainst)
    pdo_off = PDO_off(nGoalsFor, nShotsTargetFor)
    pdo_def = PDO_def(nShotsTargetAgaianst, nGoalsAgainst)
    pdo = PDO(nGoalsFor, nShotsTargetFor, nShotsTargetAgaianst, nGoalsAgainst)

    return { 'Rating': round(rating(tsr, tsott, pdo, nGames), 2),
             'Points': nPoints,
             'Goals': nGoalsFor - nGoalsAgainst,
             'Goals_off': nGoalsFor,
             'Goals_def': nGoalsAgainst,
             'TSR': round(tsr, 2),
             'TSoTt': round(tsott, 2),
             'TSoTt_off': round(TSoTt_off(nShotsTargetFor, nShotsFor), 2),
             'TSoTt_def': round(TSoTt_def((nShotsAgainst - nShotsTargetAgaianst), nShotsAgainst), 2),
             'PDO_off': round(pdo_off, 2),
             'PDO_def': round(pdo_def, 2),
             'PDO': round(pdo, 2)
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
        csvfile = 'D1.csv'

    dictTeamStats = fileToStats(csvfile)

#    print '{0:<15}\t{1:<6}\t{2:<8}\t{3:<8}'.format('Club', 'PDO', 'PDO-Offense', 'PDO-Defense')
#    print '-' * 45

#    for name, val in sorted(dictTeamStats.items(), key=lambda x: -x[1]['PDO']):
#        print '{0:<15}\t{1:.1f}\t{2:.1f}\t\t{3:.1f}'.format(name, val['PDO'], val['PDO_off'], val['PDO_def'])

    print ','.join(['Club',
                    'Rating',
                    'Points',
                    'Goals Diff',
                    'Goals Scored',
                    'Goals Conceded',
                    'TSR',
                    'TSoTt',
                    'TSoTt-Offense',
                    'TSoTt-Defense',
                    'PDO',
                    'PDO-Offense',
                    'PDO-Defense'])
 
    for name, val in sorted(dictTeamStats.items(), key=lambda x: -x[1]['Points']):
        print ','.join(map(str, [name,
                                 val['Rating'],
                                 val['Points'],
                                 val['Goals'],
                                 val['Goals_off'],
                                 val['Goals_def'],
                                 val['TSR'],
                                 val['TSoTt'],
                                 val['TSoTt_off'],
                                 val['TSoTt_def'],
                                 val['PDO'],
                                 val['PDO_off'],
                                 val['PDO_def']]))


if __name__ == "__main__":
    main()
