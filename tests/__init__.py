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
from nose.tools import eq_
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


def test_index_selenium():
    driver.get('http://localhost:5000/')

    result = driver.find_element_by_class_name('mission').text
    mission = ("GetPost is a 21st-century take on the Oberlin mailroom. We "
               "aim to save both students and employees a significant amount "
               "of time and energy by allowing package information to be "
               "stored and viewed online. No longer will anyone have to walk "
               "all the way up to Wilder Hall in order to check on a package, "
               "just to learn that it hasn't arrived yet and that they'll be "
               "forced to repeat themselves the day after! In short, GetPost "
               "brings the mailroom directly to you."
               )

    eq_(
        result,
        mission,
        'Home page contents are incorrect.'
        )


def test_ping():
    test_app = app.test_client()
    rv = test_app.get('/ping')
    rv_string = rv.data.decode('utf-8')
    eq_(
        rv_string,
        'What the brangan.',
        'Ping response string not identical'
    )
