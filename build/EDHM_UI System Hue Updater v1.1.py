"""
ED HUD Colour Mod
=================
Version: 3.2.1
- Back to vanilla tkinter
- Horizontal layout: Environmental and Ship HUD side by side
- Two pages: HUD and Current System
- Page buttons above palette buttons
"""

import os
import re
import json
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# =============================================
# PALETTES
# =============================================

MAP_ECONOMY = {
    "None":(0.5,0.5,0.5),"Tourism":(0.5,0.0,0.8),"Service":(0.0,0.3,1.0),
    "Refinery":(1.0,0.5,0.0),"Extraction":(1.0,0.0,0.0),"Industrial":(1.0,1.0,0.0),
    "Agriculture":(0.0,1.0,0.0),"HighTech":(0.0,1.0,1.0),"Colony":(0.2,0.4,1.0),
    "Military":(1.0,0.0,1.0),"Terraforming":(0.5,1.0,0.0),"Prison":(0.25,0.25,0.25),
    "Damaged":(0.05,0.05,0.05),"Rescue":(1.0,1.0,0.0),
}
MAP_GOVERNMENT = {
    "None":(1.0,1.0,1.0),"Anarchy":(1.0,0.5,0.0),"Colony":(0.6,0.8,0.0),
    "Democracy":(0.0,1.0,0.0),"Imperial":(0.0,0.8,0.2),"Corporate":(0.0,0.7,0.4),
    "Communism":(0.0,0.8,0.7),"Feudal":(0.3,0.6,1.0),"Dictatorship":(0.0,0.3,1.0),
    "Theocracy":(0.3,0.0,1.0),"Cooperative":(0.6,0.0,1.0),"Patronage":(0.8,0.0,0.8),
    "Confederacy":(1.0,0.0,0.0),"PrisonColony":(1.0,0.3,0.0),"Engineer":(0.5,0.5,0.5),
}
MAP_STATE = {
    "None":(1.0,1.0,1.0),"Retreat":(1.0,0.0,0.0),"War":(1.0,0.5,0.0),
    "Lockdown":(1.0,1.0,0.0),"CivilUnrest":(0.6,0.8,0.0),"CivilWar":(0.0,1.0,0.0),
    "Boom":(0.0,1.0,1.0),"Expansion":(0.3,0.6,1.0),"Bust":(0.0,0.3,1.0),
    "Outbreak":(0.3,0.0,1.0),"Famine":(0.6,0.0,1.0),"Election":(0.6,0.3,0.0),
    "Investment":(0.8,0.8,0.8),"CivilLiberty":(1.0,0.0,0.5),"Incursion":(1.0,0.5,0.8),
    "Blight":(0.8,0.4,0.8),"NaturalDisaster":(1.0,0.0,0.0),"InfrastructureFailure":(0.7,0.4,0.0),
    "Drought":(0.0,1.0,0.0),"TerroristAttack":(0.5,0.5,0.5),"PublicHoliday":(0.5,0.0,0.8),
    "ThargoidAlert":(1.0,1.0,0.0),"ThargoidInvasion":(1.0,0.5,0.0),"ThargoidControlled":(0.6,0.8,0.0),
    "ThargoidTitan":(1.0,0.0,0.0),"PostThargoidRecovery":(0.6,0.0,1.0),"Counterstrike":(0.0,1.0,0.0),
}
MAP_ALLEGIANCE = {
    "None":(0.5,0.5,0.5),"Federation":(1.0,0.0,0.0),"Empire":(0.0,0.3,1.0),
    "Alliance":(0.0,1.0,0.0),"Independent":(1.0,1.0,0.0),"PilotsFed":(1.0,0.5,0.0),
}
MAP_SECURITY = {
    "High":(0.0,0.3,1.0),"Medium":(0.0,1.0,1.0),"Low":(0.0,1.0,0.0),
    "Anarchy":(1.0,0.0,0.0),"None":(0.5,0.5,0.5),
}
MAP_STAR_CLASS = {
    "O":(0.3,0.5,1.0),"B":(0.2,0.4,1.0),"A":(0.4,0.3,1.0),"F":(0.6,0.6,0.8),
    "G":(0.5,0.5,0.0),"K":(0.7,0.3,0.0),"M":(0.7,0.0,0.0),"L":(1.0,0.0,0.0),
    "T":(0.5,0.1,0.0),"Y":(0.3,0.05,0.0),"TTS":(0.5,0.2,0.0),"C":(0.4,0.4,0.0),
    "W":(0.7,0.7,0.9),"D":(0.5,0.6,1.0),"N":(0.3,0.3,0.3),"None":(0.5,0.5,0.5),
}
MAP_PP_STATE = {
    "None":(1.0,1.0,1.0),"Unoccupied":(1.0,1.0,1.0),"Expansion":(0.5,0.5,0.5),
    "Contested":(0.4,0.05,0.0),"Exploited":(0.8,0.2,0.0),"Fortified":(0.0,0.7,0.0),"Stronghold":(0.5,0.0,0.8),
}
MAP_PP_POWER = {
    "None":(1.0,1.0,1.0),"Contested":(0.4,0.05,0.0),"Jerome Archer":(1.0,0.0,0.8),
    "Nakato Kaine":(0.6,1.0,0.0),"Zemina Torval":(0.0,0.4,1.0),"Yuri Grom":(1.0,0.5,0.0),
    "Pranav Antal":(1.0,0.9,0.0),"Li Yong-Rui":(0.0,0.8,0.3),"Felicia Winters":(1.0,0.7,0.0),
    "Edmund Mahon":(0.2,0.8,0.0),"Denton Patreus":(0.0,0.8,1.0),"Archon Delaine":(1.0,0.0,0.0),
    "Aisling Duval":(0.4,0.8,1.0),"Arissa Lavigny-Duval":(0.6,0.0,1.0),
}

def _bright(d,b=0.58): return {k:(round(r+(1-r)*b,4),round(g+(1-g)*b,4),round(bl+(1-bl)*b,4)) for k,(r,g,bl) in d.items()}
def _dark(d,b=0.42):   return {k:(round(r*b,4),round(g*b,4),round(bl*b,4)) for k,(r,g,bl) in d.items()}

