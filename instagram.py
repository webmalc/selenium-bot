#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import settings


class App(object):

    tags = [
        'детскаяфотосессия', 'фотограф', 'фотография', 'свадебнаяфотография', 'lovestory',
        'дети', 'красота'
    ]

    def __init__(self):
        self.driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

    def _auth(self):
        self.driver.get('https://www.instagram.com/')
        self.driver.find_elements_by_xpath("//a[contains(text(), 'Log in')]")[0].click()
        self.driver.find_element_by_name('username').send_keys(settings.USERNAME_INSTAGRAM)
        self.driver.find_element_by_name('password').send_keys(settings.PASS_INSTAGRAM)
        self.driver.find_elements_by_xpath("//button[contains(text(), 'Log in')]")[0].click()
        time.sleep(5)

    def _wait_for_links(self, wait_class='img'):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_class))
        )

    def _like(self, skip=False, iterations=50, wait_selector="article", selector='span.coreSpriteHeartOpen', popup=None):
        self._wait_for_links(wait_selector)
        counter = 0
        for i in range(0, iterations):
            for link in self.driver.find_elements_by_css_selector(selector):
                if not skip or (skip and random.randrange(1, 11) > 2):
                    link.click()
                    if popup:
                        time.sleep(random.randrange(1, 3))
                        try:
                            self.driver.find_element_by_css_selector(popup).click()
                        except NoSuchElementException:
                            pass
                        try:
                            self.driver.find_element_by_css_selector('button._3eajp').click()
                        except NoSuchElementException:
                            pass
                counter += 1
                time.sleep(random.randrange(1, 3))

                if counter > 500:
                    print('Total: {}'.format(counter))
                    return True

            time.sleep(random.randrange(3, 5))
            load_more = self.driver.find_elements_by_xpath("//a[contains(text(), 'Load more')]")
            if len(load_more):
                try:
                    load_more[0].click()
                except WebDriverException:
                    print('load_more exception')
                    pass

            self._wait_for_links(wait_selector)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print('Total: {}'.format(counter))
        return True

    def run(self):
        self._auth()
        self._like()

        for tag in self.tags:
            self.driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
            self._like(selector='a._8mlbc', wait_selector='a._8mlbc', popup='span.coreSpriteHeartOpen')
        self.driver.close()


if __name__ == "__main__":
    app = App()
    app.run()
