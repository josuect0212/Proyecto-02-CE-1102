from turtle import down
from DriverSerial import DriverSerial
from threading import Thread
from tkinter import *
import threading 
import pygame
import serial
import random
import pickle
import time
import sys
import os

pygame.mixer.init()


def loadImage(filename):
    path = os.path.join('auxiliar',filename)
    imagen = PhotoImage(file=path)
    return imagen

def read(filename):
    '''this funcion open and read a file
    parameters: 
    filename: refers to the name of the file 

    return: a list of the lines of the file
    '''
    fileC = open(filename)
    content=fileC.readlines()
    fileC.close()
    return content

def write(filename,text):
    '''this funcion rewite all the information of a file
    paramenter:
    filename: refes to the name of the file 
    content: refest to what is goin to be writen
    '''
    fileC = open(filename,'w')
    fileC.write(text)
    fileC.close()

def sound(_x_):

        if _x_ =='game':
            pygame.mixer.music.stop()
            MusicPath = os.path.join("auxiliar",'Menu_Soundtrack.wav')
            pygame.mixer.music.load(MusicPath)
            pygame.mixer.music.play()  
        elif _x_ == 'menu':
            pygame.mixer.music.stop()
            MusicPath = os.path.join("auxiliar",'BG_Music.wav')
            pygame.mixer.music.load(MusicPath)
            pygame.mixer.music.play() 
        elif _x_ == 'win':
            pygame.mixer.music.stop()
            MusicPath = os.path.join("auxiliar",'Victory.wav')
            pygame.mixer.music.load(MusicPath)
            pygame.mixer.music.play() 
        elif _x_ == 'defeat':
            pygame.mixer.music.stop()
            MusicPath = os.path.join("auxiliar",'Defeat.wav')
            pygame.mixer.music.load(MusicPath)
            pygame.mixer.music.play() 
        else:
            pass
    

'''def playMusic(name):
    #pygame.mixer.music.stop()
    MusicPath = os.path.join("auxiliar",name)
    pygame.mixer.music.load(MusicPath) 
    pygame.mixer.music.play()'''