BRIGHT_ECONOMY=_bright(MAP_ECONOMY); BRIGHT_GOVERNMENT=_bright(MAP_GOVERNMENT); BRIGHT_STATE=_bright(MAP_STATE)
BRIGHT_ALLEGIANCE=_bright(MAP_ALLEGIANCE); BRIGHT_SECURITY=_bright(MAP_SECURITY); BRIGHT_STAR_CLASS=_bright(MAP_STAR_CLASS)
BRIGHT_PP_STATE=_bright(MAP_PP_STATE); BRIGHT_PP_POWER=_bright(MAP_PP_POWER)
DARK_ECONOMY=_dark(MAP_ECONOMY); DARK_GOVERNMENT=_dark(MAP_GOVERNMENT); DARK_STATE=_dark(MAP_STATE)
DARK_ALLEGIANCE=_dark(MAP_ALLEGIANCE); DARK_SECURITY=_dark(MAP_SECURITY); DARK_STAR_CLASS=_dark(MAP_STAR_CLASS)
DARK_PP_STATE=_dark(MAP_PP_STATE); DARK_PP_POWER=_dark(MAP_PP_POWER)

ORANGES_ECONOMY = {
    "None":(0.55,0.45,0.30),"Tourism":(0.85,0.35,0.10),"Service":(0.75,0.50,0.20),
    "Refinery":(1.0,0.55,0.05),"Extraction":(0.90,0.25,0.05),"Industrial":(1.0,0.75,0.05),
    "Agriculture":(0.65,0.60,0.08),"HighTech":(1.0,0.65,0.15),"Colony":(0.70,0.55,0.25),
    "Military":(0.80,0.20,0.08),"Terraforming":(0.72,0.65,0.10),"Prison":(0.35,0.28,0.18),
    "Damaged":(0.15,0.10,0.05),"Rescue":(1.0,0.80,0.10),
}
ORANGES_GOVERNMENT = {
    "None":(0.95,0.88,0.75),"Anarchy":(1.0,0.42,0.02),"Colony":(0.80,0.68,0.12),
    "Democracy":(0.72,0.65,0.08),"Imperial":(0.85,0.62,0.10),"Corporate":(0.78,0.58,0.18),
    "Communism":(0.72,0.55,0.22),"Feudal":(0.65,0.52,0.28),"Dictatorship":(0.55,0.38,0.15),
    "Theocracy":(0.75,0.40,0.12),"Cooperative":(0.82,0.48,0.08),"Patronage":(0.78,0.35,0.10),
    "Confederacy":(0.92,0.22,0.05),"PrisonColony":(0.85,0.35,0.05),"Engineer":(0.50,0.42,0.28),
}
ORANGES_STATE = {
    "None":(0.95,0.88,0.75),"Retreat":(0.92,0.18,0.05),"War":(1.0,0.42,0.02),
    "Lockdown":(1.0,0.75,0.05),"CivilUnrest":(0.85,0.65,0.08),"CivilWar":(0.68,0.60,0.08),
    "Boom":(1.0,0.80,0.15),"Expansion":(0.75,0.60,0.20),"Bust":(0.50,0.38,0.15),
    "Outbreak":(0.72,0.32,0.08),"Famine":(0.60,0.28,0.08),"Election":(0.70,0.50,0.15),
    "Investment":(0.80,0.72,0.50),"CivilLiberty":(0.90,0.48,0.12),"Incursion":(0.88,0.52,0.20),
    "Blight":(0.65,0.42,0.18),"NaturalDisaster":(0.92,0.18,0.05),"InfrastructureFailure":(0.78,0.45,0.08),
    "Drought":(0.82,0.68,0.08),"TerroristAttack":(0.48,0.38,0.22),"PublicHoliday":(1.0,0.72,0.08),
    "ThargoidAlert":(1.0,0.75,0.05),"ThargoidInvasion":(1.0,0.42,0.02),"ThargoidControlled":(0.78,0.55,0.08),
    "ThargoidTitan":(0.92,0.18,0.05),"PostThargoidRecovery":(0.65,0.50,0.18),"Counterstrike":(0.72,0.65,0.10),
}
ORANGES_ALLEGIANCE = {
    "None":(0.55,0.45,0.30),"Federation":(0.90,0.20,0.05),"Empire":(0.60,0.48,0.25),
    "Alliance":(0.70,0.62,0.10),"Independent":(1.0,0.75,0.05),"PilotsFed":(1.0,0.50,0.05),
}
ORANGES_SECURITY = {
    "High":(0.55,0.42,0.20),"Medium":(0.85,0.68,0.12),"Low":(1.0,0.55,0.05),
    "Anarchy":(0.90,0.18,0.05),"None":(0.50,0.40,0.25),
}
ORANGES_STAR_CLASS = {
    "O":(0.70,0.60,0.85),"B":(0.65,0.58,0.80),"A":(0.72,0.62,0.75),"F":(0.80,0.72,0.55),
    "G":(1.0,0.80,0.15),"K":(1.0,0.55,0.08),"M":(0.95,0.32,0.05),"L":(0.82,0.22,0.05),
    "T":(0.65,0.18,0.05),"Y":(0.45,0.12,0.05),"TTS":(0.68,0.28,0.08),"C":(0.60,0.50,0.15),
    "W":(0.85,0.80,0.70),"D":(0.78,0.72,0.85),"N":(0.40,0.32,0.22),"None":(0.50,0.40,0.25),
}
ORANGES_PP_STATE = {
    "None":(0.95,0.88,0.75),"Unoccupied":(0.95,0.88,0.75),"Expansion":(0.55,0.45,0.28),
    "Contested":(0.42,0.15,0.05),"Exploited":(0.92,0.38,0.05),"Fortified":(0.72,0.62,0.10),"Stronghold":(1.0,0.62,0.05),
}
ORANGES_PP_POWER = {
    "None":(0.95,0.88,0.75),"Contested":(0.42,0.15,0.05),"Jerome Archer":(0.90,0.28,0.08),
    "Nakato Kaine":(0.78,0.68,0.10),"Zemina Torval":(0.60,0.50,0.28),"Yuri Grom":(1.0,0.50,0.05),
    "Pranav Antal":(1.0,0.78,0.08),"Li Yong-Rui":(0.68,0.60,0.10),"Felicia Winters":(1.0,0.70,0.05),
    "Edmund Mahon":(0.72,0.65,0.08),"Denton Patreus":(0.65,0.52,0.30),"Archon Delaine":(0.95,0.20,0.05),
    "Aisling Duval":(0.82,0.72,0.50),"Arissa Lavigny-Duval":(0.80,0.42,0.10),
}
VAPOR_ECONOMY = {
    "None":(0.55,0.52,0.62),"Tourism":(0.72,0.18,0.88),"Service":(0.18,0.38,0.95),
    "Refinery":(1.0,0.45,0.35),"Extraction":(1.0,0.15,0.35),"Industrial":(1.0,0.75,0.18),
    "Agriculture":(0.15,0.92,0.62),"HighTech":(0.22,0.95,0.92),"Colony":(0.28,0.42,0.98),
    "Military":(0.95,0.15,0.88),"Terraforming":(0.52,0.95,0.42),"Prison":(0.28,0.25,0.38),
    "Damaged":(0.12,0.08,0.18),"Rescue":(1.0,0.78,0.18),
}
VAPOR_GOVERNMENT = {
    "None":(0.90,0.88,0.98),"Anarchy":(1.0,0.42,0.28),"Colony":(0.68,0.88,0.32),
    "Democracy":(0.12,0.95,0.55),"Imperial":(0.18,0.85,0.48),"Corporate":(0.12,0.78,0.68),
    "Communism":(0.12,0.82,0.82),"Feudal":(0.32,0.52,0.98),"Dictatorship":(0.08,0.18,0.95),
    "Theocracy":(0.52,0.18,0.98),"Cooperative":(0.72,0.18,0.98),"Patronage":(0.88,0.18,0.88),
    "Confederacy":(0.98,0.12,0.38),"PrisonColony":(1.0,0.28,0.22),"Engineer":(0.55,0.52,0.68),
}
VAPOR_STATE = {
    "None":(0.90,0.88,0.98),"Retreat":(0.98,0.12,0.38),"War":(1.0,0.38,0.22),
    "Lockdown":(1.0,0.78,0.18),"CivilUnrest":(0.72,0.88,0.22),"CivilWar":(0.12,0.95,0.55),
    "Boom":(0.12,0.92,0.95),"Expansion":(0.28,0.48,0.98),"Bust":(0.08,0.18,0.95),
    "Outbreak":(0.52,0.15,0.95),"Famine":(0.72,0.12,0.95),"Election":(0.72,0.38,0.18),
    "Investment":(0.82,0.80,0.92),"CivilLiberty":(0.98,0.18,0.62),"Incursion":(0.98,0.48,0.82),
    "Blight":(0.82,0.42,0.88),"NaturalDisaster":(0.98,0.12,0.38),"InfrastructureFailure":(0.88,0.35,0.18),
    "Drought":(0.12,0.95,0.55),"TerroristAttack":(0.55,0.52,0.65),"PublicHoliday":(0.65,0.18,0.88),
    "ThargoidAlert":(1.0,0.78,0.18),"ThargoidInvasion":(1.0,0.38,0.22),"ThargoidControlled":(0.72,0.88,0.22),
    "ThargoidTitan":(0.98,0.12,0.38),"PostThargoidRecovery":(0.72,0.12,0.95),"Counterstrike":(0.12,0.95,0.55),
}
VAPOR_ALLEGIANCE = {
    "None":(0.55,0.52,0.62),"Federation":(0.98,0.12,0.38),"Empire":(0.08,0.22,0.95),
    "Alliance":(0.12,0.95,0.55),"Independent":(1.0,0.78,0.18),"PilotsFed":(1.0,0.42,0.28),
}
VAPOR_SECURITY = {
    "High":(0.08,0.22,0.95),"Medium":(0.12,0.92,0.95),"Low":(0.12,0.95,0.55),
    "Anarchy":(0.98,0.12,0.38),"None":(0.55,0.52,0.62),
}
VAPOR_STAR_CLASS = {
    "O":(0.42,0.55,0.98),"B":(0.28,0.40,0.98),"A":(0.52,0.35,0.98),"F":(0.68,0.65,0.88),
    "G":(0.62,0.58,0.25),"K":(0.82,0.38,0.18),"M":(0.82,0.15,0.28),"L":(0.98,0.12,0.38),
    "T":(0.62,0.18,0.22),"Y":(0.42,0.12,0.18),"TTS":(0.62,0.28,0.22),"C":(0.52,0.48,0.18),
    "W":(0.78,0.75,0.95),"D":(0.48,0.62,0.98),"N":(0.35,0.32,0.45),"None":(0.55,0.52,0.62),
}
VAPOR_PP_STATE = {
    "None":(0.90,0.88,0.98),"Unoccupied":(0.90,0.88,0.98),"Expansion":(0.55,0.52,0.65),
    "Contested":(0.48,0.08,0.12),"Exploited":(0.88,0.25,0.22),"Fortified":(0.12,0.78,0.45),"Stronghold":(0.62,0.12,0.88),
}
VAPOR_PP_POWER = {
    "None":(0.90,0.88,0.98),"Contested":(0.48,0.08,0.12),"Jerome Archer":(0.98,0.12,0.82),
    "Nakato Kaine":(0.68,0.98,0.22),"Zemina Torval":(0.08,0.32,0.98),"Yuri Grom":(0.98,0.48,0.22),
    "Pranav Antal":(1.0,0.78,0.18),"Li Yong-Rui":(0.12,0.85,0.48),"Felicia Winters":(1.0,0.72,0.15),
    "Edmund Mahon":(0.28,0.85,0.22),"Denton Patreus":(0.12,0.82,0.98),"Archon Delaine":(0.98,0.12,0.28),
    "Aisling Duval":(0.48,0.82,0.98),"Arissa Lavigny-Duval":(0.68,0.12,0.98),
}

