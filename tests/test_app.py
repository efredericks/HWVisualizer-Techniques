# https://github.com/miguelgrinberg/flack/blob/master/tests/tests.py
import unittest

from flask import Flask, abort, url_for
from flask_testing import TestCase, LiveServerTestCase

from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from server import app, socketio, isDone
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time
import os


class TestBase(LiveServerTestCase):
    def create_app(self):
        # app = Flask(__name__)
        # app.config['SECRET_KEY'] = 's3cr3t'
        self.app = app
        app.config.update(
            LIVESERVER_PORT=8081
        )
        # bootstrap = Bootstrap(app)
        # socketio = SocketIO(app)

        self.ctx = self.app.app_context()
        self.client = self.app.test_client()

        return app#socketio

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(r'/mnt/c/chromedriver/chromedriver.112.exe', chrome_options=chrome_options)
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()
        # self.ctx.pop()

    def test_server_is_running(self):
        global isDone # terrible terrible hack

        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
        time.sleep(10)

        if os.path.exists('tests/client-done'):
        # if isDone:
            print(">>> WOO IT FINISHED YAY")
        else:
            print(">>> NOO IT DID NOT FINISH ARGHGHGHGH")

        # client = socketio.test_client(self.app)
        # recvd = client.get_received()
        # timeout = 100
        # while timeout > 0:
        #     client = socketio.test_client(self.app)
        #     recvd = client.get_received()
        #     print("RX: {0}".format(recvd))
        #     timeout-=1
        #     time.sleep(0.05)


    """
    def test_socketio(self):
        client = socketio.test_client(self.app)
        recvd = client.get_received()

        # time.sleep(1.5)
        # client.emit('get_status', None)
        # recvd = client.get_received()
        # print("RX", recvd)
        # print(recvd[0])

        # time.sleep(10)
        # client.emit('status', None)
        # recvd = client.get_received()
        # self.assertEqual(len(recvd), 1)
        # print(recvd[0])



        timeout = 1000
        while timeout > 0:
            client.emit('get_status', None)
            recvd = client.get_received()
            print("RX", recvd)
            # if recvd == "done":
        #     # if recvd != []:
        #     print("RECEIVED: {0}".format(recvd[0]))
        #         # break
            timeout -= 1
            time.sleep(0.1)
    """

if __name__ == "__main__":
    unittest.main()