class GAME:

    def __init__(self,P_N,num_boat_P,num_boat_C,M_P,M_C,M_S,nfs_p,nfs_c):
        #self.__serial=DriverSerial()
        self.turn=True
        self.Player_NAME=P_N#refers to the name of the player
        self.num_boat_p=num_boat_P#refers to the cuantity if boats of the player
        self.num_boat_c=num_boat_C#refers to the cuantity if boats of the computer
        self.__x_c_p=30#keep track of the cords in x if the pointer
        self.__y_c_p=40#keep track of the cords in y of the pointer
        self.__player_M=M_P#is the matriz of the cords of the players boats
        self.__computer_M=M_C#is the matriz of the cords of the computers boats
        self.__back_ground=None#it refers to the canvas 
        self.__matriz_shoot=M_S#this is made for the matriz used to select de computer shoot cords
        self.__nfs_c=nfs_c#cantidad de disparos de la computadora
        self.__nfs_P=nfs_p#cantidad de disparos del jugador
        self.cordx=0#matris cords
        self.cordy=0#matris cords
        self.hit_shots=0
        self.fail_shots=0
        self.T0=None#inicial time
        self.Tf=None#final time
        self.led=0

    def close_game(self):
        self.stats=Toplevel()
        self.Game.wm_attributes('-topmost',1)
        self.stats.geometry('350x220')
        self.stats.title('STATS')
        self.stats.resizable(height=NO,width=NO)
        self.Tf=round(time.time()-self.T0,3)
        
        def placeonlist(Scorelist,finallist,points,i,place):
            if Scorelist==[] or i==10:
                print(finallist)
                write('scores.txt',finallist)
                return place 
            elif float(Scorelist[0].split(',')[0])<=float(points[0].split(',')[0]):
                finallist+=str(Scorelist[0])
                print(finallist+'1')
                return placeonlist(Scorelist[1:],finallist,points,i+1,0)
            elif float(Scorelist[0].split(',')[0])>float(points[0].split(',')[0]):
                finallist+=str(points[0])
                finallist+=str(Scorelist[0])
                print(finallist+'2')
                return placeonlist(Scorelist[1:],finallist,'1000000,---',i+1,i)

        p=[str(self.Tf)+','+self.Player_NAME+'\n']
        place=placeonlist(read('scores.txt'),'',p,1,0)

        if place>10:
            Text=self.Player_NAME+':\nYour time: '+str(self.Tf)+'s'+'\n\nYou shot '+str(self.__nfs_P)+' times.\n'+str(self.hit_shots)+' hits.\n'+str(self.fail_shots)+' fails.'
        else:
            Text=self.Player_NAME+':\nYour time: '+str(self.Tf)+'s'+'\nYou got '+str(place)+' on the hall of fame.'+'\n\nYou shot '+str(self.__nfs_P)+' times.\n\n'+str(self.hit_shots)+'hits\n'+str(self.fail_shots)+' fails'
        
        infof=Label(self.stats,text=Text,font=('helvetica',18))
        infof.pack()

        retur_B=Button(self.stats,text='return',command=self.retur)
        retur_B.place(x=300,y=180)
        self.stats.mainloop()

    def retur(self):
        self.Game.destroy()
        m=MENU()
        m.window()
               
    def playMusic(self,name):
        pygame.mixer.music.stop()
        MusicPath = os.path.join("auxiliar",name)
        pygame.mixer.music.load(MusicPath)
        pygame.mixer.music.play()
        time.sleep(2)
        sound('game')


    def matriz_shoot(self):
        '''
        this funcion make a matris for the shoots
        parameters:self
        return:-
        '''
        M=[]
        l=[]
        for i in range(10):
            for j in range(10):
                l+=[j]
            random.shuffle(l)
            M+=[l]
            l=[]
        return M
        
        

    def Computer_shoot(self,i):

        if self.__matriz_shoot[i]!=[]:
            self.__nfs_c+=1
            M=self.__matriz_shoot
            j=M[i][0]
            #cords=(i,j)
            
            t='shoot'+str(i)+str(j)
            
            M[i]=M[i][1:]
            self.__matriz_shoot=M
            
            if self.__player_M[j][i]==1:
                self.__player_M[j][i]=3
                
                self.num_boat_p-=1

                self.__back_ground.create_oval(20,20,60,60,fill='red1',tags=t)
                self.__back_ground.moveto(t,x=i*40+460,y=j*40+40)
                self.Game.update()
                
               
                if self.num_boat_p>0:

                    time.sleep(0.8)
                    n=random.randint(0,9)
                    self.Computer_shoot(n)

                else:

                    self.info=Label(self.Game,text='YOU DIED',bg='black',fg='red',font=('helvetica',45))
                    self.info.place(x=310,y=200)
                    sound('defeat')
                    self.close_game()
                    

            else:
                self.__player_M[j][i]=2

                self.__back_ground.create_oval(20,20,60,60,fill='White',tags=t)
                self.__back_ground.moveto(t,x=i*40+460,y=j*40+40)
                self.Game.update() 
                self.turn=True
        else:
            n=random.randint(0,9)
            self.Computer_shoot(n)

            
    def genera_Barcos(self):
        '''
        this funcion generate the graphically
        parameters:self
        return:-
        '''
    
        m=self.__player_M
        for i in range(0,9):
            for j in range(0,9):
                if m[i][j]==1:
                    b='barco'+str(i)+str(j)
                    
                    self.__back_ground.create_oval(20,20,60,60,fill='green',tags=b)
                    self.__back_ground.moveto(b,x=j*40+460,y=i*40+40)

                elif m[i][j]==2:
                    b='barco'+str(i)+str(j)

                    self.__back_ground.create_oval(20,20,60,60,fill='white',tags=b)
                    self.__back_ground.moveto(b,x=j*40+460,y=i*40+40)

                elif m[i][j]==3:
                    b='barco'+str(i)+str(j)

                    self.__back_ground.create_oval(20,20,60,60,fill='red',tags=b)
                    self.__back_ground.moveto(b,x=j*40+460,y=i*40+40)

        n=self.__computer_M
        for i in range(10):
            for j in range(10):
                if n[i][j]==2:
                    b='barco'+str(i)+str(j)

                    self.__back_ground.create_oval(20,20,60,60,fill='white',tags=b)
                    self.__back_ground.moveto(b,x=j*40+30,y=i*40+40)
    
                elif n[i][j]==3:
                    b='barco'+str(i)+str(j)

                    self.__back_ground.create_oval(20,20,60,60,fill='red',tags=b)
                    self.__back_ground.moveto(b,x=j*40+30,y=i*40+40) 

                elif n[i][j]==1:
                    b='barco'+str(i)+str(j)

                    self.__back_ground.create_oval(21,21,55,55,fill='red',tags=b)
                    self.__back_ground.moveto(b,x=j*40+35,y=i*40+45) 
                    

            
    def save(self):
        tp=time.time()
        propertys=[self.Player_NAME,self.num_boat_p,self.num_boat_c,self.__player_M,self.__computer_M,self.__matriz_shoot,self.__nfs_P,self.__nfs_c,self.T0,tp]
        x=open('partidaguardada','wb')
        pickle.dump(propertys,x)
        x.close()
        self.Game.destroy()
        m=MENU()
        m.window()

    def main(self):
        '''
        this funcion initialize the game window
        parameters:self
        return:-
        '''
        def createM(A,x,color):
            for i in range(0,10):
                for j in range(0,10):
                    tag=str(i)+str(j)+str(color)
                    A.create_rectangle(40*i+x,
                                        40*j+40,
                                        40*i+x+40,
                                        40*j+80,
                                        fill=color,
                                        tags=tag)



        
        
        self.Game=Tk()
        self.Game.geometry('900x500')
        self.Game.title('Game')
        self.Game.resizable(width=NO,height=NO)
        self.Game.wm_attributes('-topmost',1)
        self.__back_ground=Canvas(self.Game,width=900,height=500,bg='Black')
        self.__back_ground.pack()
        

        createM(self.__back_ground,30,'green1')
        createM(self.__back_ground,460,'blue')

        self.genera_Barcos()
        self.T0=time.time()



        self.__back_ground.create_polygon(35,55,45,55,45,45,
                                        55,45,55,55,65,55,
                                        65,65,55,65,55,75,
                                        45,75,45,65,35,65,
                                        fill='red',tags='pointer')

        
        BeginA=Button(self.Game,text='conect arduino',bg='green1',fg='black')
        BeginA.place(x=720,y=10)
        loadG=Button(self.Game,text='save game',bg='black',fg='green1',command=self.save)
        loadG.place(x=820,y=10)

        def move_managment(direction):
            if self.turn==True:
                if direction == 'U' and self.__y_c_p>70:
                    self.__back_ground.move('pointer',0,-40)
                    self.Game.update()
                    self.__y_c_p-=40
                    self.cordy-=1
                    print('UP')
                elif direction == 'R' and self.__x_c_p<390:
                    self.__back_ground.move('pointer',40,0)
                    self.Game.update()
                    self.__x_c_p+=40
                    self.cordx+=1
                    print('RIGHT')
                elif direction == 'D' and self.__y_c_p<390:
                    self.__back_ground.move('pointer',0,40)
                    self.Game.update()
                    self.__y_c_p+=40
                    self.cordy+=1
                    print('DOWN')
                elif direction == 'L' and self.__x_c_p>69:
                    self.__back_ground.move('pointer',-40,0)
                    self.Game.update()
                    self.__x_c_p-=40
                    self.cordx-=1
                    print('LEFT')
                elif direction == 'S':
                    self.turn=False
                    if self.num_boat_c>0 and self.num_boat_p>0:
                        self.__nfs_P+=1
                        i=self.cordy
                        j=self.cordx
                        h='p'+str(i)+str(j)
                        
                        try:
                            self.info.destroy()
                        except:
                            pass

                        if self.__computer_M[i][j]==1:
                            self.hit_shots+=1 
                            self.playMusic('Shot.wav')
    
                            self.info=Label(self.Game,text='nice shot, you have another try',bg='black',fg='green1')
                            self.info.place(x=10,y=15)

                            self.__back_ground.create_oval(20,20,60,60,fill='red',tags=h)
                            self.__back_ground.moveto(h,x=j*40+30,y=i*40+40)
                            self.Game.update
                            self.__computer_M[i][j]=3 
                            self.num_boat_c-=1
                            if self.num_boat_c>0:
                                self.turn=True
                            else:
                                self.info=Label(self.Game,text='YOU WIN',bg='black',fg='green1',font=('helvetica',45))
                                self.info.place(x=310,y=200) 
                                sound('win')
                                self.close_game() 
                                
                        elif self.__computer_M[i][j]==2 or self.__computer_M[i][j]==3:
                            
                            self.info=Label(self.Game,text='coord already shooted',bg='black',fg='white')
                            self.info.place(x=10,y=15)
                            self.turn=True

                        else:
                            self.fail_shots+=1
                            self.playMusic('Miss.wav')

                            self.info=Label(self.Game,text='You miss the shot',bg='black',fg='red')
                            self.info.place(x=10,y=15)
                            self.__back_ground.create_oval(20,20,60,60,fill='white',tags=h)
                            self.__back_ground.moveto(h,x=j*40+30,y=i*40+40)
                            self.Game.update()
                            self.__computer_M[i][j]=2
                            print(self.__computer_M)

                            n=random.randint(0,9)
                            print(n)
                            self.Computer_shoot(n)
                    else:
                        pass
                    

                #print((self.__nfs_P,self.__nfs_c))
                else:
                    print('limite') 
            else:
                pass
        
        self.Game.bind('<Up>',lambda direction:move_managment('U'))
        self.Game.bind('<Right>',lambda direction:move_managment('R'))
        self.Game.bind('<Down>',lambda direction:move_managment('D'))
        self.Game.bind('<Left>',lambda direction:move_managment('L'))
        self.Game.bind('<space>',lambda direction:move_managment('S'))

        self.Game.mainloop()
    
    '''def __compareSerial(self, command):
        if(command!=None):
            if(command =="arriba\n"):
                self.__back_ground.move('pointer',0,-40)
                self.__y_c_p-=40
                self.cordy-=1
                print('UP')
            elif(command=="abajo\n"):
                self.__back_ground.move('pointer',0,40)
                self.__y_c_p+=40
                self.cordy+=1
                print('DOWN')
            elif(command=="derecha\n"):
                self.__back_ground.move('pointer',40,0)
                self.__x_c_p+=40
                self.cordx+=1
                print('RIGHT')
            elif(command=="Izquierda\n"):
                self.__back_ground.move('pointer',-40,0)
                self.__x_c_p-=40
                self.cordx-=1
                print('LEFT')
            elif(command=="precion\n"):
                if self.num_boat_c>0 and self.num_boat_p>0:
                    self.__nfs_P+=1
                    i=self.cordy
                    j=self.cordx
                    h='p'+str(i)+str(j)
                    
                    try:
                        self.info.destroy()
                    except:
                        pass

                    if self.__computer_M[i][j]==1:
                        self.hit_shots+=1 
                        self.playMusic('Shot.wav')
 
                        self.info=Label(self.Game,text='nice shot, you have another try',bg='black',fg='green1')
                        self.info.place(x=10,y=15)

                        self.__back_ground.create_oval(20,20,60,60,fill='red',tags=h)
                        self.__back_ground.moveto(h,x=j*40+30,y=i*40+40)
                        self.__computer_M[i][j]=2 
                        self.num_boat_c-=1
                        if self.num_boat_c>0:
                            pass  
                        else:
                            self.info=Label(self.Game,text='YOU WIN',bg='black',fg='green1',font=('helvetica',45))
                            self.info.place(x=310,y=200) 
                            sound('win')
                            self.close_game() 
                            
                    elif self.__computer_M[i][j]==2:
                        
                        self.info=Label(self.Game,text='coord already shooted',bg='black',fg='white')
                        self.info.place(x=10,y=15)

                    else:
                        self.fail_shots+=1
                        self.playMusic('Miss.wav')

                        self.info=Label(self.Game,text='You miss the shot',bg='black',fg='red')
                        self.info.place(x=10,y=15)
                        self.__back_ground.create_oval(20,20,60,60,fill='white',tags=h)
                        self.__back_ground.moveto(h,x=j*40+30,y=i*40+40)
                        self.__computer_M[i][j]=2
                        print(self.__computer_M)

                        n=random.randint(0,9)
                        print(n)
                        self.Computer_shoot(n)
                else:
                   pass
                
            else:
                print(command)
'''