def _mk(e,g,s,a,sec,sc,pp,ppp):
    return {"Economy":e,"Government":g,"State":s,"Allegiance":a,"Security":sec,"Star Class":sc,"Powerplay State":pp,"Powerplay Power":ppp}

PALETTES = {
    "map":       _mk(MAP_ECONOMY,MAP_GOVERNMENT,MAP_STATE,MAP_ALLEGIANCE,MAP_SECURITY,MAP_STAR_CLASS,MAP_PP_STATE,MAP_PP_POWER),
    "bright":    _mk(BRIGHT_ECONOMY,BRIGHT_GOVERNMENT,BRIGHT_STATE,BRIGHT_ALLEGIANCE,BRIGHT_SECURITY,BRIGHT_STAR_CLASS,BRIGHT_PP_STATE,BRIGHT_PP_POWER),
    "dark":      _mk(DARK_ECONOMY,DARK_GOVERNMENT,DARK_STATE,DARK_ALLEGIANCE,DARK_SECURITY,DARK_STAR_CLASS,DARK_PP_STATE,DARK_PP_POWER),
    "oranges":   _mk(ORANGES_ECONOMY,ORANGES_GOVERNMENT,ORANGES_STATE,ORANGES_ALLEGIANCE,ORANGES_SECURITY,ORANGES_STAR_CLASS,ORANGES_PP_STATE,ORANGES_PP_POWER),
    "vaporwave": _mk(VAPOR_ECONOMY,VAPOR_GOVERNMENT,VAPOR_STATE,VAPOR_ALLEGIANCE,VAPOR_SECURITY,VAPOR_STAR_CLASS,VAPOR_PP_STATE,VAPOR_PP_POWER),
}

