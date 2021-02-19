from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestApiPages(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome('functional_test/chromedriver.exe')
    
    def tearDown(self):
        self.browser.close()
    
    def test_api_list_displayed(self):
        self.browser.get(('%s%s' % (self.live_server_url, '/api/')))
        time.sleep(20)