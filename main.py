#!/usr/bin/python
from random import randint
import sys
import os
import re
import curses

cursor_x=1
cursor_y=1

def draw_menu(stdscr):
    #most recent key pressed
    k='0'

    #globalize player pos
    global cursor_x
    global cursor_y

    #screen size and bounds
    height, width = stdscr.getmaxyx()
    height-=1 #im not sure why i cant use the last line but i cant. 
    world=[['.' for i in range(width)] for k in range(height)]

    #choose font
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.attron(curses.color_pair(1))

    #generate a maze
    boxify(world)
    genmaze(1,height-2,1,width-2,world,-1,-1)
    world[cursor_x][cursor_y]='@'
    world[height-2][width-2]='V'

    #make a method for creating monsters
    for i in range(10):
        cell=randcell(world)
        world[cell[0]][cell[1]]=str(i)


    while(k != ord('q')):
        #begin with fresh canvas
        stdscr.clear()

        #process input
        tx=cursor_x
        ty=cursor_y
        
        if k==ord('h'):
            cursor_y-=1
        elif k==ord('l'):
            cursor_y+=1
        elif k==ord('k'):
            cursor_x-=1
        elif k==ord('j'):
            cursor_x+=1

        if world[cursor_x][cursor_y]=='.':
            world[tx][ty]='.'
            world[cursor_x][cursor_y]='@'
        elif world[cursor_x][cursor_y]=='V':
            height, width = stdscr.getmaxyx()
            height-=1
            world=[['.' for i in range(width)] for k in range(height)]
            boxify(world)
            genmaze(1,height-2,1,width-2,world,-1,-1)
            world[height-2][width-2]='V'
            cursor_x=1
            cursor_y=1
            world[cursor_x][cursor_y]='@'
        elif re.match(r'\d',world[cursor_x][cursor_y]):
            world[cursor_x][cursor_y]='.'
            cursor_x=tx
            cursor_y=ty
        else:
            cursor_x=tx
            cursor_y=ty


        #draw the maze
        for r in range(len(world)):
            stdscr.addstr(r,0,''.join(world[r]))

        #draw screen
        stdscr.refresh()

        #get the next character
        k = stdscr.getch()
        #end of loop

def printmtx(mtx):
    for r in mtx:
        s=""
        for c in r:
            s+=c
        print(s)
def boxify(mtx):
    for r in range(len(mtx)):
        for c in range(len(mtx[0])):
            if r==0 or r==len(mtx)-1 or c==0 or c==len(mtx[0])-1: 
                mtx[r][c]='#'

def genmaze(top,bot,left,right,mtx,rhol,chol):
    mindim=3
    height=bot-top
    width=right-left
    if width>mindim and height>mindim:
        print(height,width)
    else:
        return
    pivr=rhol
    pivc=chol
    while pivr==rhol:
        pivr=randint(top+1,bot-1)
    while pivc==chol:
        pivc=randint(left+1,right-1)
    print(pivr,pivc)
    for r in range(top,bot+1):
        mtx[r][pivc]='#'
    for c in range(left,right+1):
        mtx[pivr][c]='#'
    #put in the holes
    #0,1,2,3 map up,down,left,right
    nohole=randint(0,3)
    print(nohole)
    hole0=-1
    hole1=-1
    hole2=-1
    hole3=-1
    if nohole!=0:
        hole0=randint(top,pivr-1)
        mtx[hole0][pivc]='.'
    if nohole!=1:
        hole1=randint(pivr+1,bot)
        mtx[hole1][pivc]='.'
    if nohole!=2:
        hole2=randint(left,pivc-1)
        mtx[pivr][hole2]='.'
    if nohole!=3:
        hole3=randint(pivc+1,right)
        mtx[pivr][hole3]='.'
    #tl,tr,bl,br
    genmaze(top,pivr-1,left,pivc-1,mtx,hole0,hole2)
    genmaze(top,pivr-1,pivc+1,right,mtx,hole0,hole3)
    genmaze(pivr+1,bot,left,pivc-1,mtx,hole1,hole2)
    genmaze(pivr+1,bot,pivc+1,right,mtx,hole1,hole3)
    

def domoveact(inp,mtx,pr,pc):
    tr=pr
    tc=pc
    mtx[pr][pc]='.'
    if inp=='h':
        pc-=1
    elif inp=='l':
        pc+=1
    elif inp=='k':
        pr-=1
    elif inp=='j':
        pr+=1
    else:
        print("not a move action")
    if mtx[pr][pc]!='.':
        print('there is something in the way')
        mtx[tr][tc]='@'
        pr=tr
        pc=tc
    else:
        mtx[pr][pc]='@'
def moveaction (c):
    if c=='h'or c=='j'or c=='k'or c=='l':
        return True
    else:
        return False
def randcell(mtx):
    tries=0
    out=(1,1)
    while tries<10 and mtx[out[0]][out[1]]!='.':
        out=(randint(0,len(mtx)-1),randint(0,len(mtx[0])-1))
    return out
#def makeML(mtx,lvl):
    #out=an array or some shit


#while True:
#    printworld()
#    action=input('input:')
#    if action=='q':
#        break
#    if moveaction(action):
#        domoveact(action)

def main():
    curses.wrapper(draw_menu)
if __name__ == "__main__":
    main()


