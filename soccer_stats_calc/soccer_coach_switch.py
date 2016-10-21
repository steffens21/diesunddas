import csv
import sys
import datetime
from soccer_toolbox import TSR, TSoTt, PDO, rating


def loadData(csvfile):

    listRawData = list()
    if csvfile == '-':
        fh = sys.stdin
    else:
        fh = open(csvfile, 'r')

    try:
        csvreader = csv.reader(fh, delimiter=',')
        for nRow, row in enumerate(csvreader):
            if nRow == 0:
                header = row
            else:
                listRawData.append(row)
    except Exception, sErr:
        print sErr
        sys.exit(1)
    finally:
        fh.close()

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
    # Date = Date

    dictCol = dict()
    dictCol['nColHomeTeam'] = header.index("HomeTeam")
    dictCol['nColAwayTeam'] = header.index("AwayTeam")
    dictCol['nColFTHG'] = header.index("FTHG")
    dictCol['nColFTAG'] = header.index("FTAG")
    dictCol['nColHS'] = header.index("HS")
    dictCol['nColAS'] = header.index("AS")
    dictCol['nColHST'] = header.index("HST")
    dictCol['nColAST'] = header.index("AST")
    dictCol['date'] = header.index("Date")

    return dictCol

def getStatsForTeam(team, dictCol, listRawData, dateCutOff=None):
    nGoalsForPC = 0 # PC = pre cut-off
    nGoalsAgainstPC = 0
    nShotsForPC = 0
    nShotsAgainstPC = 0 
    nShotsTargetForPC = 0
    nShotsTargetAgaianstPC = 0
    nGamesPC = 0
    nGoalsForAC = 0 # AC = after cut-off
    nGoalsAgainstAC = 0
    nShotsForAC = 0
    nShotsAgainstAC = 0 
    nShotsTargetForAC = 0
    nShotsTargetAgaianstAC = 0
    nGamesAC = 0

    for data in listRawData:
        date = datetime.datetime.strptime(data[dictCol['date']], '%d/%m/%y')
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

        if date < dateCutOff:
            nGoalsForPC += int(data[nColGoalsFor])
            nGoalsAgainstPC += int(data[nColGoalsAgainst])
            nShotsForPC += int(data[nColShotsFor])
            nShotsAgainstPC += int(data[nColShotsAgainst])
            nShotsTargetForPC += int(data[nColShotsTargetFor])
            nShotsTargetAgaianstPC += int(data[nColShotsTargetAgainst])
            nGamesPC += 1
        else:
            nGoalsForAC += int(data[nColGoalsFor])
            nGoalsAgainstAC += int(data[nColGoalsAgainst])
            nShotsForAC += int(data[nColShotsFor])
            nShotsAgainstAC += int(data[nColShotsAgainst])
            nShotsTargetForAC += int(data[nColShotsTargetFor])
            nShotsTargetAgaianstAC += int(data[nColShotsTargetAgainst])
            nGamesAC += 1

    if nGamesPC == 0 or nGamesAC == 0:
        print "Bad cut-off date"
        sys.exit(1)

    tsrPC = TSR(nShotsForPC, nShotsAgainstPC)
    tsottPC = TSoTt(nShotsTargetForPC, nShotsForPC, (nShotsAgainstPC - nShotsTargetAgaianstPC), nShotsAgainstPC)
    pdoPC = PDO(nGoalsForPC, nShotsTargetForPC, nShotsTargetAgaianstPC, nGoalsAgainstPC)

    tsrAC = TSR(nShotsForAC, nShotsAgainstAC)
    tsottAC = TSoTt(nShotsTargetForAC, nShotsForAC, (nShotsAgainstAC - nShotsTargetAgaianstAC), nShotsAgainstAC)
    pdoAC = PDO(nGoalsForAC, nShotsTargetForAC, nShotsTargetAgaianstAC, nGoalsAgainstAC)

    return { 'TSR-pre': tsrPC,
             'TSoTt-pre': tsottPC,
             'PDO-pre': pdoPC,
             'rating-pre': rating(tsrPC, tsottPC, pdoPC, nGamesPC),
             'TSR-after': tsrAC,
             'TSoTt-after': tsottAC,
             'PDO-after': pdoAC,
             'rating-after': rating(tsrAC, tsottAC, pdoAC, nGamesAC),
           }
    

def getStatsDict(setTeams, dictCol, listRawData, dateCutOff=None):
    dictTeamStats = dict()

    for team in setTeams:
        dictTeamStats[team] = getStatsForTeam(team, dictCol, listRawData, dateCutOff)
    return dictTeamStats

def fileToStats(csvfile, dateCutOff=None, sTeam=None):
    header, listRawData = loadData(csvfile)
    dictCol = getColumns(header)
    setTeams = getTeams(listRawData, dictCol['nColHomeTeam'], dictCol['nColAwayTeam'])
    if not sTeam or sTeam not in setTeams:
        print "Please enter valid team name.  Choices: ", setTeams
        sys.exit(1)
    return getStatsDict([sTeam], dictCol, listRawData, dateCutOff)


def main():
    if len(sys.argv) > 1:
        csvfile = sys.argv[1]
    else:
        csvfile = 'D1_2013-14.csv'

    if len(sys.argv) > 2:
        sDate1 = sys.argv[2]
    else:
        sDate1 = '2014-03-26'

    if len(sys.argv) > 3:
        sTeam = sys.argv[3]
    else:
        sTeam = 'Hertha'

    try:
        date1 = datetime.datetime.strptime(sDate1, '%Y-%m-%d')
    except:
        print "Please enter date in format YYYY-MM-DD"
        sys.exit(1)

    dictTeamStats = fileToStats(csvfile, date1, sTeam)
    
    print ''
    print '{0:<15} {1:<15}\t{2:<15}\t\t{3}'.format('Club', 'Rating before {0}'.format(sDate1), 'Rating after {0}'.format(sDate1), 'Difference %')
    print '-' * 100

    for name, val in sorted(dictTeamStats.items(), key=lambda x: -x[1]['rating-pre']):
        print '{0:<15} {1:.2f}\t\t\t\t{2:.2f}\t\t\t\t{3:.2f} %'.format(name, val['rating-pre'], val['rating-after'], (val['rating-after']-val['rating-pre']) / float(val['rating-pre']) *100 )
    print ''

    #print ",".join(['Club', 'Rating before {0}'.format(sDateCutOff), 'Rating after {0}'.format(sDateCutOff)])
    #for name, val in sorted(dictTeamStats.items(), key=lambda x: -x[1]['rating-pre']):
    #    print ",".join([name, str(val['rating-pre']), str(val['rating-after'])])

if __name__ == "__main__":
    main()
