# Password checker API

Given a password, assess its robustness, based on character set and password dictionaries

## Architecture
### Python backend

A [Flask](https://flask.palletsprojects.com/) powerer API.

Unit tests are in doctests, and integration ones in xxx_test.py

### web frontend

## Sources
### password dictionaries
A few dictionaries are checked. They reside in the `flask/resources/dictionaries` folder.

  * `french_passwords_top20000.txt` from [Richelieu](https://github.com/tarraschk/richelieu)
  * `10k-most-common.txt` from [SecLists](https://github.com/danielmiessler/SecLists)
