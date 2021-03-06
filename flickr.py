#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import time

import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class App(object):
    def __init__(self):
        self.driver = webdriver.Chrome(settings.DRIVER_PATH)

    def _auth(self):
        self.driver.get('https://www.flickr.com/signin')

        self.driver.find_element_by_id('login-username').send_keys(
            settings.USERNAME_FLICKR)
        self.driver.find_element_by_id('login-signin').click()
        time.sleep(1)
        self.driver.find_element_by_id('login-passwd').send_keys(
            settings.PASS_FLICKR)
        self.driver.find_element_by_id('login-signin').click()
        time.sleep(5)

    def _wait_for_links(self, wait_class='li.favorites'):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wait_class)))

    def _like(self,
              skip=False,
              iterations=50,
              wait_class='li.favorites',
              selector='li.favorites:not(.is_fav) > a.rapidnofollow'):
        self._wait_for_links(wait_class)
        counter = 0
        for i in range(0, iterations):
            for link in self.driver.find_elements_by_css_selector(selector):
                try:
                    if not skip or (skip and random.randrange(1, 11) > 3):
                        self.driver.execute_script(
                            "window.scrollTo({}, {});".format(link.location[
                                'x'], link.location['y'] - 100))
                        link.click()
                    counter += 1
                    time.sleep(random.randrange(1, 3))
                except:
                    pass

                if counter > 1500:
                    print('Total: {}'.format(counter))
                    return True

            time.sleep(5)
            self._wait_for_links(wait_class)
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                load_more = self.driver.find_elements_by_xpath(
                    "//*[contains(text(), 'Load more')]")
                if not load_more:
                    load_more = self.driver.find_elements_by_xpath(
                        "//*[contains(@data-track, 'paginationRightClick')]")
                load_more[0].click()
                time.sleep(3)
            except:
                pass

        print('Total: {}'.format(counter))
        return True

    def run(self):
        self._auth()
        self._like(
            wait_class=".activity-card-content",
            selector="a.activity-card-fave:not(.faved)")

        # Flickrist group
        self.driver.get('https://www.flickr.com/groups/flickritis/pool/')
        self._like(
            skip=True,
            wait_class='i.fave-star',
            selector='i.fave-star.fave:not(.can-not-fave)')

        # FlickrToday
        self.driver.get('https://www.flickr.com/groups/flickrtoday/pool/')
        self._like(
            skip=True,
            wait_class='i.fave-star',
            selector='i.fave-star.fave:not(.can-not-fave)')

        # Flickr central
        self.driver.get('https://www.flickr.com/groups/central/pool/')
        self._like(
            skip=True,
            wait_class='i.fave-star',
            selector='i.fave-star.fave:not(.can-not-fave)')

        # Amateurs group
        self.driver.get('https://www.flickr.com/groups/amateurs/pool/')
        self._like(
            skip=True,
            wait_class='i.fave-star',
            selector='i.fave-star.fave:not(.can-not-fave)')

        # Canon EF 24-105mm f/4L IS USM group
        self.driver.get(
            'https://www.flickr.com/groups/canon24-105mmf4lis/pool/')
        self._like(
            skip=True,
            wait_class='i.fave-star',
            selector='i.fave-star.fave:not(.can-not-fave)')

        # Recent photos
        self.driver.get('https://www.flickr.com/explore')
        self._like(
            skip=True,
            wait_class='i.fave-star',
            selector='i.fave-star.fave:not(.can-not-fave)')

        self.driver.close()


if __name__ == "__main__":
    app = App()
    app.run()
