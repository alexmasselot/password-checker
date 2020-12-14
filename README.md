# Password checker API

Given a password, assess its robustness, based on character set and password dictionaries

## Architecture
### Python backend

A [Flask](https://flask.palletsprojects.com/) powerer API.

As good default practices, use a virtual environment, install dependencies `pip install -f requirements.txt`


#### TEsting

Unit tests are in doctests, and integration ones in xxx_test.py

To run all of them

    pytest 

To run all of them, on file changes (useful in dev)
   
    ptw 

#### Check it out
Once the API is running (`flask run`), you can visit:
```
http://127.0.0.1:5000/paf%20le%20chien
```

### web frontend

## Sources
### password dictionaries
A few dictionaries are checked. They reside in the `flask/resources/dictionaries` folder.

  * `french_passwords_top20000.txt` from [Richelieu](https://github.com/tarraschk/richelieu)
  * `10k-most-common.txt` from [SecLists](https://github.com/danielmiessler/SecLists)
