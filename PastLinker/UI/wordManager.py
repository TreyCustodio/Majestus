from os.path import join
from random import randint

"""
Manages words for the game.
"""

class WordManager:

    DIFFICULTY = None

    def setDifficulty(diff = None):
        if WordManager.DIFFICULTY == None:
            WordManager.DIFFICULTY = diff

    def getCommon(sniping = False):
        """
        Return a common word from
        1000-most-common-words.txt
        """
        rand = randint(1,999)
        words = open("words\\common.txt")
        lines = words.readlines()
        line = lines[rand]

        if WordManager.DIFFICULTY == "easy":
            if "'" in line:
                line = lines[rand+1]
        
        if sniping:
            return line[0].upper()
        else:
            string = line[0].upper() + line[1:line.index("\n")]
            return string
    
    def getSeven(hard = False):
        """
        Return a seven letter word.
        If hard: get it from word-list-7-letters.txt
        else:    get it from common-7-letter-words.txt
        """
        rand = randint(1,40093)
        words = open("words\\hard7.txt")
        lines = words.readlines()
        line = lines[rand]
        string = line[0].upper() + line[1:line.index("\n")]
        return string
    
