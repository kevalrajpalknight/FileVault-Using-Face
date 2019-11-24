import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Train Vault")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

window.geometry('1280x720')
window.configure(background='LightSkyBlue1')

window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


message = tk.Label(window, text="Face-Vault-System" ,bg="LightSkyBlue1"  ,fg="black"  ,width=50  ,height=3,font=('Helvetica', 30, 'italic bold underline')) 

message.place(x=200, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="Black"  ,bg="LightSkyBlue1" ,font=('Helvetica', 15, 'bold') ) 
lbl.place(x=400, y=200)

txt = tk.Entry(window,width=20  ,bg="LightSkyBlue1" ,fg="Black",font=('Helvetica', 15, 'bold'))
txt.place(x=700, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="Black"  ,bg="LightSkyBlue1", height=2 ,font=('Helvetica', 15, 'bold')) 
lbl2.place(x=400, y=300)

txt2 = tk.Entry(window,width=20  ,bg="LightSkyBlue1"  ,fg="Black",font=('Helvetica', 15, 'bold')  )
txt2.place(x=700, y=315)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="Black"  ,bg="LightSkyBlue1"  ,height=2 ,font=('Helvetica', 15, 'bold underline')) 
lbl3.place(x=400, y=400)

message2 = tk.Label(window, text="" ,bg="LightSkyBlue1"  ,fg="Black"  ,width=30  ,height=2, activebackground = "LightSkyBlue3" ,font=('Helvetica', 15, 'bold')) 
message2.place(x=700, y=400)

def clear():
    txt.delete(0, 'end')    
    res = ""
    message2.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message2.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 

def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\\"+name +"-"+Id +'-'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('Capturing Images...',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>80:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('UserDetails\\Details.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message2.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message2.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message2.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split("-")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

clearButton = tk.Button(window, text="Clear", relief="flat", command=clear  ,fg="black"  ,bg="LightSkyBlue1"  ,width=20  ,height=2 ,activebackground = "LightSkyBlue3" ,font=('Helvetica', 15, ' bold '))
clearButton.place(x=950, y=200)
clearButton2 = tk.Button(window, text="Clear", relief="flat",command=clear2  ,fg="black"  ,bg="LightSkyBlue1"  ,width=20  ,height=2, activebackground = "LightSkyBlue3" ,font=('Helvetica', 15, ' bold '))
clearButton2.place(x=950, y=300)    
takeImg = tk.Button(window, text="Take Images", relief="flat",command=TakeImages  ,fg="black"  ,bg="LightSkyBlue1"  ,width=20  ,height=3, activebackground = "LightSkyBlue3" ,font=('Helvetica', 15, ' bold '))
takeImg.place(x=200, y=500)
trainImg = tk.Button(window, text="Train Images", relief="flat",command=TrainImages  ,fg="black"  ,bg="LightSkyBlue1"  ,width=20  ,height=3, activebackground = "LightSkyBlue3" ,font=('Helvetica', 15, ' bold '))
trainImg.place(x=650, y=500)
quitWindow = tk.Button(window, text="Quit", relief="flat",command=window.destroy  ,fg="black"  ,bg="LightSkyBlue1"  ,width=20  ,height=3, activebackground = "LightSkyBlue3" ,font=('Helvetica', 15, ' bold '))
quitWindow.place(x=1100, y=500)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 10, 'italic bold'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by Keval","", u"\u00A9", "superscript")
copyWrite.configure(state="disabled",fg="black"  )
copyWrite.pack(side="right")
copyWrite.place(x=800, y=750)
 
window.mainloop()