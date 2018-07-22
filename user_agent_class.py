"""
Program:
    User-agent data for use in web scraping
Author:
    haw
Version:
    1.1
"""

import sys, random, logging
import requests
import logging_class
from bs4 import BeautifulSoup
from datetime import datetime


URL_COMPUTER = 'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/computer/'
URL_PHONE = 'https://developers.whatismybrowser.com/useragents/explore/hardware_type_specific/phone/'

SELECTOR = 'td.useragent a'
logger = logging_class.PersonalLog('user_agent_class')

logging.disable(logging.DEBUG)


class UserAgent():

    def __init__(self):
        # Default user agent value
        self._filename = 'user_agents-' + datetime.now().strftime('%Y%m%d')


    def random_computer(self):
        """
        Success: Return a random user-agent
        Failed: Return an empty list
        """
        return self._load_random(URL_COMPUTER)

    def random_phone(self):
        """
        Success: Return a random user-agent
        Failed: Return an empty list
        """
        return self._load_random(URL_PHONE)

    def write_computer(self):
        self._filename = 'user_agents-computer-' + datetime.now().strftime('%Y%m%d')
        self._write_file(URL_COMPUTER)

    def write_phone(self):
        self._filename = 'user_agents-phone-' + datetime.now().strftime('%Y%m%d')
        self._write_file(URL_PHONE)


    def _load_random(self, url):
        """
        Randomly return an user-agent value
        or an empty list if no data is fetched
        """
        selected_list = self._scrape_for_user_agent(url)

        try:
            user_agent = random.choice(selected_list)
            logger.debug('User-Agent: {}'.format(user_agent.text))
        except IndexError:
            return selected_list
        else:
            return user_agent.text


    def _write_file(self, url):
        """
        Save user-agent data to file
        """
        selected_list = self._scrape_for_user_agent(url)

        if len(selected_list) != 0:
            with open(self._filename, 'w') as write_file:
                for elem in selected_list:
                    write_file.write('{}\n'.format(elem.text))

            print('Write user-agent to file {} success.'.format(self._filename))
        else:
            logger.warning('No user-agent data write to file.')


    def _scrape_for_user_agent(self, url_type):
        """
        Get and return list of fetched data
        Return an empty list if request failed
        """
        # Request for web page
        try:
            req = requests.get(url_type)
            req.raise_for_status()
        except:
            logger.warning('Request for user-agent web page failed.')
            # sys.exit(1)
            return []

        # Grab information
        soup = BeautifulSoup(req.text, 'html.parser')
        selected_elem = soup.select(SELECTOR)

        return selected_elem


if __name__ == '__main__':
    test = UserAgent()

    print(test.random_computer())
    print(test.random_phone())

    test.write_computer()
    test.write_phone()
