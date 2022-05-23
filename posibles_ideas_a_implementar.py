from tkinter import *
import time
import sys

sys.setrecursionlimit(10**8)

def createM(A,x,color):
    '''
    create a matrix of cubes
    parameters:
    A: is where the matrix is placed.
    x: is how much the matrix is displaced in the x axis.
    color: is the rgb color of the cubes.
    '''
    for i in range(0,10):
        for j in range(0,10):
            A.create_rectangle(40*i+x,40*j+40,40*i+x+40,40*j+80,fill=color)
            

def gameWindow():
    '''
    def the window for the game
    '''
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
    

def GameMainMenu():
    '''
    def de main window
    '''
    Main=Tk()
    Main.geometry('400x200')
    Main.title('MAIN_MENU')
    Main.resizable(width=NO,height=NO)
    Main.wm_attributes('-topmost',1)
    
    main_bg=Canvas(Main,width='410',height='210',bg='blue').place(x=0,y=0)
    
    gameB=Button(Main, text='game',bg='black',fg='green3',command=gameWindow).place(x=10,y=10)
    Main.mainloop()

GameMainMenu()
