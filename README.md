# ICBooks

## Summary
ICBooks is a book swapping service intended to allow Imperial College students to list books for swap, and organise swaps with their peers. [See the site live here!](https://icbooks.impaas.uk/)

It is deployed on a Tsuru server, and the tech stack includes Flask, PostgreSQL, SQLAlchemy and HTML/CSS/JS (with Jinja2 templating). It makes use of [OpenLibrary's public Search API](https://openlibrary.org/dev/docs/api/search) to fetch information about a book. Photo credit for covers also goes to OpenLibrary. 

ICBooks uses a Github Actions deployment pipeline for CI/CD, with automated format checking, test control and deployment on pushing.

## Usage

Steps to run a local version of ICNews

#### Clone the repository
```
git clone git@github.com:palmwi2010/icnews.git
```

#### Create and activate a venv
```
python -m venv venv
source venv/bin/activate
```
#### Install packages
```
pip install -r requirements.txt
```

#### Create a branch
```
git checkout -b [branch_name]
```

#### Run on a local server
```
flask run --debug
```

#### Install pre commit for format checking
```
pre-commit install
```
To check if the current directory will pass pre commit checks, run:
```
pre-commit run --all-files
```

#### When pushing to remote, set an upstream branch like the below
```
git push -u origin [branch_name]
```
