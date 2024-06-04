
import pyrebase  # pip install pyrebase4
import firebase_admin
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render



firebaseConfig={
  "apiKey": "AIzaSyAAjXMkjpkLnDRNpm4tUjxIbUuSRQuSci0",
  "authDomain": "noteis-2496d.firebaseapp.com",
  "databaseURL": "https://noteis-2496d-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "noteis-2496d",
  "storageBucket": "noteis-2496d.appspot.com",
  "messagingSenderId": "1096730103318",
  "appId": "1:1096730103318:web:b30588bfdf2f04a91aef37",
  "measurementId": "G-RMR9EH3LTD"
}
firebase=pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()




   
    

class Database:
    def register(self,email, password):
        addUser = firebase.auth().create_user_with_email_and_password(email, password)

    def sign_in(self,email,password):
        user = firebase.auth().sign_in_with_email_and_password(email,password)
    
    def adddata(self,baslik,icerik):
        data={"baslik":baslik,"icerik":icerik}
        database.push(data)

    def get_data(self):
        # Tüm veritabanı verilerini çek
        all_data = database.get()
        return all_data.val()
    
    def delete_data(self, data_id):
        # Veritabanından belirli bir veriyi sil
        database.child(data_id).remove()