DEFAULT_COLOUR = (1.0,1.0,1.0)
SOURCE_NAMES     = ["Off","Economy","Government","State","Allegiance","Security","Star Class","Powerplay State","Powerplay Power"]
ALL_SOURCE_NAMES = SOURCE_NAMES + ["Custom"]

ENVIRONMENTAL_ELEMENTS = [
    {"label":"Orbit Lines",                      "keys":[("x39","y39","z39")]},
    {"label":"Gravity Lines",                    "keys":[("x40","y40","z40")]},
    {"label":"Destination Target & Mouse Arrow", "keys":[("x65","y65","z65")]},
    {"label":"Possible SC Target Circle",        "keys":[("x66","y66","z66")]},
    {"label":"Destination Target Circle",        "keys":[("x67","y67","z67")]},
]
SHIP_HUD_ELEMENTS = [
    {"label":"Night Vision",         "keys":[("x43","y43","z43")]},
    {"label":"Panel Icons",          "keys":[("x53","y53","z53")]},
    {"label":"Supercruise Sidelines","keys":[("x176","y176","z176")]},
    {"label":"Signature Bar",        "keys":[("x206","y206","z206")]},
    {"label":"Radar Outer Rim",      "keys":[("x236","y236","z236")]},
    {"label":"Radar Grid",           "keys":[("x237","y237","z237")]},
    {"label":"Player Ship Hologram", "keys":[("x248","y248","z248")]},
]
UI_ELEMENTS = ENVIRONMENTAL_ELEMENTS + SHIP_HUD_ELEMENTS

STATE_PRIORITY = [
    "ThargoidTitan","ThargoidControlled","ThargoidInvasion","ThargoidAlert",
    "Retreat","War","CivilWar","Lockdown","Outbreak","Famine",
    "NaturalDisaster","InfrastructureFailure","TerroristAttack","Blight",
    "Drought","CivilUnrest","Incursion","Bust","PostThargoidRecovery",
    "Counterstrike","Election","CivilLiberty","PublicHoliday",
    "Expansion","Investment","Boom","None"
]

CONFIG_FILE = os.path.join(
    os.environ.get("APPDATA",os.path.expanduser("~")),
    "ED_HUD_Mod","config.json"
)

# =============================================
# HELPERS
# =============================================

def get_edhm_paths(folder):
    ini=os.path.join(folder,"Advanced.ini"); theme=os.path.join(folder,"ThemeSettings.json")
    return (ini,theme) if os.path.isfile(ini) and os.path.isfile(theme) else (None,None)

def get_latest_journal(d):
    try:
        files=[os.path.join(d,f) for f in os.listdir(d) if f.startswith("Journal.") and f.endswith(".log")]
        return max(files,key=os.path.getmtime) if files else None
    except: return None

def get_last_fsd_jump(d):
    try: files=sorted([os.path.join(d,f) for f in os.listdir(d) if f.startswith("Journal.") and f.endswith(".log")],key=os.path.getmtime,reverse=True)
    except: return None
    for fp in files:
        try:
            with open(fp,"r",encoding="utf-8") as f:
                for line in reversed(f.readlines()):
                    line=line.strip()
                    if not line: continue
                    try:
                        ev=json.loads(line)
                        if ev.get("event")=="FSDJump": return ev
                    except: continue
        except: continue
    return None

def get_last_star_class(d):
    try: files=sorted([os.path.join(d,f) for f in os.listdir(d) if f.startswith("Journal.") and f.endswith(".log")],key=os.path.getmtime,reverse=True)
    except: return "None"
    for fp in files:
        try:
            with open(fp,"r",encoding="utf-8") as f:
                for line in reversed(f.readlines()):
                    line=line.strip()
                    if not line: continue
                    try:
                        ev=json.loads(line)
                        if ev.get("event")=="StartJump" and ev.get("JumpType")=="Hyperspace":
                            return parse_star_class(ev.get("StarClass",""))
                    except: continue
        except: continue
    return "None"

def parse_economy(r):
    if not r: return "None"
    c=r.replace("$economy_","").replace(";","").strip()
    return {"Agri":"Agriculture","Extraction":"Extraction","Refinery":"Refinery","Industrial":"Industrial","HighTech":"HighTech","Military":"Military","Tourism":"Tourism","Service":"Service","Colony":"Colony","Terraforming":"Terraforming","Prison":"Prison","Damaged":"Damaged","Rescue":"Rescue","None":"None"}.get(c,"None")

