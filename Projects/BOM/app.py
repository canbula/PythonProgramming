from flask import Flask, render_template, request, redirect, url_for, session
from db import Firebase
from user import User
from note import Note
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField, CKEditor
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from chatbot import summariz

class NOTEForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content')
    submit = SubmitField('Submit')
    
class EditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content')
    submit = SubmitField('Submit')
    
class ChatForm(FlaskForm):
    BomAI = CKEditorField('BomAI',validators=[DataRequired()])
    submit = SubmitField('Submit')

chat=summariz()
ai=summariz()
app = Flask(__name__)
f = Firebase()
app.secret_key = "secretkey"
ckeditor = CKEditor(app)

@app.route('/')
def main():
    return render_template("anasayfa.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        try:
            f.login(mail, password)
            user = User(f.get_user_id(), f)
            user.save()
            session['user_id'] = f.get_user_id()
            return redirect(url_for('userpage', user_id=f.get_user_id()))
        except Exception as e:
            return render_template("login.html", error="Invalid User Information!")
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        password = request.form['password']
        mail = request.form['mail']
        username = request.form['username']
        f.register(mail, password)
        f.login(mail, password)
        user = User(f.get_user_id(), f)
        user.save()
        session['user_id'] = f.get_user_id()
        user.update({"username": username})
        return redirect(url_for('userpage', user_id=f.get_user_id()))
    return render_template("signup.html")

@app.route('/information', methods=['GET', 'POST'])
def information():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user = User(user_id, f)
    user_data = user.get()
    if request.method == 'POST':
        fullname = request.form['fullname']
        university = request.form['university']
        department = request.form['department']
        user.update({
            "fullname": fullname,
            "university": university,
            "department": department,
        })
    return render_template("information.html", user_data=user_data)

@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user = User(user_id, f)
    user_data = user.get()
    note = Note(user_id, f)
    notes = [note.get(note_id) for note_id in user.notes]
    note_id = request.args.get('note_id')
    selected_note = None
    if note_id:
        selected_note = f.ref.child(note.note_id)
    
    return render_template("userpage.html", user_data=user_data, note_data=notes, note=selected_note)

@app.route('/userpage/<note_id>', methods=['GET', 'POST'])
def show_notes(note_id):
    user_id = session.get('user_id')
    note = Note(user_id, f)
    user = User(user_id, f)
    user_data = user.get()
    notes = [note.get(note_id) for note_id in user.notes]
    selected_note_id=None
    for i in notes:
        if (note_id == i["note_idf"]):
            selected_note_id=i
            

    return render_template("userpage.html", user_data=user_data, note_data=notes, selected_note=selected_note_id)


@app.route("/add_notes", methods=['GET', 'POST'])
def add_notes():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user = User(user_id, f)
    user_data = user.get()
    form = NOTEForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            note = Note(user_id, f)
            note.title = form.title.data
            note.description = form.content.data
            note.create()
            note.note_idf = note.note_id
            note.update()
            return redirect(url_for('userpage'))
    return render_template("addnotes.html", form=form, user_data=user_data)

@app.route("/delete/<note_id>", methods=['GET', 'POST'])
def delete(note_id):
    user_id = session.get('user_id')
    ref = f.ref.child("notes").child(user_id)
    ref.child(note_id).delete()  
    return redirect(url_for('userpage'))

@app.route("/edit/<note_id>", methods=['GET', 'POST'])
def edit(note_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user = User(user_id, f)
    user_data = user.get()
    form = EditForm()
    note = Note(user_id, f)
    if request.method=="GET":  
        notes = [note.get(note_id) for note_id in user.notes]
        selected_note_id=None
        for i in notes:
                    if (note_id == i["note_idf"]):
                        selected_note_id=i
                        form.title.data=str(selected_note_id["title"])  
                        form.content.data=str(selected_note_id["description"])
                       

    else:
        if form.validate_on_submit():
            note = Note(user_id, f)
            updates = {
            "title": form.title.data,
            "description": form.content.data
            }
            f.ref.child("notes").child(user_id).child(note_id).update(updates)
            return redirect(url_for('userpage'))

    return render_template("edit-note.html",form=form, user_data=user_data,selected_note=selected_note_id)
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

@app.route("/summarize/<note_id>", methods=['GET', 'POST'])
def summarize(note_id):
    chat=summariz()
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    selected_note_id = None 
    summarize_description = ""
    text = ""
    user = User(user_id, f)
    user_data = user.get()
    form = EditForm()
    note = Note(user_id, f)
    if request.method == "GET":  
        notes = [note.get(note_id) for note_id in user.notes]
        selected_note_id = None
        for i in notes:
            if note_id == i["note_idf"]:
                selected_note_id = i
                form.title.data = str(selected_note_id["title"])  
                form.content.data = str(selected_note_id["description"])
                text = str(selected_note_id["description"])
                summarize_description = chat.model.generate_content(text + " : summarize.")
    elif request.method == "POST":
        action = request.form.get('action')
        if form.validate_on_submit():
            if action == "save":
                note = Note(user_id, f)
                updates = {
                    "title": form.title.data,
                    "description": form.content.data
                }
                f.ref.child(user_id).child(note_id).update(updates)
                return redirect(url_for('userpage'))
            elif action == "cancel":
                return redirect(url_for('userpage'))
            else:  # Summarize action
                note = Note(user_id, f)
                text = form.content.data
                summarize_description = chat.model.generate_content(text + " : verilen metni ozetle.")
            
                

    return render_template("sum.html", form=form, user_data=user_data, selected_note=selected_note_id, summarize_description=summarize_description.text)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    user = User(session.get("user_id"), f)
    user_data = user.get()
    form = ChatForm()
    question = ""
    answer_description = ""  # Initialize answer_description with a default value
    
    if request.method == "POST":
        question = form.BomAI.data
        if question:
            answer_description = ai.model.generate_content(question)
    
    return render_template("chat.html", form=form, answer_description=answer_description.text if answer_description else "",user_data=user_data)
    
if __name__ == "__main__":
    app.run(debug=True, port=5500)
