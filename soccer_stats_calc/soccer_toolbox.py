
dictWeightsByNbrOfGames = {
    0: (0.3, 0, 0),
    5: (0.5, 0.01, 0.01),
    10: (0.65, 0.02, 0.025),
    15: (0.69, 0.05, 0.07),
    20: (0.71, 0.08, 0.1),
    25: (0.72, 0.1, 0.13),
    30: (0.73, 0.15, 0.16),
    35: (0.732, 0.166, 0.176),
    }

def TSR(nShotsFor, nShotsAgainst):
    if nShotsFor + nShotsAgainst == 0:
        return 0.5
    return float(nShotsFor) / (nShotsFor + nShotsAgainst)

def TSoTt_defense(nShotsOffTargetAgainst, nShotsAgainst):
    if nShotsAgainst == 0:
        return 0.5
    return float(nShotsOffTargetAgainst) / nShotsAgainst

def TSoTt_offense(nShotsOnTargetFor, nShotsFor):
    if nShotsFor == 0:
        return 0.5
    return float(nShotsOnTargetFor) / nShotsFor

def TSoTt(nShotsOnTargetFor, nShotsFor, nShotsOffTargetAgainst, nShotsAgainst):
    return TSoTt_offense(nShotsOnTargetFor, nShotsFor) + TSoTt_defense(nShotsOffTargetAgainst, nShotsAgainst)

def PDO_offense(nGoalsFor, nShotsOnTargetFor):
    if nShotsOnTargetFor == 0:
        return 500
    return 1000 * float(nGoalsFor) / nShotsOnTargetFor

def PDO_defense(nShotsOnTargetAgainst, nGoalsAgainst):
    if nShotsOnTargetAgainst == 0:
        return 500
    return 1000 * float(nShotsOnTargetAgainst - nGoalsAgainst) / nShotsOnTargetAgainst

def PDO(nGoalsFor, nShotsOnTargetFor, nShotsOnTargetAgainst, nGoalsAgainst):
    return PDO_offense(nGoalsFor, nShotsOnTargetFor) + PDO_defense(nShotsOnTargetAgainst, nGoalsAgainst)

def rating(TSR, TSoTt, PDO, nGames):
    nGames = nGames - (nGames % 5)
    return  (0.5 + (TSR - 0.5) * dictWeightsByNbrOfGames[nGames][0]**0.5)\
          * (1.0 + (TSoTt - 1.0) * dictWeightsByNbrOfGames[nGames][1]**0.5)\
          * (1000 + (PDO - 1000) * dictWeightsByNbrOfGames[nGames][2]**0.5)

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
    pdo_off = PDO_offense(nGoalsFor, nShotsTargetFor)
    pdo_def = PDO_defense(nShotsTargetAgaianst, nGoalsAgainst)
    pdo = PDO(nGoalsFor, nShotsTargetFor, nShotsTargetAgaianst, nGoalsAgainst)

    return { 'Rating': round(rating(tsr, tsott, pdo, nGames), 2),
             'Points': nPoints,
             'Goals': nGoalsFor - nGoalsAgainst,
             'Goals_off': nGoalsFor,
             'Goals_def': nGoalsAgainst,
             'Shots_target_off': nShotsTargetFor,
             'Shots_target_def': nShotsTargetAgaianst,
             'TSR': round(tsr, 2),
             'TSoTt': round(tsott, 2),
             'TSoTt_off': round(TSoTt_offense(nShotsTargetFor, nShotsFor), 2),
             'TSoTt_def': round(TSoTt_defense((nShotsAgainst - nShotsTargetAgaianst), nShotsAgainst), 2),
             'PDO_off': round(pdo_off, 2),
             'PDO_def': round(pdo_def, 2),
             'PDO': round(pdo, 2)
           }

