"""
Temporary library for pycomic program

Author: 
    Haw
"""

import os
import re, shutil
import random
import datetime, time
import pyautogui, pyperclip

from selenium import webdriver


class Driver():
    
    class DriverError(Exception):
        """
        Raise when selenium problem occurs
        """
        pass

    def __init__(self, title, url):
        self.driver = webdriver.Chrome()

        self.chapter_title = title
        self.chapter_url = url
        self.total_page = 0

        self.dir_path = '/tmp/pycomic'

    def get(self):
        self.driver.get(self.chapter_url)

    def find_last_page(self, last_page_selector):
        regex = re.compile(r'\d{1,3}')
        element = self.driver.find_element_by_css_selector(last_page_selector)

        try:
            self.total_pages = int(regex.search(element.text).group())
        except Exception as err:
            raise self.DriverError(err)

    def get_urls_and_images(self, image_id, next_page_selector, error_text='URL error occurs'):
        self.urls = []

        # Temporary save location
        if os.path.isdir(self.dir_path):
            shutil.rmtree(self.dir_path)
        os.mkdir(self.dir_path)

        for counter in range(self.total_pages):
            for _ in range(5):
                try:
                    url = self._comic_image_url(image_id)
                    print('Page {} url {}'.format(counter, url))
                except self.DriverError:
                    self.driver.refresh()
                    continue
                else:
                    break
            else:
                print('Page {} {}'.format(counter, error_text))

            self.urls.append(url)
            next_page = self.driver.find_element_by_id(next_page_selector)
            time.sleep(random.uniform(2, 3.5))
            next_page.click()

        self.driver.close()

    def _comic_image_url(self, image_id):
        source, tag = 'src', 'img'

        try:
            element = self.driver.find_element_by_id(image_id)
            webpage = element.get_attribute(source)
            self.driver.execute_script("window.open('{page}');".format(page=webpage))
            time.sleep(1.2)
            self.driver.switch_to.window(self.driver.window_handles[1])
            image_tag = self.driver.find_element_by_tag_name(tag)
            image_url = image_tag.get_attribute(source)

            # Save image action
            filename = datetime.datetime.now().strftime('%Y%m%dT%H%M%SMS%f')
            file_path = '{}/{}'.format(self.dir_path, filename)
            pyperclip.copy(file_path)
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 's') # Show save image popup
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v') # Paste image path
            # pyautogui.typewrite(file_path, interval=0.1) # Type in file path
            pyautogui.press('enter') # Save image to temp directory
        except Exception as err:
            raise self.DriverError(err)
        finally:
            for handle in self.driver.window_handles[1:]:
                self.driver.switch_to.window(handle)
                self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        return image_url
            
            




    