<h1 align="center"> TableTracker</h1>

<p align="center">
<img src="https://github.com/Musa-Sina-Ertugrul/DBScanner/assets/102359522/1ea4b501-898f-4b57-8a7e-90e853d50cdd">
</p>

<h3 align="center"> Our Purpose</h3>

<p align="center">
<img src="https://github.com/Musa-Sina-Ertugrul/TableTracker/assets/102359522/cd2e98f0-083e-44f4-a532-e4e9b9a29c47">
</p>


# TableTracker

> TableTracker is a desktop application developed in Python that facilitates tracking and managing SQLite database tables. This application allows you to execute SQL queries on SQLite databases, visualize the results, and edit your queries.
* Assigned by Asc. Prof. Dr. Bora CANBULA

<h3 align="center">Requirements</h3>
> Python 3.11 or a newer version

<h3 align="center">Setup</h3>

> To create the necessary virtual environment in the project directory, run the following command:

```console
conda create -n TableTracker python=3.11 pip -y
```

> Activate the created virtual environment:

```console
conda activate TableTracker
```

> To install required modules

```console
pip install -r requirements.txt
```

<h3 align="center">Reformatting</h3>

> For reformatting use <b><i>black</i></b>. It reformat for pep8 as same as pylint but better !!!

```console
black .
```

<h3 align="center">Run App</h3>

> To start the application, run the following command:

```console
python table_tracker
```

> .When the application starts, you can create a new SQLite database or connect to an existing one.
> Write your SQL queries in the text box and execute the query by clicking the "Execute" button.
> The results will be displayed in the "Output Window" section.

<h3 align="center">Linting</h3>

> For running <b><i>pylint</i></b>

```console
pylint ./table_tracker/ ./test/
```

<h3 align="center">Testing</h3>

> For running <b><i>unittest</i></b>

```console
python -m unittest discover -v
```
<h3 align="center">Author</h3>
> Musa Sina Ertuğrul, İrem Demir
