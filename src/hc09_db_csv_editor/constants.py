"""Constants and configuration for the HC09 CSV Editor.

This module contains all constant values used throughout the application,
including stat limits, CSV field keys, team names, and stat mappings.
"""

from typing import Dict

# Stat Limits
MAXPLAYERSTAT = 99
MAXHEALTH = 1000
MAXSKILLPOINTS = 131000
MAXCOACHSTAT = 5
MAXGMSTAT = 5
MINPLRN = 75

# CSV Field Keys
PLAYER_FIRST_NAME_CODE = 'PFNA'
PLAYER_LAST_NAME_CODE = 'PLNA'
COACH_FIRST_NAME_CODE = 'CFNM'
COACH_LAST_NAME_CODE = 'CLNM'
TEAM_ID_KEY = 'TGID'
PERSONNEL_ID_KEY = 'PNid'

# Roster Type Headers
PLAYER_HEADER = 'PSA0'
COACH_HEADER = 'CFDA'
TRAINER_HEADER = 'TRAB'
GM_HEADER = 'GMAB'

# Team Names
TEAM_NAMES: Dict[str, str] = {
    "1": "Bears (Chicago)",
    "2": "Bengals (Cincinnati)",
    "3": "Bills (Buffalo)",
    "4": "Broncos (Denver)",
    "5": "Browns (Cleveland)",
    "6": "Buccaneers (Tampa Bay)",
    "7": "Cardinals (Arizona)",
    "8": "Chargers (Los Angeles)",
    "9": "Chiefs (Kansas City)",
    "10": "Colts (Indianapolis)",
    "11": "Cowboys (Dallas)",
    "12": "Dolphins (Miami)",
    "13": "Eagles (Philadelphia)",
    "14": "Falcons (Atlanta)",
    "15": "49ers (San Francisco)",
    "16": "Giants (New York)",
    "17": "Jaguars (Jacksonville)",
    "18": "Jets (New York)",
    "19": "Lions (Detroit)",
    "20": "Packers (Green Bay)",
    "21": "Panthers (Carolina)",
    "22": "Patriots (New England)",
    "23": "Raiders (Las Vegas)",
    "24": "Rams (Los Angeles)",
    "25": "Ravens (Baltimore)",
    "26": "Redskins (Washington)",
    "27": "Saints (New Orleans)",
    "28": "Seahawks (Seattle)",
    "29": "Steelers (Pittsburgh)",
    "30": "Texans (Houston)",
    "31": "Titans (Tennessee)",
    "32": "Vikings (Minnesota)",
    "33": "Free Agents",
}

# Player Stats Mapping (current stat -> potential stat)
PLAYER_STATS: Dict[str, str] = {
    'PSPD': 'PSDX',
    'PAGI': 'PAGX',
    'PACC': 'PACX',
    'PSTR': 'PSTX',
    'PAWR': 'PAWX',
    'PSTA': 'PSAX',
    'PINJ': 'PINX',
    'PLTR': 'PLTX',
    'PELU': 'PELX',
    'PBCV': 'PBCX',
    'PLSA': 'PLSX',
    'PLSM': 'PSMx',
    'PLJM': 'PLJX',
    'PCAR': 'PCAX',
    'PTHP': 'PTPX',
    'PTHA': 'PTAX',
    'PCTH': 'PCTX',
    'PLSC': 'PSCX',
    'PLCI': 'PLCX',
    'PLRR': 'PRRX',
    'PLRL': 'PRLX',
    'PJMP': 'PJMX',
    'PPBK': 'PPBX',
    'PRBK': 'PRBX',
    'PLIB': 'PIBX',
    'PRBS': 'PRSX',
    'PRBF': 'PRFX',
    'PPBS': 'PPSX',
    'PPBF': 'PPFX',
    'PTAK': 'PTKX',
    'PLHT': 'PLHX',
    'PLPm': 'PPMX',
    'PFMS': 'PFMX',
    'PBSG': 'PBSX',
    'PLPU': 'PPUX',
    'PLPR': 'PPRX',
    'PLMC': 'PLMX',
    'PLZC': 'PLZX',
    'PLPE': 'PPEX',
    'PKPR': 'PKPX',
    'PKAC': 'PKAX',
    'PKRT': 'PKRX',
    'PLRN': 'PLRX',
    'PTGH': 'PTGX'
}

# Player Position Abbreviations
PLAYER_POSITIONS: Dict[str, str] = {
    "0": "QB",
    "1": "HB",
    "2": "FB",
    "3": "WR",
    "4": "TE",
    "5": "LT",
    "6": "LG",
    "7": "C",
    "8": "RG",
    "9": "RT",
    "10": "LE",
    "11": "RE",
    "12": "DT",
    "13": "LOLB",
    "14": "MLB",
    "15": "ROLB",
    "16": "CB",
    "17": "FS",
    "18": "SS",
    "19": "K",
    "20": "P"
}

# Coach Position Abbreviations
COACH_POSITIONS: Dict[str, str] = {
    "0": "HC",
    "1": "OC",
    "2": "DC",
    "3": "STC",
    "4": "QBC",
    "5": "RBC",
    "6": "WRC",
    "7": "OLC",
    "8": "DLC",
    "9": "LBC",
    "10": "DBC",
}
