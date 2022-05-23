from tkinter import *
import time
import sys

sys.setrecursionlimit(10**8)

def createM(A,x,color):
    for i in range(0,10):
        for j in range(0,10):
            A.create_rectangle(40*i+x,40*j+40,40*i+x+40,40*j+80,fill=color)

def gameWindow():
    Game=Tk()
    Game.geometry('900x500')
    Game.title('Game')
    Game.resizable(width=NO,height=NO)
    Game.wm_attributes('-topmost',1)
    back_ground=Canvas(Game,width=900,height=500,bg='Black')
    back_ground.pack()
    createM(back_ground,30,'green1')
    createM(back_ground,460,'blue')

    Game.mainloop()
    
