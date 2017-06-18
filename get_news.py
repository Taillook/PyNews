# -*- coding: utf-8 -*-

import requests
import argparse
from py_news.news import News_parser


def main():
    arg_parser = argparse.ArgumentParser(description="")
    arg_parser.add_argument("--topic", type=str, default="t")
    arg_parser.add_argument("--amount", type=str, default="20")
    args = arg_parser.parse_args()

    args.amount = int(args.amount)

    if args.amount > 20:
        args.amount = 20

    payload = {"topic": args.topic}
    r = requests.get('https://news.google.com/news/section', params=payload)
    parser = News_parser()
    parser.feed(r.text)
    parser.close()

    parser.data = parser.data[0:args.amount]

    for i in parser.data:
        print("Title: " + i["title"], "\nLink: " + i["link"] + "\n")


if __name__ == '__main__':
    main()
