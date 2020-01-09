from tkinter import Tk, Canvas
from time import sleep
import random

import pygame

pygame.init()



#global variables
WIDTH = 400

HEIGHT = 400

APPLE = []
TAGS = ['APPLE1', 'APPLE2']

s = []

IsFirstIteration = True

GameIsRunning = True

SEG_SIZE = 20

IN_GAME = False

FPS = 60

GM = 0

DIRECTION_IS_CHANGED_ALREADY = False

segsOfSegs = []

TextId = None



#CLOCK = pygame.time.Clock()

#sc = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Python")
#sc.fill(WHITE)
#pygame.display.flip()



def main():
    global s
    global TextId
    global APPLE
    global TAGS
    global GM
    global IN_GAME
    global IsFirstIteration
    global DIRECTION_IS_CHANGED_ALREADY
    global segsOfSegs
    whoLose = -1

    if IsFirstIteration:
        canv.delete(TextId)


        if GM == 1:
            segsOfSegs.append([Segment(WIDTH/2 , HEIGHT/2),
                        Segment(WIDTH/2, HEIGHT/2 + SEG_SIZE),
                        Segment(WIDTH/2, HEIGHT/2 + 2*SEG_SIZE)])
        elif GM == 2:
            segsOfSegs.append([Segment(3*WIDTH/4 , HEIGHT/2),
                        Segment(3*WIDTH/4, HEIGHT/2 + SEG_SIZE),
                        Segment(3*WIDTH/4, HEIGHT/2 + 2*SEG_SIZE)])

            segsOfSegs.append([Segment(WIDTH/4 , HEIGHT/2),
                        Segment(WIDTH/4, HEIGHT/2 + SEG_SIZE),
                        Segment(WIDTH/4, HEIGHT/2 + 2*SEG_SIZE)])

        for i in range(0, GM):
            s.append(Snake(segsOfSegs[i], i))

        canv.bind("<KeyPress>", BUTTON_PRESSED)


        for i in range(0, GM):
            APPLE.append(Apple(segsOfSegs, i))



        #canv.delete(APPLE[1])

        IsFirstIteration = False
        IN_GAME = True


    if IN_GAME:
        for i in range(0, GM):

            if not i == 1:
                s[i].move()

        for i in range(0, GM):
            headCoords = canv.coords(s[i].segments[0].instance)

            x1, y1, x2, y2 = headCoords

			#falling over edge
            if x1 < 0 or x2 > WIDTH or y1 < 0 or y2 > HEIGHT:
                IN_GAME = False

                whoLose = i

            for j in range(0, GM):
                #eat apple
                #print( canv.coords(APPLE[j]))
                if (headCoords == canv.coords(APPLE[j].instance)):
                        s[i].add_segment()

                        canv.Children.Remove(APPLE[j])
                        print(APPLE[j])
                        APPLE[j] = None
                        APPLE[j] = Apple(segsOfSegs,j)

                #selfeating
                else:
                    for t in range(1, len(s[j].segments) - 1):
                        if headCoords == canv.coords(s[j].segments[t].instance):
                            IN_GAME = False

                            whoLose = i
        if len(s) == 2 and canv.coords(s[0].segments[0].instance) == canv.coords(s[1].segments[0].instance):
            whoLose = -1
            IN_GAME = False


        root.after(100, main)

    else:
        if len(s) == 1:
            #defeat text
            canv.create_text(WIDTH / 2,
                             HEIGHT / 2,
                             text = "LOSE",
                             font = "Arial 20",
                             fill = "#ff0000")
        elif whoLose == -1:
            canv.create_text(WIDTH / 2,
                             HEIGHT / 2,
                             text = "DRAW",
                             font = "Arial 20",
                             fill = "#ff0000")

        else:
            canv.create_text(WIDTH / 2,
                             HEIGHT / 2,
                             text = "Player " + (len(s) - whoLose) + " won",
                             font = "Arial 20",
                             fill = "#ff0000")

def BUTTON_PRESSED(event):
    if event.keysym in s[0].mapping:
        if event.keysym == "Down" or event.keysym == "Left" or event.keysym == "Up" or event.keysym == "Right":
            s[0].change_direction(event.keysym)
        elif len(s) > 1:
            s[1].change_direction(event.keysym)


class Segment(object):
    def __init__(self, x, y):
        self.instance = canv.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill = "black")
        #self.nextSegment = None
        #self.prevSegment = None
        #self.x = x
        #self.y = y

