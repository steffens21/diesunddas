import csv
import sys
import datetime
from collections import defaultdict
from soccer_toolbox import TSR, TSoTt, PDO, rating
from csv_tools import loadData, getTeams, getColumns

def getStatsForTeam(team, dictCol, listRawData, dateCutOff=None, bHome='no choice'):
    nGoalsFor = 0
    nGoalsAgainst = 0
    nShotsFor = 0
    nShotsAgainst = 0 
    nShotsTargetFor = 0
    nShotsTargetAgaianst = 0
    nGames = 0 

    for data in listRawData:
        date = datetime.datetime.strptime(data[dictCol['date']], '%d/%m/%y')
        if data[dictCol['nColHomeTeam']] == team and (bHome==True or bHome == 'no choice'):
            nColGoalsFor = dictCol['nColFTHG']
            nColGoalsAgainst = dictCol['nColFTAG']
            nColShotsFor = dictCol['nColHS']
            nColShotsAgainst = dictCol['nColAS']
            nColShotsTargetFor = dictCol['nColHST']
            nColShotsTargetAgainst = dictCol['nColAST']
        elif data[dictCol['nColAwayTeam']] == team and (bHome==False or bHome == 'no choice'):
            nColGoalsFor = dictCol['nColFTAG']
            nColGoalsAgainst = dictCol['nColFTHG']
            nColShotsFor = dictCol['nColAS']
            nColShotsAgainst = dictCol['nColHS']
            nColShotsTargetFor = dictCol['nColAST']
            nColShotsTargetAgainst = dictCol['nColHST']
        else:
            continue

        if date < dateCutOff:
            nGoalsFor += int(data[nColGoalsFor])
            nGoalsAgainst += int(data[nColGoalsAgainst])
            nShotsFor += int(data[nColShotsFor])
            nShotsAgainst += int(data[nColShotsAgainst])
            nShotsTargetFor += int(data[nColShotsTargetFor])
            nShotsTargetAgaianst += int(data[nColShotsTargetAgainst])
            nGames += 1
 
    if nGames == 0:
        tsr = 0.5
        tsott = 1.0
        pdo = 1000
    else:
        tsr = TSR(nShotsFor, nShotsAgainst)
        tsott = TSoTt(nShotsTargetFor, nShotsFor, (nShotsAgainst - nShotsTargetAgaianst), nShotsAgainst)
        pdo = PDO(nGoalsFor, nShotsTargetFor, nShotsTargetAgaianst, nGoalsAgainst)

    return { 'TSR': tsr,
             'TSoTt': tsott,
             'PDO': pdo,
             'rating': rating(tsr, tsott, pdo, nGames),
           }


def rating_eval(csvfile, nDrawThreshold, sSeason):

    header, listRawData = loadData(csvfile)
    dictCol = getColumns(header)

    nGames = 0
    nCorrect = 0

    for n, data in enumerate(listRawData):
        sHomeTeam = data[dictCol['nColHomeTeam']]
        sAwayTeam = data[dictCol['nColAwayTeam']]
        sResult = data[dictCol['nColResult']]
        date = datetime.datetime.strptime(data[dictCol['date']], '%d/%m/%y') - datetime.timedelta(days=1)
        nHomeRating = getStatsForTeam(sHomeTeam, dictCol, listRawData, date, True)['rating']
        nAwayRating = getStatsForTeam(sAwayTeam, dictCol, listRawData, date, False)['rating']

        if abs(nHomeRating - nAwayRating) < nDrawThreshold:
            sGuess = 'D'
        elif nHomeRating > nAwayRating:
            sGuess = 'H'
        else:
            sGuess = 'A'

        #print "{0:<15}\t{1:<15}\t{2:.2f}\t{3}\t{4}".format(sHomeTeam, sAwayTeam, nHomeRating-nAwayRating, sGuess, sResult)

#        if n < 17*9:
#            continue

        if sGuess == sResult:
            nCorrect += 1
        nGames += 1


    print '\t\t'.join([ sSeason, str(nGames), str(nCorrect) ,"{0:.2f}".format(nCorrect / float(nGames) * 100)])


def main():
    if len(sys.argv) > 1:
        nDrawThreshold = int(sys.argv[1])
    else:
        nDrawThreshold = 0

    print ''
    print '\t'.join(['Season     ', 'Nbr. of Games', 'Correct guesses', 'Percentage'])


    for sSeason in ['2010-11', '2011-12', '2012-13', '2013-14']:
        csvfile = 'D1_%s.csv' % (sSeason)
        rating_eval(csvfile, nDrawThreshold, sSeason)




if __name__ == "__main__":
    main()
