# -*- coding: utf-8 -*-

import re
import requests
import time
import os

from bs4 import BeautifulSoup

base_url = "http://www.world-art.ru"
base_url_author = "http://www.world-art.ru/people.php"
file_prefix = "wa_pushkin"
regexp = re.compile("^lyric\/lyric\.php\?id=([\d]+)")

payload = {'id': '1092'}

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/64.0.3282.167 Safari/537.36"
}


def validate_url(url):
    return regexp.match(url)


if __name__ == "__main__":
    request = requests.get(base_url_author, params=payload, headers=headers)
    soup = BeautifulSoup(request.text, 'html.parser')

    links = soup.find_all('a', href=True)
    links = list(map(lambda tag: tag['href'], filter(lambda tag: validate_url(tag['href']), links)))
    links = list(map(lambda href: base_url + "/" + href, links))

    counter = 0
    existing = os.listdir('.')
    print("%d files will be created" % len(set(links)))
    for link in sorted(set(links)):
        filename = file_prefix + '_%d.txt' % counter

        if filename not in existing:
            print("Getting info from ref: %s" % link)
            request = requests.get(link, headers=headers)
            soup = BeautifulSoup(request.text, 'html.parser')
            content = max(list(map(lambda tag: tag.text, soup.find_all('pre'))), key=len)

            print("Writing " + filename)
            with open(filename, 'w') as f:
                f.writelines(content)
            time.sleep(5)
        else:
            print(filename + " already exist, skipping")
        counter += 1
