from flask import render_template, redirect, url_for, flash, request, abort
from app import app, db, bcrypt
from app.models import Page, User, CalendarEvent
from app.forms import RegistrationForm, LoginForm, PageForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    pages = Page.query.filter_by(author=current_user, deleted=False).all()
    trash_pages = Page.query.filter_by(author=current_user, deleted=True).all()
    events = CalendarEvent.query.all()
    return render_template('index.html', pages=pages, trash_pages=trash_pages, events=events)

@app.route('/page/<int:page_id>')
@login_required
def page(page_id):
    page = Page.query.get_or_404(page_id)
    if page.author != current_user:
        abort(403)
    return render_template('page.html', page=page)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form.get('date', None)
        content_with_date = f"Date: {date}\n\n{content}" if date else content
        new_page = Page(title=title, content=content_with_date, author=current_user)
        db.session.add(new_page)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:page_id>', methods=['POST'])
@login_required
def delete(page_id):
    page = Page.query.get_or_404(page_id)
    if page.author != current_user:
        abort(403)
    page.deleted = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/trash')
@login_required
def trash():
    pages = Page.query.filter_by(author=current_user, deleted=True).all()
    return render_template('trash.html', pages=pages)

@app.route('/restore/<int:page_id>', methods=['POST'])
@login_required
def restore(page_id):
    page = Page.query.get_or_404(page_id)
    if page.author != current_user:
        abort(403)
    page.deleted = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/permanent_delete/<int:page_id>', methods=['POST'])
@login_required
def permanent_delete(page_id):
    page = Page.query.get_or_404(page_id)
    if page.author != current_user:
        abort(403)
    db.session.delete(page)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:page_id>', methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    page = Page.query.get_or_404(page_id)
    if page.author != current_user:
        abort(403)
    form = PageForm()
    if form.validate_on_submit():
        page.title = form.title.data
        page.content = form.content.data
        db.session.commit()
        flash('Page has been updated!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = page.title
        form.content.data = page.content
    return render_template('edit_page.html', form=form, page=page)

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
    title = request.form['title']
    description = request.form['description']
    date = request.form['date']
    new_event = CalendarEvent(title=title, description=description, start_date=date)
    db.session.add(new_event)
    db.session.commit()
    flash('Event has been added!', 'success')
    return redirect(url_for('index'))
