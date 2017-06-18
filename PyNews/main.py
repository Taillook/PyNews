# -*- coding: utf-8 -*-


import requests
from html.parser import HTMLParser
import sys

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = False
        self.link = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h2" and "class" in attrs and attrs['class'] == "esc-lead-article-title":
            #print("開始タグ :", tag, attrs)
            self.title = True
            self.link = True
        if tag == "a" and self.link == True:
            #print("開始タグ :", tag, attrs)
            print("Link : ", attrs["href"])
    #def handle_endtag(self, tag):
        #print("終了タグ :", tag)
    def handle_data(self, data):
        if self.title == True or self.link == True:
            print("データ:", data)
            self.title = False
            self.link = False

def main(args=sys.argv[0]):
    payload = {'topic' : 't'}
    r = requests.get('https://news.google.com/news/section', params=payload)
    parser = Parser()
    parser.feed(r.text)
    parser.close()
if __name__ == '__main__':
    main()