def parse_government(r):
    if not r: return "None"
    c=r.replace("$government_","").replace(";","").strip()
    return {"Anarchy":"Anarchy","Colony":"Colony","Democracy":"Democracy","Imperial":"Imperial","Corporate":"Corporate","Communism":"Communism","Feudal":"Feudal","Dictatorship":"Dictatorship","Theocracy":"Theocracy","Cooperative":"Cooperative","Patronage":"Patronage","Confederacy":"Confederacy","PrisonColony":"PrisonColony","Workshop":"Engineer","Engineer":"Engineer","None":"None"}.get(c,"None")

def parse_state(factions):
    if not factions: return "None"
    active=set()
    for f in factions:
        for e in f.get("ActiveStates",[]):
            s=e.get("State","")
            if s: active.add(s)
    for s in STATE_PRIORITY:
        if s in active: return s
    return "None"

def parse_allegiance(r):
    if not r: return "None"
    return {"Federation":"Federation","Empire":"Empire","Alliance":"Alliance","Independent":"Independent","PilotsFederation":"PilotsFed","None":"None"}.get(r,"None")

def parse_security(r):
    if not r: return "None"
    c=r.lower().replace(";","").strip()
    for p in ["$system_security_","$galaxy_map_info_state_security_","$galagy_map_info_state_security_"]: c=c.replace(p,"")
    return {"high":"High","medium":"Medium","low":"Low","anarchy":"Anarchy","lawless":"Anarchy"}.get(c,"None")

def parse_star_class(r):
    if not r: return "None"
    u=r.upper()
    for p in ["TTS","W","D","N"]:
        if u.startswith(p): return p
    return u[0] if u and u[0] in MAP_STAR_CLASS else "None"

def parse_powerplay_state(r):
    if not r: return "None"
    return {"Unoccupied":"Unoccupied","Expansion":"Expansion","Contested":"Contested","Exploited":"Exploited","Fortified":"Fortified","Stronghold":"Stronghold"}.get(r,"None")

def parse_powerplay_power(powers,state):
    if not powers: return "None"
    if state=="Contested" or len(powers)>1: return "Contested"
    return powers[0] if powers[0] in MAP_PP_POWER else "None"

def write_ini_colour(path,xk,yk,zk,r,g,b):
    with open(path,"r",encoding="utf-8") as f: c=f.read()
    c=re.sub(rf"(?m)^{xk}\s*=.*$",f"{xk} = {r}",c)
    c=re.sub(rf"(?m)^{yk}\s*=.*$",f"{yk} = {g}",c)
    c=re.sub(rf"(?m)^{zk}\s*=.*$",f"{zk} = {b}",c)
    with open(path,"w",encoding="utf-8") as f: f.write(c)

def touch_theme_json(path): os.utime(path,None)

def float_to_hex(r,g,b):
    cl=lambda v:min(255,max(0,int(v*255)))
    return f"#{cl(r):02x}{cl(g):02x}{cl(b):02x}"

