import csv
import sys

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
    # FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)

    dictCol = dict()
    dictCol['nColHomeTeam'] = header.index("HomeTeam")
    dictCol['nColAwayTeam'] = header.index("AwayTeam")
    dictCol['nColFTHG'] = header.index("FTHG")
    dictCol['nColFTAG'] = header.index("FTAG")
    dictCol['nColHS'] = header.index("HS")
    dictCol['nColAS'] = header.index("AS")
    dictCol['nColHST'] = header.index("HST")
    dictCol['nColAST'] = header.index("AST")
    dictCol['nColResult'] = header.index("FTR")
    dictCol['date'] = header.index("Date")

    return dictCol