class Coloca_Barcos:

    def __init__(self,P_N,c1,c2,c4):
        self.P_N=P_N#refers to the player name
        self.Game=None#refers to the window (tk)
        self.m=None#refers to a matriz with the pocicion of the boats (pc)
        self.i=0#cosrd of the pointer(0,9)
        self.j=0#cordos of the pointer(0,9)
        self.o=0#ship orientation
        self.c_r=c1+c2+c4#refers to the total cuantiti of the boats
        self.c1=c1#numer of sigle boats
        self.c2=c2#numer of double boats
        self.c4=c4#numer of quadruple boats
        self.l=1#leng of the ships
        self.__x_c_p=30#cords in x of the pointer 
        self.__y_c_p=40#cords in y of the pointer
        self.__back_ground=None#main canvas 
        

        

    '''
    def n_b_c(self):
        if self.c_r>0:
            if self.c1>0:
                self.l=1
            elif self.c2>0 and self.c1==0:
                self.l=2
            else:
                self.l=4
        else:
            pass
        '''

    def matriz_shoot(self):
        '''
        this funcion make a matris for the shoots
        parameters:self
        return:-
        '''
        M=[]
        l=[]
        for i in range(10):
            for j in range(10):
                l+=[j]
            random.shuffle(l)
            M+=[l]
            l=[]
        return M

    def creaMatriz(self):
        '''
        this funcion initialize the matriz of the pc cords in 0's
        parameters:self
        return:mf
        '''
        a=[]
        mf=[]
        for i in range(0,10):
            for j in range(0,10):
                a+=[0]
                
            mf+=[a]
            a=[]
        return mf

    def genera_matriz_PC(self,C):
        '''
        this funcion sets the cords of the pc boats
        parameters:self
        C: cuantity of boats to add
        returns:
        m:the matris with the 'boats'
        '''
        l=[]
        m=self.creaMatriz()
        for i in range(0,100):
            l+=[i]
            random.shuffle(l)
        while C>0:
            u=l[0]
            i=u%10
            j=u//10
            m[j][i]=1
            l=l[1:]
            C-=1
        return m

    def clb(self):
        '''
        this funcion ask asck if thers already a boat or no
        parameters:self
        return:boolean
        '''
        if self.o==0:
            for x in range(0,self.l):
                print(self.i,self.j,self.l,len(self.m))

                if self.m[int(self.i+x)][int(self.j)]!=0:
                    return False
                return True 
        else:
            for x in range(0,self.l):
                if self.m[int(self.i)][int(self.j)+x]!=0:
                    return False
                return True 

 
    def coloca(self):
        '''
        this funcion place the boats graphically and logically
        parameters:self
        return:-
        '''
        global x
        try:
            self.ocupado.destroy()
        except:
            pass

        if self.c_r>0:

            if self.clb()==True:
            
                if self.o==0:
                
                    print(self.i,self.j)
                    print(self.m)
                    for x in range(self.l):
                        self.m[(self.i)][(self.j)+x]=1
                    
                    
                    t='b'+str(self.i)+str(self.j)
                    print(t,self.j,self.i)
                    print(self.m)
                    
                    X_=(self.j)*40+460
                    Y_=(self.i)*40+40

                    
                    self.__back_ground.create_oval(X_,Y_,X_+40,Y_+40,fill='green',tags=t)
                    self.__back_ground.moveto(t,x=X_,y=Y_)
                    self.c_r-=1
                    
                else:

                    print(self.i,self.j)
                    print(self.m)
                    for y in range(self.l):
                        self.m[(self.i)+y][(self.j)]=1
                    
                    
                    t='b'+str(self.i)+str(self.j)
                    print(t,self.j,self.i)
                    
                    X_=(self.j)*40+460
                    Y_=(self.i)*40+40

                    
                    self.__back_ground.create_oval(X_,Y_,X_+40,Y_+40,fill='green1',tags=t)
                    self.__back_ground.moveto(t,x=X_,y=Y_)
                    self.c_r-=1
                    
            else:
                self.ocupado=Label(self.Game,text='thers already a boat in ther',bg='black',fg='red',font=('helvetica',18))
                self.ocupado.place(x=8,y=4)
                

        else:
            
            sound('game')
            c=self.c1#+self.c2*2+self.c4*4
            self.Game.destroy()

            #######################
            x=GAME(self.P_N,c,c,self.m,self.genera_matriz_PC(c),self.matriz_shoot(),0,0)
            x.main()
            
            

    def main(self):
        '''
        this funcion inicializ the window and keep track of the keys
        parameters:self
        return:-
        '''

        self.m=self.creaMatriz()

        def createM(A,x,color):
            for i in range(0,10):
                for j in range(0,10):
                    tag=str(i)+str(j)+str(color)
                    A.create_rectangle(40*i+x,
                                        40*j+40,
                                        40*i+x+40,
                                        40*j+80,
                                        fill=color,
                                        tags=tag)

        self.Game=Tk()
        self.Game.geometry('900x500')
        self.Game.title('Game')
        self.Game.resizable(width=NO,height=NO)
        self.Game.wm_attributes('-topmost',1)
        self.__back_ground=Canvas(self.Game,width=900,height=500,bg='Black')
        self.__back_ground.pack()
        

        createM(self.__back_ground,30,'green1')
        createM(self.__back_ground,460,'blue')

        

        self.__back_ground.create_polygon(35,55,
                                        45,55,
                                        45,45,
                                        55,45,
                                        55,55,
                                        65,55,
                                        65,65,
                                        55,65,
                                        55,75,
                                        45,75,
                                        45,65,
                                        35,65,
                                        fill='red',
                                        tags='pointer')
        self.__back_ground.move('pointer',430,0)


        def move_managment(direction):

            if direction == 'U' and self.__y_c_p>70:

                self.__back_ground.move('pointer',0,-40)
                self.i-=1
                self.__y_c_p-=40
                print('UP')

            elif direction == 'R' and self.__x_c_p<390:

                self.__back_ground.move('pointer',40,0)
                self.j+=1
                self.__x_c_p+=40
                print('RIGHT')

            elif direction == 'D' and self.__y_c_p<390:

                self.__back_ground.move('pointer',0,40)
                self.i+=1
                self.__y_c_p+=40
                print('DOWN')

            elif direction == 'L' and self.__x_c_p>69:

                self.__back_ground.move('pointer',-40,0)
                self.j-=1
                self.__x_c_p-=40
                print('LEFT')

            else:

                print('limite') 

        
        self.Game.bind('<Up>',lambda direction:move_managment('U'))
        self.Game.bind('<Right>',lambda direction:move_managment('R'))
        self.Game.bind('<Down>',lambda direction:move_managment('D'))
        self.Game.bind('<Left>',lambda direction:move_managment('L'))
        self.Game.bind('<space>',lambda l:self.coloca())

        self.Game.mainloop()