class Apple(object):
    def __init__(self, segsOfSegs, i):
        TAGS = ["APPLE1", "APPLE2"]
        COLORS = ["RED","ORANGE"]
        IsPlaceFree = False

        while not IsPlaceFree:
            posx = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
            posy = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))

            IsPlaceFree = True

            for i in range(0, len(segsOfSegs)):
                if not IsPlaceFree:
                    continue

                for seg in segsOfSegs[i]:
                    if not IsPlaceFree:
                        continue
                    x1,y1,x2,y2 = canv.coords(seg.instance)

                    #checking if coords are taken
                    if  (posx == x1 and
                         posy == y1 and
                         posx + SEG_SIZE == x2 and
                         posy + SEG_SIZE == y2):
                         IsPlaceFree = False
                self.instance = canv.create_rectangle(posx,
                                  posy,
                                  posx + SEG_SIZE,
                                  posy + SEG_SIZE,
                                  fill = COLORS[i], tag = TAGS[i])
            #print(i)


class Snake(object):
    def __init__(self, segments, i = 0):
        self.segments = segments

        self.player = i

        #adding reference for prev and next segment
        for i in range(1, len(segments) - 1):
            self.segments[i].prevSegment = segments[i - 1]
            if i != len(segments) - 1:
                self.segments[i].nextSegment = segments[i + 1]


        #mapping of movement directions
        self.mapping = {"Down": (0, 1),
                        "Up": (0, -1),
                        "Left": (-1, 0),
                        "Right": (1, 0),
                        "s": (0, 1),
                        "w": (0, -1),
                        "a": (-1, 0),
                        "d": (1, 0)}



        self.direction = (0, -1)

    #movement function
    def move(self):
        for i in range(len(self.segments) - 1):
            segment = self.segments[-1 - i].instance
            x1, y1, x2, y2 = canv.coords(self.segments[-2 - i].instance)
            canv.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = canv.coords(self.segments[0].instance)

        canv.coords(self.segments[0].instance,
                    x1 + self.direction[0]*SEG_SIZE,
                    y1 + self.direction[1]*SEG_SIZE,
                    x2 + self.direction[0]*SEG_SIZE,
                    y2 + self.direction[1]*SEG_SIZE)

    #change movement vector
    def change_direction(self, vector):

        x1, y1, x2, y2 = canv.coords(self.segments[0].instance)
        q, w, e, r = canv.coords(self.segments[1].instance)

        if vector in self.mapping:
            if not (x1 + self.mapping[vector][0]*SEG_SIZE == q and
                    y1 + self.mapping[vector][1]*SEG_SIZE == w and
                    x2 + self.mapping[vector][0]*SEG_SIZE == e and
                    y2 + self.mapping[vector][1]*SEG_SIZE == r):
                if ( self.direction[0] != -self.mapping[vector][0] ) or \
                        ( self.direction[1] != -self.mapping[vector][1] ):
                    self.direction = self.mapping[vector]


    #add segment after eating apple or smth else
    def add_segment(self):
        last_seg = canv.coords(self.segments[-1].instance)

        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE

        self.segments.insert(-1, Segment(x, y))



#eda
'''
def spawn_apple(segsOfSegs, i = 0):
    IsPlaceFree = False

    while not IsPlaceFree:
        posx = SEG_SIZE * (random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE))
        posy = SEG_SIZE * (random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE))

        IsPlaceFree = True

        for i in range(0, len(segsOfSegs)):
            if not IsPlaceFree:
                continue

            for seg in segsOfSegs[i]:
                if not IsPlaceFree:
                    continue
                x1,y1,x2,y2 = canv.coords(seg.instance)

                #checking if coords are taken
                if  (posx == x1 and
                     posy == y1 and
                     posx + SEG_SIZE == x2 and
                     posy + SEG_SIZE == y2):
                     IsPlaceFree = False

        if len(APPLE) < i + 1:
            APPLE.append(canv.create_rectangle(posx,
                                  posy,
                                  posx + SEG_SIZE,
                                  posy + SEG_SIZE,
                                  fill = "red"))
            return
		APPLE[i] = canv.create_rectangle(posx,
                              posy,
                              posx + SEG_SIZE,
                              posy + SEG_SIZE,
                              fill = "red")
'''

def gameModeShoose(event):
    if IN_GAME:
        return

    global GM
    if (event.keysym == "1"):
        GM = 1
    elif (event.keysym == "2"):
        GM = 2
    main()


root = Tk()

root.title("Python Snake")

canv = Canvas(root, width = WIDTH, height = HEIGHT, bg = "#ffffff")

canv.grid()

canv.focus_set()

TextId = canv.create_text(WIDTH / 2,
                HEIGHT / 2,
                text = "Shoose GM (count of players)\n 1 - solo\n 2 - PvP",
                font = "Arial 20",
                fill = "black")

canv.bind("1", gameModeShoose)
canv.bind("2", gameModeShoose)

root.mainloop()
