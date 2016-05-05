#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import settings


class App(object):

    def __init__(self):
        self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

    def _auth(self):
        self.driver.get('https://500px.com/following')
        self.driver.find_element_by_name('email').send_keys(settings.USERNAME)
        self.driver.find_element_by_name('password').send_keys(settings.PASS)
        self.driver.find_element_by_css_selector('input.login_only').click()

    def _wait_for_links(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.new_fav"))
        )

    def _like(self, skip=False):
        self._wait_for_links()
        counter = 0
        for i in range(0, 3):
            for link in self.driver.find_elements_by_css_selector('a.new_fav:not(.hearted)'):
                try:
                    if not skip or (skip and random.randrange(1, 11) > 3):
                        link.click()
                    counter += 1
                    time.sleep(random.randrange(1, 3))
                except:
                    pass
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self._wait_for_links()

        print('Total: {}'.format(counter))

    def run(self):
        # following
        self._auth()
        self._like()

        # fresh
        self.driver.get('https://500px.com/fresh')
        self._like(skip=True)

        # fresh
        self.driver.get('https://500px.com/upcoming')
        self._like(skip=True)

        # popular
        self.driver.get('https://500px.com/popular')
        self._like(skip=True)

        self.driver.close()

if __name__ == "__main__":
    app = App()
    app.run()
