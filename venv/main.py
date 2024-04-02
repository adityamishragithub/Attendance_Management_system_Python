import os
import cv2
import pickle
import face_recognition
import numpy as np

import cvzone #in cvZone fancy rectangle are available 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
cred = credentials.Certificate("C:\\Users\\DELL\\Desktop\\Face_rec_real_time\\venv\\serviceAccountKey.json.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendancerealtime-44c7e-default-rtdb.firebaseio.com/",
                                    'storageBucket': "faceattendancerealtime-44c7e.appspot.com"
                                    })
bucket=storage.bucket()




cap=cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)



imgBackground = cv2.imread("Resourses/background.png")
#Importing a mode images into a list
foldermodepath='Resourses/modes'
modePathlist= os.listdir(foldermodepath)
imgModelist=[]

for path in modePathlist:
    imgModelist.append(cv2.imread(os.path.join(foldermodepath,path)))
#print(len(imgModelist))

#Load encodeding file...
print("Loading Encode File...")
file=open("EncodeFile.p","rb")
encodeListKnownWithIds=pickle.load(file)
file.close()
#pickle.dump(encodeListKnownWithIds,file)
encodeListKnown, studentids=encodeListKnownWithIds



print(studentids)
print("Encode File Loaded")
modeType=0
counter=0
id=-1
imgStudent=[]
while True:
    success ,img = cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurrFrame=face_recognition.face_locations(imgS)
    encodeCurrFrame=face_recognition.face_encodings(imgS,faceCurrFrame)
    imgBackground[162:162+480,55:55+640]=img
    imgBackground[44:44+633,808:808+414]=imgModelist[modeType]

    for encodeFace,faceLoc in zip(encodeCurrFrame,faceCurrFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
        print('matches',matches)
        print('distances',faceDis)


        matchIndex=np.argmin(faceDis)
        print("Match Index",matchIndex)

        if matches[matchIndex]:
            print("Known Face Detected")
            print(studentids[matchIndex])
            #now we use open rec which is provided by open cv
            #bounding box location is what we get from face location is 
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4    # we have to multiply by 4 because we reduse the size of image by 4 in above 
            

            # create bounding box
            # our img is not starting from zero we have to add x and y value which is starting from img ange then our image start
            # basically we have to add offset values
            bbox=55+x1,162+y1,x2-x1,y2-y1

            imgBackground= cvzone.cornerRect(imgBackground,bbox,rt=0)
            # firstarg: the img which is going to be used , secarg: the bounding box ,rt=rectangle thickness
            id=studentids[matchIndex]
            print(id)
            if  counter == 0:
                counter=1
                modeType=1
    
    if counter!=0:
        if counter==1:
            # get the Data
            studentInfo=db.reference(f'Face_Rec_Real_Time/Photos/{id}').get()
            print(studentInfo)
            blob=bucket.get_blob(f'Photos/{id}.png')
            #print(blob)
            
            #array = np.frombuffer(blob.download_as_string(), np.uint8)
            #imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)


            # get the image from the storage
        cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        
        cv2.putText(imgBackground,str(studentInfo['Major']),(999,550),cv2.FONT_HERSHEY_COMPLEX,0.4,(255,255,255),1)
        cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
        cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        cv2.putText(imgBackground,str(studentInfo['Starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
        (w,h),_ =cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset=(414-w)//2
        
        cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
        # imgBackground[175:175+216,909:909+216]=imgStudent
        counter+=1

    
            

    #cv2.imshow("webcam",img)
    cv2.imshow("Face Attendance",imgBackground)
    cv2.waitKey(1 )