from enum import Enum

FLOW_RATE = 60.0/100.0  # .6
PUMP_CONFIG_PATH = "./utils/pump_config.json"
PREMADE_DRINKS_PATH = "./utils/premade_drinks.json"

class LiquidType(Enum):
    ALCOHOL = "Alcohol"
    MIXER   = "Mixer"

class StrengthLevel(Enum):
    INVALID     = -1
    EASY_TIGER  = 35
    FIFTY_FIFTY = 50
    LITTY_TITTY = 65
    ADIOS_MF    = 80
    MIXER_LEVEL = 260

SPOTIFY_PLAY_STATE_STYLE = \
" \
QPushButton{\
background-image: url(:/images/images/pause-button.png);\
border-radius:50px;\
max-width:50px;\
max-height:50px;\
min-width:48px;\
min-height:48px;\
}\
\
QPushButton:pressed {\
    border-style: inset;\
    background: qradialgradient(\
        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\
        radius: 1.35, stop: 0, stop: 1\
        );\
    }\
"
SPOTIFY_PAUSED_STATE_STYLE = \
" \
QPushButton{\
background-image: url(:/images/images/play-button.png);\
border-radius:50px;\
max-width:50px;\
max-height:50px;\
min-width:48px;\
min-height:48px;\
}\
\
QPushButton:pressed {\
    border-style: inset;\
    background: qradialgradient(\
        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\
        radius: 1.35, stop: 0, stop: 1\
        );\
    }\
"

SPOTIFY_TAB_STYLE = \
" \
QListWidget{\
color: rgb(255, 255, 255);\
background-color: rgb(0, 0, 0);\
}\
\
QLineEdit{\
color: rgb(0, 0, 0);\
}\
\
QTabWidget{\
color: rgb(255, 255, 255);\
background-color: rgb(0, 0, 0);\
}\
\
QTabBar:Tab{\
color: rgb(255, 255, 255);\
background-color: rgb(0, 0, 0);\
}\
QTabBar:Tab:selected{\
background-color: rgb(117, 116, 115);\
}\
"