#c=Coloca_Barcos(1,2,3)
#c.main()

class MENU:

    def __init__(self):
        
        self.__Menu=None#refers to the window (Tk)
        self.__error=None#refers to a label to show an error with the data

    def cargarImagen(self,nombre):
        ruta = os.path.join('auxiliar',nombre)
        imagen = PhotoImage(file=ruta)
        return imagen

    def window(self):
        '''
        this funcion make the menu window 
        parameters:self
        return:-
        '''
        sound('menu')
        self.__Menu = Tk()
        self.__Menu.geometry('711x400')
        self.__Menu.title('MAIN_MENU')
        self.__Menu.resizable(width=NO,height=NO)
        self.__Menu.wm_attributes('-topmost',1)

        Background = self.cargarImagen('fondo_menu.png')
        labelBg = Label(self.__Menu,image=Background)
        labelBg.pack()

        cancel = Button(self.__Menu,text='Exit',bg='green1',command=self.__Menu.destroy)
        cancel.place(x=80,y=360)
        
        NameL=Label(self.__Menu, text='Enter__your__Initials:',
                    bg='green2',fg='Black')
        NameL.place(x=15,y=225)

        NAMeE=Entry(bg='black',fg='green2')
        NAMeE.place(x=10,y=250)

        COBl=Label(self.__Menu, text='select_the_cuantity_of_boats:',
                    bg='green1',fg='black')
        COBl.place(x=10,y=295)

        CDB=Entry(bg='black',fg='green2')
        CDB.place(x=10,y=320)

        playB = Button(self.__Menu, text= 'Play',bg='green1',fg='black',command=lambda: self.begin((NAMeE.get()),(CDB.get())))
        playB.place(x=20,y=360)

        '''beginarduino= Button(self.__Menu,text='arduino', bg='green1',fg='balck',command=th_receiveData)
        beginarduino.place(x=60,y=360)'''

        up_menu=Menu(self.__Menu)
        up_menu.add_command(label='help',command = self.Help)

        up_menu.add_command(label='HALL_OF_FAME',command=self.HoF)

        up_menu.add_command(label='LOAD_GAME',command=self.load_G)

        self.__Menu.config(menu=up_menu)
        self.__Menu.mainloop()

    def begin(self,name,cdb):
        '''
        This funcion ask if the data is correct and begin the window for 
        selecting the boats cords
        parameters:self
        -name:the name of the player(str)
        -cdb:refers to the amount of boats the user indicates
        return:-
        '''
        boats=cdb.split(',')
            
        if len(boats)==3:
            try:
                self.__error.destroy()

            except:
                pass
            
            try: 
                s=int(boats[0])
                d=int(boats[1])
                c=int(boats[2])
                
            except:
                self.__error=Label(self.__Menu,text='thers an error with the data, try again :)',bg='black',fg='green1')
                self.__error.place(x=30,y=50)
                return 0

            if 80>((s*1)+(d*2)+(c*4)):
                self.__Menu.destroy() 
                x=Coloca_Barcos(name,s,d,c)
                x.main()
            else:
                self.__error=Label(self.__Menu,text='those are to much boats, try again :)',bg='black',fg='green1')
                self.__error.place(x=30,y=50)
        else:
            self.__error=Label(self.__Menu,text='thers an error with the data, try again :)',bg='black',fg='green1')
            self.__error.place(x=30,y=50)
    

    def Help(self):
        '''
        this funcion if for the help window
        parameters:self
        return:-
        '''
        help = Toplevel(bg='black')
        help.geometry('500x300')
        help.title('help')
        help.resizable(width=NO,height=NO)

        info = Label(help,text='ferst put your inicials and the amound of boats,\n ',bg='#000000',fg='green1')
        info.pack()

        cancel = Button(help,text='Exit',command=help.destroy)
        cancel.place(x=450,y=250)
        help.mainloop()
    
    def HoF(self):
        '''
        this funcion if for the hall of fame 
        parameters:self
        return:-
        '''
        def prepartoshow(Scorelist,finall):
            if Scorelist==[]:
                return finall
            else:
                return prepartoshow(Scorelist[1:],finall+str(Scorelist[0]))

        hof =Toplevel()
        hof.geometry('400x500')
        hof.title('Hall_of_Fame')
        
        scoreslist= prepartoshow(read('scores.txt'),'')
        listoS = Label(hof,text=scoreslist,bg='green1',fg='black',justify='left')
        listoS.place(x=10,y=50)

        cancel = Button(hof,text='Exit',command=hof.destroy)
        cancel.place(x=350,y=460)
        hof.mainloop()

    def load_G(self):
        x=open('partidaguardada','rb')
        propertys=pickle.load(x)
        self.__Menu.destroy()
        y=GAME(propertys[0],propertys[1],propertys[2],propertys[3],propertys[4],propertys[5],propertys[6],propertys[7])
        y.main()
        


def comiezo():
    M=MENU()
    M.window()
    

comiezo()
