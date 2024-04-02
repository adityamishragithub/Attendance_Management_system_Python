import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:\\Users\\DELL\\Desktop\\Face_rec_real_time\\venv\\serviceAccountKey.json.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendancerealtime-44c7e-default-rtdb.firebaseio.com/"})
ref=db.reference('students')
data={
    "204":
    {
        "name":"Priyanshu Yadav",
        "Major":"Computer Science",
        "Starting_year":2020,
        "total_attendance":15,
        "standing":"A",
        "year":3,
        "Last_attendance":"2023-05-30 00:54:34"
    },

    "221":
    {
        "name":"Sagar Pal",
        "Major":"Computer Science",
        "Starting_year":2020,
        "total_attendance":3,
        "standing":"C",
        "year":3,
        "Last_attendance":"2023-05-30 00:54:34"
    },

    "297":
    {
        "name":"Vanshika Bajpai",
        "Major":"Computer Science",
        "Starting_year":2020,
        "total_attendance":10,
        "standing":"B",
        "year":3,
        "Last_attendance":"2023-05-30 00:54:34"
    },

    "321654":
    {
        "name":"Murtaza Hussan",
        "Major":"Robotics",
        "Starting_year":2017,
        "total_attendance":4,
        "standing":"D",
        "year":2,
        "Last_attendance":"2023-05-30 00:54:34"
    },

    "852741":
    {
        "name":"Emly Blunt",
        "Major":"Economics",
        "Starting_year":2018,
        "total_attendance":12,
        "standing":"B",
        "year":2,
        "Last_attendance":"2023-05-11 00:54:34"
    },

    "963852":
    {
        "name":"Elon Musk",
        "Major":"Physics",
        "Starting_year":2021,
        "total_attendance":7,
        "standing":"G",
        "year":3,
        "Last_attendance":"2023-05-11 00:54:34"
    }
}
for key,value in data.items():
    ref.child(key).set(value)
