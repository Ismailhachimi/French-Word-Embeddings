""""
This script contains a Spider class with a main code that is using the class functions to get
urls and scrape text files.
"""

import requests
import argparse
import time
import os
import zipfile
import shutil
import urllib
from bs4 import BeautifulSoup


class SubtitlesSpider:
    """
    SubtitlesSpider is a spider that contains actions needed to apply on a list of series urls.
    Using this class can help improve code and use the urls for future operations in a scraping process.
    """
    list_series = []
    urls = []

    def __init__(self, listseries):
        """
        Subtitles constructor : This saves a list of series and the url source
        :param listseries:
        """
        self.list_series = listseries
        self.url_source = 'https://www.sous-titres.eu'

    def get_urls(self):
        """
        This function helps us get the series urls for future scraping process
        :return:
        """
        urls = []
        hrefs = []

        for serie in self.list_series:
            tmp = self.url_source + '/series/' + serie + ".html"
            urls.append(tmp.replace(" ", "_"))

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            a_tags = soup.findAll('a', {"class": "subList"})

            for a in a_tags:
                hrefs.append(self.url_source + '/series/' + a.get('href'))

        self.urls = hrefs

    def extract_files(self):
        """
        This function helps extract zipfiles from self.urls, get one text file for each zipfie and delete
        the whole zipfiles at the end.
        :return:
        """
        current_dir = os.getcwd() + '/zipfiles/'
        strfiles = os.getcwd() + '/strfiles/'

        if not os.path.exists(current_dir):
            os.mkdir(current_dir)
        if not os.path.exists(strfiles):
            os.mkdir(strfiles)

        time.sleep(1)
        for zip_file_url in self.urls:

            tmp_string = ''

            # may replace DVD with S | S with DVD
            if 'S' not in zip_file_url and 'EN' not in zip_file_url:

                file_name = zip_file_url.split('/')[-1]
                file_path = current_dir+file_name

                print("Zipfile name : "+file_name)

                urllib.request.urlretrieve(zip_file_url, file_path)

                with zipfile.ZipFile(file_path) as zf:
                    zf.extractall(path=strfiles + 'tmp/')

                tmp_files = [element for element in os.listdir(strfiles + 'tmp/')
                             if '__' not in element and element != 'Readme.md']

                if len(tmp_files) < 20:
                    if not os.path.isfile(strfiles + 'tmp/' + tmp_files[0]):
                        if os.path.exists(strfiles + 'tmp/' + 'VF/'):
                            tmp_files = os.listdir(strfiles + 'tmp/VF/')
                            tmp_string = 'VF/'
                        else:
                            for file in tmp_files:
                                shutil.rmtree(strfiles + 'tmp/' + file)
                            continue

                    saved_file = [file for file in tmp_files if 'srt' in file and 'VO' not in file][0]
                    print("\tSaved file : " + saved_file + "\n")
                    shutil.copy(strfiles + 'tmp/' + tmp_string + saved_file, strfiles, follow_symlinks=False)

                    if not tmp_string:
                        for file in tmp_files:
                            os.remove(strfiles + 'tmp/' + file)
                    else:
                        tmp_dirs = os.listdir(strfiles + 'tmp/')
                        for tmp_dir in tmp_dirs:
                            shutil.rmtree(strfiles + 'tmp/' + tmp_dir)
                else:
                    if os.path.isfile(strfiles + 'tmp/' + tmp_files[0]):
                        for file in tmp_files:
                            os.remove(strfiles + 'tmp/' + file)
                    else:
                        for file in tmp_files:
                            shutil.rmtree(strfiles + 'tmp/' + file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--serie",
                        help="The serie we want to scrape. A list of series is available by default.",
                        type=str)

    inputs = parser.parse_args()

    list_series = ['greys anatomy']

    input_series = list_series if inputs.serie is None else [inputs.serie]

    start_time = time.time()

    spider = SubtitlesSpider(input_series)
    spider.get_urls()
    spider.extract_files()

    finish_time = time.time()

    if finish_time - start_time < 2:
        print("The serie doesn't exist or it's not available on the website.")
    elif inputs.serie is None:
        print("The default series' files have been loaded.")
    else:
        files = [file for file in os.listdir('zipfiles') if file != 'Readme.md']
        for file in files:
            os.remove('zipfile/' + file)
        print("The new serie's files have been loaded.")


