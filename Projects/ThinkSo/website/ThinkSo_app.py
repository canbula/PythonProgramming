from flask import Flask, redirect, render_template, request, url_for, session, jsonify
from website.models import Note, User
from website.database import Firebase

db = Firebase()
_USER = None
default_data = {
    "log_text": 'log in',
    "user": ""
}

class ThinkSo:
    app = Flask(__name__, template_folder="../website/templates")

    def run(self, debug=True):
        self.app.run(debug=debug)
    
    @app.route('/')
    def root():
        global default_data
        data = default_data
        data.update({"log_url": url_for('login_page')})
        if _USER not in [None, False]:
            data = {
                "log_url": url_for('logout_page'),
                "log_text": 'log out',
                "user": "Welcome " + str(_USER.name) + " :)"
            }
            return redirect('/note')
        return render_template('homepage.html', data=data)

    @app.route("/homepage")
    def home_page():
        data = {
            "log_url": url_for('logout_page'),
            "log_text": 'log out',
            "user": "Welcome " + str(_USER.name) + " :)"
        }
        if _USER not in [None, False]:
            data = default_data
            data.update({"log_url": url_for('login_page')})
            return redirect('/note')

        return render_template('homepage.html', data=data)

    @app.route('/logout')
    def logout_page():
        global _USER
        _USER = None

        return redirect("/")

    @app.route("/login/", methods=["GET", "POST"])
    def login_page():
        global _USER
        if request.method == "POST":
            email = request.form.get("email")
            pw = request.form.get("password")
            if email and pw:
                user = db.is_user_exists(email=email, pw=pw, get_user_obj=True)
                if user is not False:
                    _USER = user
            return redirect("/")
        return render_template("login.html")

    @app.route("/calendar")
    def calendar_page():
        return render_template('calendar.html')

    @app.route("/blog")
    def blog_page():
        return render_template('blog.html')

    @app.route("/note", methods=["GET", "POST"])
    def note_page():
        global _USER
        if _USER not in [None, False]:
            _USER = db.get_user(_USER.id) # update user info
            user_notes = db.get_notes(_USER.notes, raw=True)
            user_notes = [note for note in user_notes if note is not None] # Filtreleme adımı
            if request.method == "POST":
                title = request.form.get("note_title")
                text = request.form.get("note_text")
                if 'permission' not in title.lower() and 'username' not in title.lower():
                    if title or text:
                        db.add_note(user_ids=[_USER.id], title=title, content=text)
                        return redirect(url_for('note_page', note_title=title, note_desc=text, add_new_note=True))
            return render_template('note.html',
                                   add_new_note=request.args.get('add_new_note'),
                                   note_title=request.args.get('note_title'),
                                   note_desc=request.args.get('note_desc'),
                                   user_notes=user_notes,
                                   _USER=_USER)
        else:
            return redirect('/')

    @app.route("/update_note/<int:note_id>", methods=["POST"])
    def update_note(note_id):
        note_id = request.form.get("note_id")
        title = request.form.get("title")
        content = request.form.get("content")
        if note_id and title and content:
            db.update_note(note_id, title, content)
            return jsonify(success=True)
        return jsonify(success=False)

    @app.route("/add_user/<int:note_id>", methods=["POST"])
    def add_user(note_id):
        try:
            add = request.form.get("add")
            note_id = request.form.get("note_id")
            content = request.form.get("content")
            user_names = content.split(",")
            users = [db.get_uid(user_name, "name") for user_name in user_names]
            user_ids = db.ref_notes.child(note_id).child("user_ids").get()
            if not user_ids or len(user_ids) < 0:
                return jsonify(success=False)
            
            for user in users: # add user ids into the note info on DB
                if add.lower() == "add" and user not in user_ids:
                    user_ids.append(user)
                if add.lower() == "remove" and user in user_ids:
                    user_ids.remove(user)
            db.ref_notes.child(note_id).child("user_ids").set(user_ids)

            for uid in users:  # add/remove  note id into all of the users info on DB
                usr = db.get_user(uid=str(uid))
                if add.lower() == "add":
                    usr.notes.append(int(note_id))
                elif int(note_id) in usr.notes:
                    usr.notes.remove(int(note_id))
                usr.notes = list(set(usr.notes))
                db.ref_users.child(str(uid)).child("notes").set(usr.notes)

            if len(user_ids) == 0:
                db.delete_note(note_id)

            return jsonify(success=True)
        except Exception as e:
            return jsonify(success=False)

    @app.route('/delete_note/<int:note_id>', methods=['DELETE'])
    def delete_note_page(note_id):
        global _USER
        if _USER not in [None, False]:
            db.delete_note(note_id)
            _USER = db.get_user(_USER.id) # update user info
            return '', 204
        else:
            return '', 401
