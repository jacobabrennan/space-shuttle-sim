

# = Particle ==================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
import random
# Local Modules
from config import *
from vector3d import *


class Particle:

    def __init__(self, position=(0, 0, 0), radius=1):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        self.radius = radius
        self.test_a = 0

    def take_turn(self, game_time):
        self.test_a += 0.1
        if(self.test_a > 100):
            self.test_a = 0

    def sprite(self, radius, position):
        tile = (
            int(((position[0]/radius)+2) * 25),
            int(((position[1]/radius)+1.6) * 16),
        )
        string_index = tile[1]*100 + tile[0] + int(self.test_a)
        # print(string_index, tile)
        return map_earth[string_index]

map_earth = ''.join(reversed([
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    ',,,,,,,,,,,,,,.,..,,,,,,,,,,..,,,,,,,,....,.,,,,,......,,..,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,..,..',
    ',....,.......,,....,=:.~=~I~~.=.,,,,,,,,:::~:, ?7=I 7~,$ 7         IOO~.,.IO7,=,,.,.,......,...,,,.,',
    '=.,?,..,~~,.,,,?+~.::,++I+?=OO  OO~:,,::::7               OO  OO?8 O    ????+????+?$?$ O    O,.,,,,,',
    '+OOO??II77I77I7???7 II7++7+ ++?? OOI.:~:$O O O       8?77I77?  ?II????+I+7?I?IIII?I7IIII?II77?II???I',
    '   77II77III77$$7$77III7O OI+7OI    ~=       O  O O?IIO $$$8$$$$$7$7$7777$$$77777777777I??7?I$IIIIO ',
    '    OIOOOOO $+I $$$ $$77IOO7II7?7O              7OOO$$O7$$$$$$ $$$$$77$7$7777$$$77?7IIII OOOOI$ O   ',
    '          OOO  7 $I??7$$  77$$$$7OO           OOIO77$$$$77777IIIIIII?III$77777$7$77$777$7 OOO       ',
    '            OOO7I$77I?I$$8 $$$7 $O             OO$$I$$$7$7O$II? +=~++??? I7I7?I++??I7$7$OO$O        ',
    '               $???$I?I$$$$$$OOOOO             77$$OOOO$O$?77?$O~=++7?I=+=:=$==+? 7$7 OOI           ',
    '              OO +77II7$$$$$OOOOO               7?+,OOOOOOO7=?I??+=?II7I?=+===$$777 O 7 O           ',
    '                O O7??IOOOOO OOO              +=+~+=++?~~==I~++ +I?==+?7 7?  $ $$77OO               ',
    '                    $IOOOO$ $OO              ~==+=~+++~+=~?++==~+I  OI7777$ $   $ OOOO              ',
    '                     O7$$O  OOOO             ++++==+:~:===++O+=~7OOOOOI7OOOO 77OO O7                ',
    '                       O OO O+ O   O         77IIII???II??I7?$O+O  OOO 7O OOO  $ OO7$               ',
    '                         O  $ 7$7$7OOO        O $ O $$$$$77I7??       O   OOO7OO O$OO               ',
    '                          OI$ OO  $$O           OOO $ O   7$I7 O             $    OOOOO             ',
    '                          OI$ OO   $77?+          OOO7$$$7II OO                OO  O  $O$7 I$       ',
    '                           O?$  $$$$I7?O            O?7II7777O                     OOO   $OOO       ',
    '         $                 O 7+$ $777I$O             ?II77I7 O7                     I?I?O?  OO     $',
    '                            OO?I777777               $???77OOO7                  ?IIII????IO O OO   ',
    '                            OOIII77$  O               ????7                      +IIII7?+I?I        ',
    '                             O?I???                   O7IO                        ??   7I??$        ',
    '                             $?I                                                         O        7 ',
    '                             7IO                                                           O    IO  ',
    '                            O?O                                                                     ',
    '                              O                                                                     ',
    '                                O7                                                                  ',
    '                              :=,                             +:,,$O   O,......,:?,,..,.,, O        ',
    '              7     $:.,,.O~,.,.,O          .,..,..,,,.,:.,,...,,::+=,,....,,,,,,....,:,,,,,,,,:I   ',
    ':~==.,.,::,::~:,,,:,::,,,~,=..,...,.:..:~=:,~:::,,,,,:,,,,,,:::,,..,,,:,:::::::,,,,:,:::::,::~~:....',
    ':,...~~:::~::::,,,:::,,,.:~~~:::~::,,,,,,:~:,::::::::::::::::::::::::::::::::::::~::::,,,,,,,,~=?=~:',
    ',,,,,,,.,.,.,,..,.........,,,,.......,....,....,...,,,,.,,,,,,,,,,,,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
    '####################################################################################################',
]))
