# Pytonotes 📒

Pytonotes is clone of Notion. And, is created by students of Manisa Celal Bayar University for project of Python Programming course. In this project we used; Django, Bootstrap, FontAwesome and IBM Plex Font Family.

## Members of Project ️🧑‍💻🧑‍💻🧑‍💻

- **Farid Mammadov** - `200315093`
- **Mert Can Fidan** - `200315091`
- **Orkun Altınyelken** - `220315001`

## Compability ✅ :

- Python 3.10 or newer
- Django 5
- Bootstrap 5 and Font Awesome 6 -> Includes in project file.


## Installation of Requirements 🛠️ : 
Ensure you're in the root directory of Pynotion and execute the following command in your terminal:

```sh
pip install -r requirements.txt
```

In case of problem with versions, you can try this command too;

```sh
pip install --upgrade -r requirements.txt
```


## Database Setup 💾 : 
We've got your back with an SQLite. And, you can easy setup your database with these commands;

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py seed_db
```

## Launching Pytonotes 🚀 : 
Now! It's time to run NotinPy. You can simply run Pytonotes with only this command:

```sh
python manage.py runserver
```

Open your browser and type http://127.0.0.1:8000/ to Adress Bar for use Pytonotes.

## Examples and Adding More Data

There is already several user created for startup, if you want to reinstall examples you need to use this command again;

```sh
python manage.py seed_db
```

Also, if you want to expand examples you can insert data to `/notes/management/seed_db.py`. And, these are our default examples users which's you can just login to and created by us;

> user1@example<span>.com<br />
> password1

> user2@example<span>.com<br />
> password2

> user2@example<span>.com<br />
> password2

> user2@example<span>.com<br />
> password2

## Currently Missing Features

> [!WARNING]  
> Because of our project is not commercial, we are not included work accounts or releative things. Mainly, focused on default Notion properties.

- User validation after registration process
- 2FA
- Custom User Profile Images
- Adding another account to same client. (Basically, there is no support for more than one account on same time)
- Search function
- Home Page
- Settıngs & Members menu.
- Creating new pages
- Adding pages to Favorites
- Last edited indicator
- Auto save after edit. (Currently we can save but manually via button, not after editing files.)
- Sharing (Actually we can currently share workspaces but there is missing integration for this.)
- Comments
- Updates
- Editor Settings
- Calendar
- Trash
- Creating Teamspace
- Ellipsis drop down menus currently not works on shared Workspaces. (But works on owned Workspaces.)
- Views and Views Group (Currently we are only have title and text view.)



