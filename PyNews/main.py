# -*- coding: utf-8 -*-


import requests
from html.parser import HTMLParser
import sys
import argparse


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
    topic_list = ["h", "w", "b", "n", "t", "el", "p", "e", "s", "m"]

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--topic", type=str, default="t")
    parser.add_argument("--amount", type=str, default="20")
    args = parser.parse_args()

    args.amount = int(args.amount)

    if args.amount > 20:
        args.amount = 20
    if args.topic not in topic_list:
        args.topic = "h"

    payload = {'topic': args.topic}
    r = requests.get('https://news.google.com/news/section', params=payload)
    parser = Parser()
    parser.feed(r.text)
    parser.close()

    parser.data = parser.data[0:args.amount]

    for i in parser.data:
        print("Title: " + i["title"], "\nLink: " + i["link"] + "\n")


if __name__ == '__main__':
    main()
