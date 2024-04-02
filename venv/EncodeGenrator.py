import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
cred = credentials.Certificate("C:\\Users\\DELL\\Desktop\\Face_rec_real_time\\venv\\serviceAccountKey.json.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendancerealtime-44c7e-default-rtdb.firebaseio.com/",
                                    'storageBucket': "faceattendancerealtime-44c7e.appspot.com"
                                    })


# importing the student images
folderpath='Photos'
Pathlist= os.listdir(folderpath)
imgList=[]
studentids=[]
for path in Pathlist:
    imgList.append(cv2.imread(os.path.join(folderpath,path)))
    studentids.append(os.path.splitext(path)[0])
    fileName= f'{folderpath}/{path}'
    bucket= storage.bucket()
    blob =bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    #print(path)
    #print(os.path.splitext(path)[0])

print(len(imgList))
print(studentids)

encodeList=[]
# window_name='Photo'
def findEncodings(imgList):
    
    for img in imgList:
        
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

       
    return encodeList
print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown, studentids]
#print("EncodeFile.p",'wb')
file=open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("fileSave")
#print(encodeListKnown)
print("Encoding Complete")