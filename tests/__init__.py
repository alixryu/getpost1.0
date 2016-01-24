""":mod:`tests` --- Test module of getpost
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Command:
        $ nosetests -sv

    Flags:
        -s, --nocapture
            Don't capture stdout.

        -v=DEFAULT, --verbose=DEFAULT
            Be more verbose.

"""
from selenium import webdriver

from getpost.config import TestConfig
from getpost import create_app


app = create_app(TestConfig)
driver = webdriver.Firefox()


def setup_package():
    "set up pre-test configurations"
    app.config['TESTING'] = True


def teardown_package():
    "tear down pre-test configurations"
    app.config['TESTING'] = False
    driver.close()


from tests.hogwarts import *
