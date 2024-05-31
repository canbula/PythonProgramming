from flask import Flask, render_template,request
import random
from textbox import TextBoxDb
 
from db import Firebase
app = Flask(__name__)
 
datas=[]
link = "quick_note"
 

f = Firebase()
f.login("prof@university.edu", "password")
 
@app.route("/")
def home_page():
    datas = paragraph()
    if len(datas) !=0:
        return render_template("index.html", items = datas)
    

    return render_template("index.html")
 
 

 
@app.route("/yapilacaklar", methods=["GET","POST"])
def add_textbox():
    if request.method == "POST":
        todo_name = request.form['input-box']
        cur_id = random.randint(1,10000)
        cur_id = str(cur_id)
        textBox= TextBoxDb( cur_id, link,f)
        textBox.class_ = link
        textBox.id = (
        cur_id)
 
        textBox.paragraph = todo_name
        textBox.create()
       
        return render_template("index.html", items = paragraph()) 
 
    else:
        return render_template("error.html")
   
 

@app.route("/delete/<todo_id>", methods=["GET","POST"])
def delete(todo_id):
    datas = []
   
    ref = f.ref
    for i in link.split('/'):
        ref =  ref.child(i)
 
    for j in ref.get():
        item = ref.child(j).get()
        if item and "id" in item and str(item["id"]) == todo_id:
            datas= paragraph()
            if len(datas) >1:
                ref.child(j).delete()
            datas =paragraph()
 
    return render_template("index.html", items = datas)
   
 
@app.route("/update/<int:todo_id>", methods=["GET", "POST"])
def update(todo_id):
    todo_paragraph = request.form['box']
    print(todo_paragraph)
    update_data = {
    'paragraph': todo_paragraph,
    'id': todo_id,
    'class_': ''
    }
    ref = f.ref
    for i in link.split('/'):
        ref =  ref.child(i)
 
    for j in ref.get():
        item = ref.child(j).get()
        if item and "id" in item and str(item["id"]) == str(todo_id):
            ref.child(j).update(update_data)
 
    return render_template("index.html", items = paragraph())
      
 
def paragraph():
    datas = []
   
    ref = f.ref
    for i in link.split('/'):
        ref =  ref.child(i)
 
    for j in ref.get():
        if "paragraph" in ref.child(j).get():
                paragraph = ref.child(j).get()["paragraph"]
                id = ref.child(j).get()["id"]
                datas.append({"paragraph": paragraph, "id": id})
 
    return datas

"""

@app.route('/route', methods=['POST'])
def button_click():
    data = request.get_json()
    link = data['buttonId']
    # Buton idsini işle
    print("Buton ID'si:", link)

       return redirect(url_for('home_page'))



"""
 
 
 
if __name__ == "__main__":
 
 
    app.run()