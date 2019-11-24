# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 23:40:39 2019

@author: knight
"""

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
import sys
from cryptography.fernet import Fernet
import os
import cv2
import pandas as pd
import time
def TrackImages():
	try:
		recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
		recognizer.read("TrainingImageLabel\\Trainner.yml")
		harcascadePath = "haarcascade_frontalface_default.xml"
		faceCascade = cv2.CascadeClassifier(harcascadePath) 
		cam = cv2.VideoCapture(0)
		font = cv2.FONT_HERSHEY_SIMPLEX   
		while True:
			ret, im =cam.read()
			gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
			faces=faceCascade.detectMultiScale(gray, 1.2,5)
			for(x,y,w,h) in faces:
				cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
				Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
				if(int(conf) > 75):
					tt=int(Id)
					cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)  
					time.sleep(2)
					cam.release()
					cv2.destroyAllWindows(); return tt
				else:
					Id='Unknown'
					tt=str(Id)  
				if(conf > 65):
					noOfFile=len(os.listdir("IntruderImages"))+1
					cv2.imwrite("IntruderImages\\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
				cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)  

			cv2.imshow('Comparing Images...',im) 
			if (cv2.waitKey(1)==ord('q')):
				break

		cam.release()
		cv2.destroyAllWindows(); return tt
	except Exception as e:
		print(e)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Electroic File System Open File"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300


        self.InitWindow()


    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()

        self.btn1 = QPushButton("Lock/Unlock File")
        self.btn1.clicked.connect(self.getFile)

        vbox.addWidget(self.btn1)

        self.label = QLabel("Smart Locker")
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.show()
    
    def locker(self, file_path):
        try:
            
            ## Encrpyting the Selected File
            if ".locked" in os.path.basename(file_path):
                df = pd.read_csv("UserDetails\\Details.csv")
                list_of_IDs = list(df.Id)
                # print(list_of_IDs)
                pred_Id = TrackImages()
                # print(pred_Id)
                
                if  pred_Id in list_of_IDs:
                    with open('<<Your Key Location>>\\key.key','rb') as k:  # Replace with location Where you want to hide this key
                       key =  k.read()
                    with open(file_path, 'rb') as f:
                        data = f.read()
                    
                    fernet = Fernet(key)
                    encrypted = fernet.decrypt(data)
                    temp = file_path
                    with open(str(file_path).replace(".locked",""), 'wb') as f:
                        f.write(encrypted)
                    os.remove(temp)
                else:
                    pass
    			
            else:
                key = Fernet.generate_key().decode()
                with open('<<Your Key Location>>\\key.key','w') as k:   # Replace with location Where you want to hide this key
                    k.write(key)
                with open(file_path, 'rb') as f:
                    data = f.read()
                    
                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)
                encrpytedfile = file_path+".locked"
                
                with open(encrpytedfile, 'wb') as f:
                    f.write(encrypted)
                os.remove(file_path)
        except FileNotFoundError:
            pass
        
        
    def getFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Lock/Unlock file','', "All files (*.*)")
        file_path = fname[0]
        self.locker(file_path)
    
        
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())