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
        self.driver = webdriver.Chrome(settings.DRIVER_PATH)

    def _auth(self):
        self.driver.get('https://500px.com/login')
        self.driver.find_element_by_name('email').send_keys(settings.USERNAME_500PX)
        self.driver.find_element_by_name('password').send_keys(settings.PASS_500PX)
        self.driver.find_element_by_css_selector('input.unified_signup__submit_button').click()
        time.sleep(5)
        self.driver.get('https://500px.com/')

    def _wait_for_links(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.new_fav"))
        )

    def _like(self, skip=False, iterations=3):
        self._wait_for_links()
        counter = 0

        for i in range(0, iterations):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        for link in self.driver.find_elements_by_css_selector('a.new_fav:not(.hearted)'):
            try:
                if not skip or (skip and random.randrange(1, 11) > 3):
                    link.click()
                counter += 1
                time.sleep(random.randrange(1, 3))
            except:
                pass

        print('Total: {}'.format(counter))

    def run(self):
        # following
        self._auth()
        self._like()

        # activity
        self.driver.get('https://500px.com/activity')
        self._like(skip=True)

        # fresh
        self.driver.get('https://500px.com/fresh')
        self._like(skip=True)

        # fresh
        self.driver.get('https://500px.com/upcoming')
        self._like(skip=True)

        # popular
        self.driver.get('https://500px.com/popular')
        self._like(skip=True)

        # popular
        self.driver.get('https://500px.com/editors')
        self._like(skip=True)

        self.driver.close()

if __name__ == "__main__":
    app = App()
    app.run()
