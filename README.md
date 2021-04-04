# App Listing API

A REST API for an app store like application project using `fastapi` and `dataset`, setup for easy deployment on `heroku`.
Use the ADMIN_USERNAME, ADMIN_PASSWORD and ADMIN_EMAIL enviroment variables to add an admin user during startup

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## To Do
- [ ] External auth
- [ ] Change password
- [ ] Admin dashboard

## Usage

Clone the repo

```sh
$ git clone https://github.com/Ju99ernaut/app-listing-server.git
$ cd app-listing-server
```

Create virtual enviroment

```sh
$ python -m venv venv
```

Activate virtual enviroment

Linux/MacOS: `source venv/bin/activate`
Windows: `.\venv\Scripts\Activate.ps1` or `.\venv\Scripts\activate`

Install dependencies

> Use `requirements.txt` in production

```sh
$ pip install -r requirements.dev.txt`
```

Run tests

```sh
$ cd api 
$ python -m pytest
$ cd ..
```

Run

```sh
$ python api/main.py
```

The API should now be available at `http://127.0.0.1:8000` and the API documentation will be available at `/docs` or `/redoc`.


## License

MIT
