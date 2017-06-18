# -*- coding: utf-8 -*-


import requests
from html.parser import HTMLParser
import sys


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = False
        self.link = False
        self.data = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h2" and "class" in attrs and attrs['class'] == "esc-lead-article-title":
            self.data.append({})
            self.title = True
            self.link = True

        if tag == "a" and self.link == True:
            self.data[-1].update({"link": attrs["href"]})

    def handle_data(self, data):
        if self.title == True or self.link == True:
            self.data[-1].update({"title": data})
            self.title = False
            self.link = False


def main(args=sys.argv[0]):
    payload = {'topic': 't'}
    r = requests.get('https://news.google.com/news/section', params=payload)
    parser = Parser()
    parser.feed(r.text)
    parser.close()
    print(parser.data)


if __name__ == '__main__':
    main()
