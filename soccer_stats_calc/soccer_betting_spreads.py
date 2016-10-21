from csv_tools import loadData
import sys

def getColumns(header):
    # CSV columns
    # HomeTeam = Home Team
    # AwayTeam = Away Team
    # FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)
    # Date = Date

    # B365H = Bet365 home win odds
    # B365D = Bet365 draw odds
    # B365A = Bet365 away win odds
    # BSH = Blue Square home win odds
    # BSD = Blue Square draw odds
    # BSA = Blue Square away win odds
    # BWH = Bet&Win home win odds
    # BWD = Bet&Win draw odds
    # BWA = Bet&Win away win odds
    # GBH = Gamebookers home win odds
    # GBD = Gamebookers draw odds
    # GBA = Gamebookers away win odds
    # IWH = Interwetten home win odds
    # IWD = Interwetten draw odds
    # IWA = Interwetten away win odds
    # LBH = Ladbrokes home win odds
    # LBD = Ladbrokes draw odds
    # LBA = Ladbrokes away win odds
    # PSH = Pinnacle Sports home win odds
    # PSD = Pinnacle Sports draw odds
    # PSA = Pinnacle Sports away win odds
    # SOH = Sporting Odds home win odds
    # SOD = Sporting Odds draw odds
    # SOA = Sporting Odds away win odds
    # SBH = Sportingbet home win odds
    # SBD = Sportingbet draw odds
    # SBA = Sportingbet away win odds
    # SJH = Stan James home win odds
    # SJD = Stan James draw odds
    # SJA = Stan James away win odds
    # SYH = Stanleybet home win odds
    # SYD = Stanleybet draw odds
    # SYA = Stanleybet away win odds
    # VCH = VC Bet home win odds
    # VCD = VC Bet draw odds
    # VCA = VC Bet away win odds
    # WHH = William Hill home win odds
    # WHD = William Hill draw odds
    # WHA = William Hill away win odds

    dictCol = dict()
    dictCol['nColHomeTeam'] = header.index("HomeTeam")
    dictCol['nColAwayTeam'] = header.index("AwayTeam")
#    dictCol['nColsOddsHome'] = [i for i in range(header.index("B365H"), range(header.index("B365H") + 3*13, 3)]
#    dictCol['nColsOddsAway'] = [i for i in range(header.index("B365A"), range(header.index("B365A") + 3*13, 3)]
#    dictCol['nColsOddsDraw'] = [i for i in range(header.index("B365D"), range(header.index("B365D") + 3*13, 3)]
    dictCol['nColResult'] = header.index("FTR")
    dictCol['date'] = header.index("Date")

    dictOddCol = dict()

    try:
        dictOddCol['Bet365'] = {'nColOddsHome' : header.index("B365H"),
                                'nColOddsAway' : header.index("B365A"),
                                'nColOddsDraw' : header.index("B365D"),}
    except ValueError:
        pass

    try:
        dictOddCol['Blue Square'] = {'nColOddsHome' : header.index("BSH"),
                                     'nColOddsAway' : header.index("BSA"),
                                     'nColOddsDraw' : header.index("BSD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Bet&Win'] = {'nColOddsHome' : header.index("BWH"),
                                 'nColOddsAway' : header.index("BWA"),
                                 'nColOddsDraw' : header.index("BWD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Gamebookers'] = {'nColOddsHome' : header.index("GBH"),
                                     'nColOddsAway' : header.index("GBA"),
                                     'nColOddsDraw' : header.index("GBD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Interwetten'] = {'nColOddsHome' : header.index("IWH"),
                                     'nColOddsAway' : header.index("IWA"),
                                     'nColOddsDraw' : header.index("IWD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Ladbrokes'] = {'nColOddsHome' : header.index("LBH"),
                                   'nColOddsAway' : header.index("LBA"),
                                   'nColOddsDraw' : header.index("LBD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Pinnacle Sports'] = {'nColOddsHome' : header.index("PSH"),
                                         'nColOddsAway' : header.index("PSA"),
                                         'nColOddsDraw' : header.index("PSD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Sporting Odds'] = {'nColOddsHome' : header.index("SOH"),
                                       'nColOddsAway' : header.index("SOA"),
                                       'nColOddsDraw' : header.index("SOD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Sportingbet'] = {'nColOddsHome' : header.index("SBH"),
                                     'nColOddsAway' : header.index("SBA"),
                                     'nColOddsDraw' : header.index("SBD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Stan James'] = {'nColOddsHome' : header.index("SJH"),
                                    'nColOddsAway' : header.index("SJA"),
                                    'nColOddsDraw' : header.index("SJD"),}
    except ValueError:
        pass

    try:
        dictOddCol['Stanleybet'] = {'nColOddsHome' : header.index("SYH"),
                                    'nColOddsAway' : header.index("SYA"),
                                    'nColOddsDraw' : header.index("SYD"),}
    except ValueError:
        pass

    try:
        dictOddCol['VC Bet'] = {'nColOddsHome' : header.index("VCH"),
                                'nColOddsAway' : header.index("VCA"),
                                'nColOddsDraw' : header.index("VCD"),}
    except ValueError:
        pass

    try:
        dictOddCol['William Hill'] = {'nColOddsHome' : header.index("WHH"),
                                      'nColOddsAway' : header.index("WHA"),
                                      'nColOddsDraw' : header.index("WHD"),}
    except ValueError:
        pass


    return dictCol, dictOddCol


def main():
    if len(sys.argv) > 1:
        csvfile = sys.argv[1]
    else:
        csvfile = 'D1_2013-14.csv'

    header, listRawData = loadData(csvfile)
    dictCol, dictOddCol = getColumns(header)

    dictProbsAndSpread = dict()

    print ',,,'.join(sorted(dictOddCol.keys()))

    for data in listRawData:
        for sBettingAgent in dictOddCol.keys():

            try:
                nHomeOdds = float(data[dictOddCol[sBettingAgent]['nColOddsHome']])
                nAwayOdds = float(data[dictOddCol[sBettingAgent]['nColOddsAway']])
                nDrawOdds = float(data[dictOddCol[sBettingAgent]['nColOddsDraw']])
            except:
                continue

            dictProbsAndSpread[sBettingAgent] = (
                1/nHomeOdds * 100,
                1/nAwayOdds * 100,
                1/nDrawOdds * 100,
                (1 - 1/nHomeOdds - 1/nAwayOdds - 1/nDrawOdds) * 100
            )
            


        print ','.join([ ','.join(map(lambda x: format(x,'f'),dictProbsAndSpread[sBetAgent])) for sBetAgent in sorted(dictOddCol.keys())])


if __name__ == "__main__":
    main()
