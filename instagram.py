#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time

from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings


class App(object):
    def __init__(self):
        self.driver = webdriver.Chrome(settings.DRIVER_PATH)
        self.counter = 0

    def _auth(self):
        self.driver.get('https://www.instagram.com/')
        self.driver.find_elements_by_xpath("//a[contains(text(), 'Log in')]")[
            0].click()
        self.driver.find_element_by_name('username').send_keys(
            settings.USERNAME_INSTAGRAM)
        self.driver.find_element_by_name('password').send_keys(
            settings.PASS_INSTAGRAM)
        self.driver.find_elements_by_xpath(
            "//button[contains(text(), 'Log in')]")[0].click()
        time.sleep(5)

    def _wait_for_links(self, wait_class='img'):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_class)))

    def _like(self,
              skip=False,
              iterations=50,
              wait_selector="article",
              selector='span.coreSpriteLikeHeartOpen',
              popup=None):
        self._wait_for_links(wait_selector)
        print('Start on URL {}'.format(self.driver.current_url))
        counter = 0
        done = []
        for i in range(0, iterations):
            for link in self.driver.find_elements_by_css_selector(selector):
                if (not skip or (skip and random.randrange(1, 11) > 2)) and (
                        link.get_attribute('href') not in done or not popup):
                    done.append(link.get_attribute('href'))
                    self.driver.execute_script(
                        "window.scrollTo({}, {});".format(link.location[
                            'x'], link.location['y'] - 100))
                    try:
                        link.click()
                        time.sleep(random.randrange(1, 2))
                    except WebDriverException:
                        print('link exception')
                    if popup:
                        time.sleep(random.randrange(1, 2))
                        try:
                            self.driver.find_element_by_css_selector(
                                popup).click()
                        except NoSuchElementException:
                            # print('heart exception')
                            pass
                        try:
                            self.driver.find_element_by_css_selector(
                                'button._3eajp').click()
                        except NoSuchElementException:
                            print('close exception')
                            pass
                    counter += 1
                    self.counter += 1
                    print('Likes: {}'.format(self.counter))
                    time.sleep(random.randrange(1, 2))

                    if counter > settings.MAX_PHOTOS_INSTAGRAM:
                        print('Total: {}'.format(counter))
                        return True

            load_more = self.driver.find_elements_by_xpath(
                "//a[contains(text(), 'Load more')]")
            if len(load_more):
                try:
                    load_more[0].click()
                except WebDriverException:
                    print('load_more exception')
                    pass

            time.sleep(random.randrange(1, 2))
            self._wait_for_links(wait_selector)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

        print('Total on URL {}: {}'.format(self.driver.current_url, counter))
        return True

    def run(self):
        self._auth()
        self._like()

        for tag in settings.TAGS_INSTAGRAM:
            self.driver.get(
                'https://www.instagram.com/explore/tags/{}/'.format(tag))
            self._like(
                selector='a._8mlbc',
                wait_selector='a._8mlbc',
                popup='span.coreSpriteLikeHeartOpen')
        self.driver.close()


if __name__ == "__main__":
    app = App()
    app.run()
