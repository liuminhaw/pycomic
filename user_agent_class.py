"""
Program:
    User-agent data for use in web scraping
Author:
    haw
"""

import sys, shelve, random
import requests
import logging_class
from bs4 import BeautifulSoup
from datetime import datetime


URL = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/'
SELECTOR = 'td.useragent a'
logger = logging_class.PersonalLog('user_agent_class')



class UserAgent():

    def __init__(self):
        # Default user agent value
        self.filename = 'user_agents-' + datetime.now().strftime('%Y%m%d')


    def load_random(self):
        """
        Randomly return an user-agent value
        """
        selected_list = self._scrape_for_user_agent()

        user_agent = random.choice(selected_list)
        logger.debug('User-Agent: {}'.format(user_agent.text))

        return user_agent.text


    def write_file(self):
        """
        Save user-agent data to file
        """
        selected_list = self._scrape_for_user_agent()

        with open(self.filename, 'w') as write_file:
            for elem in selected_list:
                write_file.write('{}\n'.format(elem.text))

        print('Write user-agent to file {} success.'.format(self.filename))


    def _scrape_for_user_agent(self):
        """
        Get and return list of fetched data
        """
        # Request for web page
        try:
            req = requests.get(URL)
            req.raise_for_status()
        except:
            logger.warning('Request for user-agent web page failed.')
            sys.exit(1)

        # Grab information
        soup = BeautifulSoup(req.text, 'html.parser')
        selected_elem = soup.select(SELECTOR)

        return selected_elem


if __name__ == '__main__':
    test = UserAgent()
    test.load_random()
    test.write_file()
