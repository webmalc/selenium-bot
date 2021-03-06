#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings


class App(object):
    def __init__(self):
        self.driver = webdriver.Chrome(settings.DRIVER_PATH)
        self.counter = 0

    def _auth(self):
        self.driver.get('https://500px.com/login')

        self.driver.find_element_by_name('email').send_keys(
            settings.USERNAME_500PX)
        self.driver.find_element_by_name('password').send_keys(
            settings.PASS_500PX)
        self.driver.find_element_by_css_selector(
            'input.unified_signup__submit_button').click()
        time.sleep(5)
        self.driver.get('https://500px.com/')

    def _wait_for_links(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.new_fav")))

    def _like(self, skip=False, iterations=30):
        print('Start on URL {}'.format(self.driver.current_url))
        self.driver.execute_script(
            "window.scrollTo(document.body.scrollWidth, 0);")
        self._wait_for_links()
        counter = 0

        for i in range(0, iterations):
            for link in self.driver.find_elements_by_css_selector(
                    'a.new_fav:not(.hearted)'):
                try:
                    if not skip or (skip and random.randrange(1, 11) > 3):
                        self.driver.execute_script(
                            "window.scrollTo({}, {});".format(link.location[
                                'x'], link.location['y'] - 100))
                        link.click()
                    counter += 1
                    self.counter += 1
                    print('Likes: {}'.format(self.counter))
                    time.sleep(random.randrange(3, 7))
                except:
                    pass

                if self.driver.find_elements_by_xpath(
                        "//*[contains(text(), 'Too many requests')]"):
                    print('Ban on URL {}: {}'.format(self.driver.current_url,
                                                     counter))
                    return True
                if counter > 500:
                    print('Total on URL {}: {}'.format(self.driver.current_url,
                                                       counter))
                    return True

            self.driver.execute_script(
                "window.scrollTo(document.body.scrollWidth, document.body.scrollHeight);"
            )
            self._wait_for_links()

        print('Total on URL {}: {}'.format(self.driver.current_url, counter))

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
