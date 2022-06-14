from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
import os
#from playsound import playsound
from threading import Thread
import threading
import time
from DriverSerial import DriverSerial

class prueba:

    def __init__(self):
        self.__serial=DriverSerial()
        self.n=0

    def readSerial(self):
        while(True):
            command= self.__serial.read()
            self.__compareSerial(command)

    def sendSerial(self,n):
        command= self.__serial.send(n.encode())

        
    def th_receiveData(self):
        th_time=Thread(target=self.readSerial, args=())
        th_time.start()

    def th_sendData(self):
        th_time=Thread(target=self.sendSerial, args=())
        th_time.start()

    def closeSerial(self):
        self.__serial.close()

    def __compareSerial(self, command):
        if(command!=None):
            if(command =="arriba\n"):
                print("arriba\n")
                self.sendSerial('4\n')
            elif(command=="abajo\n"):
                print("abajo\n")
                self.sendSerial('3\n')
            elif(command=="derecha\n"):
                print("derecha\n")
                self.sendSerial('2\n')
            elif(command=="Izquierda\n"):
                print("Izquierda\n")
                self.sendSerial('1\n')
                
            elif(command=="precion\n"):
                self.th_sendData()
                
            else:
                print(command)
x=prueba()
x.th_receiveData()