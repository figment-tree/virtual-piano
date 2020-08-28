# Virtual Piano (middle octave)

import pygame as pg
from music21 import *
import threading

# mandatory
pg.init()


font = pg.font.Font("fonts/Respective_2.0.ttf", 180)
text = font.render("Virtual Piano", True, (210, 190, 255))
piano = pg.display.set_mode((800, 600))
pg.display.set_caption("Virtual Piano")

keyPad_x = 50
keyPad_y = 200
keyPad_h = 400
keyPad_w = 700

currentNotes = []

class Key:
    pg.time.delay(10)

    def __init__(self, x, noteName, keyName):
        self.x = x
        self.y = 201
        self.noteName = noteName
        self.keyName = keyName

        self.note = note.Note(noteName)

    def displayNote(self):
        self.noteFont = pg.font.Font("fonts/JosefinSans-Regular.ttf", self.noteFontSize)
        self.keyFont = pg.font.Font("fonts/JosefinSans-Regular.ttf", self.keyFontSize)

        self.noteText = self.noteFont.render(self.noteName, True, self.fontColor)
        self.keyText = self.keyFont.render(self.keyName, True, self.fontColor)

        piano.blit(self.noteText, (self.font_x, self.font_y))
        piano.blit(self.keyText, (self.font_x + 10, self.font_y + 5 + self.noteFontSize))

    def initialise(self):
        self.playing = False
        pg.draw.rect(piano, self.color, (self.x, self.y, self.w, self.h))
        self.displayNote()

    def getClicked(self):
        self.playing = True
        pg.draw.rect(piano, self.clickedColor, (self.x, self.y, self.w, self.h))
        self.displayNote()

    def playSound(self):
        t = threading.Thread(target=self.soundThread)
        t.start()

    def soundThread(self):
        currentNotes.append(self.note)
        pianoChord = chord.Chord(currentNotes)
        pianoChord.show('midi')

class WhiteKey(Key):
    def __init__(self, x, noteName, keyName):
        Key.__init__(self, x, noteName, keyName)
        self.h = 400
        self.w = 98
        self.color = (255, 255, 255)
        self.clickedColor = (223, 215, 230)

        self.fontColor = (0, 0, 0)
        self.noteFontSize = 50
        self.keyFontSize = 40
        self.font_x = self.x + 20
        self.font_y = self.y + 280

        self.initialise()


class BlackKey(Key):
    def __init__(self, x, noteName, keyName):
        Key.__init__(self, x, noteName, keyName)
        self.h = 200
        self.w = 60
        self.color = (0, 0, 0)
        self.clickedColor = (60, 55, 70)

        self.fontColor = (255, 255, 255)
        self.noteFontSize = 22
        self.keyFontSize = 18
        self.font_x = self.x + 10
        self.font_y = self.y + 130

        self.initialise()

# The dictionary maps keyboard keys to piano keys
keys = {pg.K_a: WhiteKey(51, 'C4', 'A'),
     pg.K_s: WhiteKey(151, 'D4', 'S'),
     pg.K_d: WhiteKey(251, 'E4', 'D'),
     pg.K_f: WhiteKey(351, 'F4', 'F'),
     pg.K_g: WhiteKey(451, 'G4', 'G'),
     pg.K_h: WhiteKey(551, 'A4', 'H'),
     pg.K_j: WhiteKey(651, 'B4', 'J'),
     pg.K_w: BlackKey(120, 'C#4', 'W'),
     pg.K_e: BlackKey(220, 'D#4', 'E'),
     pg.K_t: BlackKey(420, 'F#4', 'T'),
     pg.K_y: BlackKey(520, 'G#4', 'Y'),
     pg.K_u: BlackKey(620, 'A#4', 'U')}

def handleKeyPress(key):
    key.getClicked()
    pg.display.update()

def handleKeyRelease(key):
    keys[event.key].initialise()
    pg.display.update()
    currentNotes.remove(key.note)

run = True
playing = False

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            try:
                handleKeyPress(keys[event.key])
                keys[event.key].playSound()
            except KeyError:
                pass

        if event.type == pg.KEYUP:
            try:
                handleKeyRelease(keys[event.key])
            except KeyError:
                pass

    # to remove the old position
    piano.fill((20, 0, 40))
    piano.blit(text, (180, 45))
    pg.draw.rect(piano, (0, 0, 0), (keyPad_x, keyPad_y, keyPad_w, keyPad_h))

    for key in keys:
        if not(keys[key].playing):
            keys[key].initialise()
        else:
            keys[key].getClicked()

    # to refresh display and show rectangle
    pg.display.update()

pg.quit()
