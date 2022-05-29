from tkinter import *
import time
import sys
import DriverSerial

class GAME:

    def __init__(self):#,num_boat,COM,baudrate):
        #self.num_boat=num_boat
        #self.__serial=DriverSerial(COM,baudrate)
        self.__x_c_p=30
        self.__y_c_p=40

    def main(self):
        def createM(A,x,color):
            for i in range(0,10):
                for j in range(0,10):
                    A.create_rectangle(40*i+x,40*j+40,40*i+x+40,40*j+80,fill=color)
        

        Game=Tk()
        Game.geometry('900x500')
        Game.title('Game')
        Game.resizable(width=NO,height=NO)
        Game.wm_attributes('-topmost',1)
        back_ground=Canvas(Game,width=900,height=500,bg='Black')
        back_ground.pack()
        
        createM(back_ground,30,'green1')
        createM(back_ground,460,'blue')

        def move_managment(direction):
            if direction == 'U' and self.__y_c_p>70:
                return U(0)
            elif direction == 'R' and self.__x_c_p<390:
                return R(0)
            elif direction == 'D' and self.__y_c_p<390:
                return D(0)
            elif direction == 'L' and self.__x_c_p>70:
                return L(0)
            else:
                print('limite') 

        def U(m):
            self.__y_c_p-=40
            print('UP')

        def R(m):
            self.__x_c_p+=40
            print('RIGHT')

        def D(m):
            self.__y_c_p+=40
            print('DOWN')

        def L(m):
            self.__x_c_p-=40
            print('LEFT')
        
        Game.bind('<Up>',lambda direction:move_managment('U'))
        Game.bind('<Right>',lambda direction:move_managment('R'))
        Game.bind('<Down>',lambda direction:move_managment('D'))
        Game.bind('<Left>',lambda direction:move_managment('L'))

        Game.mainloop()

x=GAME()
x.main()