class Tooltip:
    """Simple hover tooltip for any widget."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text   = text
        self.tip    = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(self.tip, text=self.text, background="#ffffe0",
                       foreground="#333333", relief="solid", borderwidth=1,
                       font=("TkDefaultFont", 8), padx=6, pady=4)
        lbl.pack()

    def hide(self, event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None




class EDHudModApp:

    def __init__(self,root):
        self.root=root
        self.root.title("EDHM-UI System Hue Updater  v3.2")
        self.root.iconbitmap("edhm_icon.ico")
        self.root.minsize(900,500)
        self.root.geometry("1100x500")

        self.running           = False
        self.watcher_thread    = None
        self._updating_all     = False
        self.cached_star_class = "None"
        self.palette_mode      = "map"
        self.active_page       = "hud"

        self.edhm_ini_folder = tk.StringVar()
        self.journal_dir     = tk.StringVar()
        self.all_env_source  = tk.StringVar(value="Off")
        self.all_ship_source = tk.StringVar(value="Off")
        self.mappings        = [tk.StringVar(value="Off") for _ in UI_ELEMENTS]
        self.custom_env_preset  = ["Off"]*len(ENVIRONMENTAL_ELEMENTS)
        self.custom_ship_preset = ["Off"]*len(SHIP_HUD_ELEMENTS)

        self.status_vars = {k:tk.StringVar(value="—") for k in [
            "System","Economy","Government","Allegiance",
            "Security","State","Star Class","PP State","PP Power"]}

        self.current_values = {k:"None" for k in [
            "Economy","Government","State","Allegiance",
            "Security","Star Class","Powerplay State","Powerplay Power"]}

        self.swatches         = {}
        self.element_swatches = []
        self.palette_btns     = {}
        self.page_btns        = {}

        self.load_config()
        self.build_ui()

        for var in self.mappings:
            var.trace_add("write",self._on_individual_change)

        self.root.after(200,self.start)

    # ------------------------------------------
    # CONFIG
    # ------------------------------------------

    def load_config(self):
        if not os.path.exists(CONFIG_FILE): return
        try:
            with open(CONFIG_FILE,"r") as f: data=json.load(f)
            self.edhm_ini_folder.set(data.get("edhm_ini_folder",""))
            self.journal_dir.set(data.get("journal_dir",""))
            self.all_env_source.set(data.get("all_env_source","Off"))
            self.all_ship_source.set(data.get("all_ship_source","Off"))
            self.palette_mode=data.get("palette_mode","map")
            self.custom_env_preset =data.get("custom_env_preset", ["Off"]*len(ENVIRONMENTAL_ELEMENTS))
            self.custom_ship_preset=data.get("custom_ship_preset",["Off"]*len(SHIP_HUD_ELEMENTS))
            for i,val in enumerate(data.get("mappings",[])):
                if i<len(self.mappings): self.mappings[i].set(val)
        except: pass

    def save_config(self):
        os.makedirs(os.path.dirname(CONFIG_FILE),exist_ok=True)
        with open(CONFIG_FILE,"w") as f:
            json.dump({"edhm_ini_folder":self.edhm_ini_folder.get(),"journal_dir":self.journal_dir.get(),
                       "all_env_source":self.all_env_source.get(),"all_ship_source":self.all_ship_source.get(),
                       "palette_mode":self.palette_mode,"custom_env_preset":self.custom_env_preset,
                       "custom_ship_preset":self.custom_ship_preset,
                       "mappings":[m.get() for m in self.mappings]},f,indent=4)

    # ------------------------------------------
    # UI BUILD
    # ------------------------------------------

    def build_ui(self):
        pad={"padx":8,"pady":4}

        # ── File paths ──
        pf=ttk.LabelFrame(self.root,text="File Paths")
        pf.grid(row=0,column=0,sticky="ew",**pad)
        pf.columnconfigure(1,weight=1); pf.columnconfigure(4,weight=1)

        ttk.Label(pf,text="EDHM-ini Folder",width=16,anchor="w").grid(row=0,column=0,padx=(8,4),pady=6)
        ttk.Entry(pf,textvariable=self.edhm_ini_folder).grid(row=0,column=1,padx=4,pady=6,sticky="ew")
        ttk.Button(pf,text="Browse",width=8,command=self.browse_edhm).grid(row=0,column=2,padx=(4,4),pady=6)
        edhm_info=tk.Label(pf,text="ⓘ",foreground="#888888",cursor="question_arrow")
        edhm_info.grid(row=0,column=3,padx=(0,16),pady=6)
        Tooltip(edhm_info,"eg. C:/Users/YourName/EDHM_UI/ODYSS/EDHM/EDHM-Ini")

        ttk.Label(pf,text="ED Journal Folder",width=16,anchor="w").grid(row=0,column=4,padx=(0,4),pady=6)
        ttk.Entry(pf,textvariable=self.journal_dir).grid(row=0,column=5,padx=4,pady=6,sticky="ew")
        ttk.Button(pf,text="Browse",width=8,command=self.browse_journal).grid(row=0,column=6,padx=(4,4),pady=6)
        jour_info=tk.Label(pf,text="ⓘ",foreground="#888888",cursor="question_arrow")
        jour_info.grid(row=0,column=7,padx=(0,8),pady=6)
        Tooltip(jour_info,"eg. C:/Users/YourName/Saved Games/Frontier Developments/Elite Dangerous")

        pf.columnconfigure(1,weight=1); pf.columnconfigure(5,weight=1)

        # ── Page buttons ──
        nbf=ttk.Frame(self.root)
        nbf.grid(row=1,column=0,sticky="ew",padx=8,pady=(4,0))

        for key,label in [("hud","HUD"),("system","Current System")]:
            btn=ttk.Button(nbf,text=label,command=lambda k=key:self._show_page(k))
            btn.pack(side="left",padx=(0,4))
            self.page_btns[key]=btn

        # ── Palette buttons ──
        pbf=ttk.LabelFrame(self.root,text="Colour Palette")
        pbf.grid(row=2,column=0,sticky="ew",**pad)

        for key,label in [("map","ED Starmap"),("bright","BRIGHT"),("dark","DARK"),("oranges","ORANGES"),("vaporwave","VAPORWAVE")]:
            btn=ttk.Button(pbf,text=label,command=lambda k=key:self.set_palette(k))
            btn.pack(side="left",padx=4,pady=6)
            self.palette_btns[key]=btn

        # ── Page container ──
        self.page_frame=ttk.Frame(self.root)
        self.page_frame.grid(row=3,column=0,sticky="nsew",padx=8,pady=4)
        self.root.grid_rowconfigure(3,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.page_frame.grid_rowconfigure(0,weight=1)
        self.page_frame.grid_columnconfigure(0,weight=1)

        self._build_hud_page()
        self._build_system_page()

        # ── Bottom bar ──
        # Row A — Apply Now centred
        af=ttk.Frame(self.root)
        af.grid(row=4,column=0,sticky="ew",padx=8,pady=(4,0))
        af.columnconfigure(0,weight=1)
        ttk.Button(af,text="Apply Now",width=30,command=self.apply_now).grid(row=0,column=0,pady=4)

        # Row B — status label left of On/Off, both on right
        bf=ttk.Frame(self.root)
        bf.grid(row=5,column=0,sticky="ew",padx=8,pady=(0,8))
        bf.columnconfigure(0,weight=1)
        self.status_label=ttk.Label(bf,text="Stopped",foreground="gray",anchor="e")
        self.status_label.grid(row=0,column=0,padx=(4,4),pady=4,sticky="e")
        self.toggle_btn=ttk.Button(bf,text="Off",width=6,command=self.toggle)
        self.toggle_btn.grid(row=0,column=1,pady=4,sticky="e")

        self._update_palette_buttons()
        self._show_page("hud")

    def _build_hud_page(self):
        self.hud_page=ttk.Frame(self.page_frame)
        self.hud_page.grid(row=0,column=0,sticky="nsew")
        self.hud_page.grid_rowconfigure(0,weight=1)
        self.hud_page.grid_columnconfigure(0,weight=1)
        self.hud_page.grid_columnconfigure(1,weight=1)

        ec=len(ENVIRONMENTAL_ELEMENTS)

        # Environmental panel
        ef=ttk.LabelFrame(self.hud_page,text="Environmental")
        ef.grid(row=0,column=0,sticky="nsew",padx=(0,4))
        ef.columnconfigure(1,weight=1)

        ttk.Label(ef,text="All Environmental",anchor="w",font=("TkDefaultFont",9,"bold")).grid(row=0,column=0,padx=8,pady=(6,2),sticky="w")
        env_cb=ttk.Combobox(ef,textvariable=self.all_env_source,values=ALL_SOURCE_NAMES,state="readonly",width=16)
        env_cb.grid(row=0,column=1,padx=8,pady=(6,2))
        env_cb.bind("<<ComboboxSelected>>",lambda e:self._on_env_all_change())

        ttk.Separator(ef,orient="horizontal").grid(row=1,column=0,columnspan=3,sticky="ew",padx=8,pady=4)

        for i,el in enumerate(ENVIRONMENTAL_ELEMENTS):
            ttk.Label(ef,text=el["label"],anchor="w").grid(row=i+2,column=0,padx=8,pady=3,sticky="w")
            cb=ttk.Combobox(ef,textvariable=self.mappings[i],values=SOURCE_NAMES,state="readonly",width=16)
            cb.grid(row=i+2,column=1,padx=8,pady=3)
            sw=tk.Label(ef,width=3,bg="#404040",relief="flat")
            sw.grid(row=i+2,column=2,padx=(0,8),pady=3,sticky="e")
            self.element_swatches.append(sw)

        # Ship HUD panel
        sf=ttk.LabelFrame(self.hud_page,text="Ship HUD")
        sf.grid(row=0,column=1,sticky="nsew",padx=(4,0))
        sf.columnconfigure(1,weight=1)

        ttk.Label(sf,text="All Ship HUD",anchor="w",font=("TkDefaultFont",9,"bold")).grid(row=0,column=0,padx=8,pady=(6,2),sticky="w")
        ship_cb=ttk.Combobox(sf,textvariable=self.all_ship_source,values=ALL_SOURCE_NAMES,state="readonly",width=16)
        ship_cb.grid(row=0,column=1,padx=8,pady=(6,2))
        ship_cb.bind("<<ComboboxSelected>>",lambda e:self._on_ship_all_change())

        ttk.Separator(sf,orient="horizontal").grid(row=1,column=0,columnspan=3,sticky="ew",padx=8,pady=4)

        for i,el in enumerate(SHIP_HUD_ELEMENTS):
            idx=ec+i
            ttk.Label(sf,text=el["label"],anchor="w").grid(row=i+2,column=0,padx=8,pady=3,sticky="w")
            cb=ttk.Combobox(sf,textvariable=self.mappings[idx],values=SOURCE_NAMES,state="readonly",width=16)
            cb.grid(row=i+2,column=1,padx=8,pady=3)
            sw=tk.Label(sf,width=3,bg="#404040",relief="flat")
            sw.grid(row=i+2,column=2,padx=(0,8),pady=3,sticky="e")
            self.element_swatches.append(sw)

    def _build_system_page(self):
        self.system_page=ttk.Frame(self.page_frame)
        self.system_page.grid(row=0,column=0,sticky="nsew")

        sf=ttk.LabelFrame(self.system_page,text="Current System")
        sf.grid(row=0,column=0,sticky="nsew",padx=0,pady=0)
        self.system_page.grid_rowconfigure(0,weight=1)
        self.system_page.grid_columnconfigure(0,weight=1)
        sf.columnconfigure(1,weight=1)

        rows=[("System",None),("Economy","Economy"),("Government","Government"),
              ("Allegiance","Allegiance"),("Security","Security"),("State","State"),
              ("Star Class","Star Class"),("PP State","Powerplay State"),("PP Power","Powerplay Power")]

        for i,(label,source_key) in enumerate(rows):
            ttk.Label(sf,text=label+":",width=12,anchor="w").grid(row=i,column=0,padx=(12,4),pady=3,sticky="w")
            ttk.Label(sf,textvariable=self.status_vars[label],anchor="w",width=28).grid(row=i,column=1,padx=4,pady=3,sticky="w")
            if source_key:
                sw=tk.Label(sf,width=3,bg="#404040",relief="flat")
                sw.grid(row=i,column=2,padx=(0,12),pady=3,sticky="e")
                self.swatches[source_key]=sw

    # ------------------------------------------
    # PAGE SWITCHING
    # ------------------------------------------

    def _show_page(self,key):
        self.active_page=key
        self.hud_page.grid_remove()
        self.system_page.grid_remove()
        if key=="hud": self.hud_page.grid()
        else:          self.system_page.grid()
        for k,btn in self.page_btns.items():
            btn.state(["pressed"] if k==key else ["!pressed"])

    # ------------------------------------------
    # PALETTE
    # ------------------------------------------

    def get_source_maps(self): return PALETTES[self.palette_mode]

    def set_palette(self,mode):
        self.palette_mode=mode
        self._update_palette_buttons()
        self._update_swatches()
        self.save_config()

    def _update_palette_buttons(self):
        for key,btn in self.palette_btns.items():
            btn.state(["pressed"] if key==self.palette_mode else ["!pressed"])

    # ------------------------------------------
    # ALL / CUSTOM / INDIVIDUAL
    # ------------------------------------------

    def _on_env_all_change(self):
        sel=self.all_env_source.get(); ec=len(ENVIRONMENTAL_ELEMENTS)
        if sel=="Custom":
            self._updating_all=True
            for i,v in enumerate(self.custom_env_preset):
                if i<ec: self.mappings[i].set(v)
            self._updating_all=False
        elif sel in SOURCE_NAMES:
            self._updating_all=True
            for i in range(ec): self.mappings[i].set(sel)
            self._updating_all=False
        self._update_swatches()

    def _on_ship_all_change(self):
        sel=self.all_ship_source.get(); ec=len(ENVIRONMENTAL_ELEMENTS); sc=len(SHIP_HUD_ELEMENTS)
        if sel=="Custom":
            self._updating_all=True
            for i,v in enumerate(self.custom_ship_preset):
                if i<sc: self.mappings[ec+i].set(v)
            self._updating_all=False
        elif sel in SOURCE_NAMES:
            self._updating_all=True
            for i in range(sc): self.mappings[ec+i].set(sel)
            self._updating_all=False
        self._update_swatches()

    def _on_individual_change(self,*args):
        if self._updating_all: return
        ec=len(ENVIRONMENTAL_ELEMENTS); sc=len(SHIP_HUD_ELEMENTS)
        ev=[self.mappings[i].get() for i in range(ec)]
        sv=[self.mappings[ec+i].get() for i in range(sc)]
        self.all_env_source.set(ev[0] if len(set(ev))==1 else "Custom")
        if len(set(ev))!=1: self.custom_env_preset=ev[:]
        self.all_ship_source.set(sv[0] if len(set(sv))==1 else "Custom")
        if len(set(sv))!=1: self.custom_ship_preset=sv[:]
        self._update_swatches()

    # ------------------------------------------
    # SWATCHES
    # ------------------------------------------

    def _update_swatches(self):
        sm=self.get_source_maps()
        for sk,sw in self.swatches.items():
            cm=sm.get(sk)
            if not cm: sw.config(bg="#404040"); continue
            rgb=cm.get(self.current_values.get(sk,"None"),DEFAULT_COLOUR)
            sw.config(bg=float_to_hex(*rgb))
        for i,sw in enumerate(self.element_swatches):
            src=self.mappings[i].get()
            if src=="Off" or src not in sm: sw.config(bg="#404040"); continue
            rgb=sm[src].get(self.current_values.get(src,"None"),DEFAULT_COLOUR)
            sw.config(bg=float_to_hex(*rgb))

    # ------------------------------------------
    # BROWSE
    # ------------------------------------------

    def browse_edhm(self):
        p=filedialog.askdirectory(title="Select EDHM-Ini Folder")
        if p: self.edhm_ini_folder.set(p)

    def browse_journal(self):
        p=filedialog.askdirectory(title="Select Journal Folder")
        if p: self.journal_dir.set(p)

    def get_paths(self):
        f=self.edhm_ini_folder.get()
        return get_edhm_paths(f) if f else (None,None)

    # ------------------------------------------
    # ON / OFF
    # ------------------------------------------

    def toggle(self):
        if self.running: self.stop()
        else: self.start()

    def start(self):
        self.save_config(); self.running=True
        self.toggle_btn.config(text="Off")
        self.status_label.config(text="Running — watching for jumps...",foreground="green")
        self.watcher_thread=threading.Thread(target=self.watch_loop,daemon=True)
        self.watcher_thread.start()

    def stop(self):
        self.running=False
        self.toggle_btn.config(text="On")
        self.status_label.config(text="Paused",foreground="gray")

    def on_close(self):
        self.save_config(); self.running=False; self.root.destroy()

    # ------------------------------------------
    # APPLY NOW
    # ------------------------------------------

    def apply_now(self):
        ini,theme=self.get_paths()
        if not ini: messagebox.showerror("Error","Advanced.ini or ThemeSettings.json not found.\nCheck your EDHM-Ini folder."); return
        jd=self.journal_dir.get()
        if not jd: messagebox.showerror("Error","Please set the Journal folder."); return
        ev=get_last_fsd_jump(jd)
        if not ev: messagebox.showwarning("No Jump Found","No FSDJump found in journals."); return
        self.cached_star_class=get_last_star_class(jd)
        self._apply_colours(ev,ini,theme)
        self.status_label.config(text="Applied manually.")

    # ------------------------------------------
    # WATCHER
    # ------------------------------------------

    def watch_loop(self):
        last_j=None; last_p=0
        while self.running:
            try:
                cur=get_latest_journal(self.journal_dir.get())
                if cur!=last_j: last_j=cur; last_p=0
                if not cur: time.sleep(2); continue
                with open(cur,"r",encoding="utf-8") as f:
                    f.seek(last_p); lines=f.readlines(); last_p=f.tell()
                for line in lines:
                    line=line.strip()
                    if not line: continue
                    try: ev=json.loads(line)
                    except: continue
                    et=ev.get("event")
                    if et=="StartJump" and ev.get("JumpType")=="Hyperspace":
                        self.cached_star_class=parse_star_class(ev.get("StarClass",""))
                    elif et=="FSDJump":
                        ini,theme=self.get_paths()
                        if ini: self._apply_colours(ev,ini,theme)
            except Exception as e:
                self.root.after(0,lambda e=e:self.status_label.config(text=f"Error: {e}"))
            time.sleep(1)

    # ------------------------------------------
    # COLOUR APPLICATION
    # ------------------------------------------

    def _apply_colours(self,event,ini_path,theme_path):
        sm=self.get_source_maps()
        system=event.get("StarSystem","Unknown")
        vals={
            "Economy":parse_economy(event.get("SystemEconomy","")),
            "Government":parse_government(event.get("SystemGovernment","")),
            "State":parse_state(event.get("Factions",[])),
            "Allegiance":parse_allegiance(event.get("SystemAllegiance","")),
            "Security":parse_security(event.get("SystemSecurity","")),
            "Star Class":self.cached_star_class,
            "Powerplay State":parse_powerplay_state(event.get("PowerplayState","")),
            "Powerplay Power":parse_powerplay_power(event.get("Powers",[]),event.get("PowerplayState","")),
        }
        wrote=False
        for i,el in enumerate(UI_ELEMENTS):
            src=self.mappings[i].get()
            if src=="Off" or src not in sm: continue
            colour=sm[src].get(vals.get(src,"None"),DEFAULT_COLOUR)
            for (xk,yk,zk) in el["keys"]: write_ini_colour(ini_path,xk,yk,zk,*colour)
            wrote=True
        if wrote: touch_theme_json(theme_path)
        self.root.after(0,lambda:self._update_status(system,vals))

    def _update_status(self,system,vals):
        self.status_vars["System"].set(system)
        self.status_vars["Economy"].set(vals["Economy"])
        self.status_vars["Government"].set(vals["Government"])
        self.status_vars["Allegiance"].set(vals["Allegiance"])
        self.status_vars["Security"].set(vals["Security"])
        self.status_vars["State"].set(vals["State"])
        self.status_vars["Star Class"].set(vals["Star Class"])
        self.status_vars["PP State"].set(vals["Powerplay State"])
        self.status_vars["PP Power"].set(vals["Powerplay Power"])
        self.status_label.config(text=f"Last jump: {system}")
        self.current_values={k:vals[k] for k in vals}
        self._update_swatches()


if __name__=="__main__":
    root=tk.Tk()
    app=EDHudModApp(root)
    root.protocol("WM_DELETE_WINDOW",app.on_close)
    root.mainloop()
