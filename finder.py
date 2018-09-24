# -*- coding: utf-8 -*-
# Author: https://www.github.com/theShaswato
from multiprocessing.dummy import Pool, Manager
from sys import exit, argv
from os import system, name
import requests, socket, urllib.request, json

header = {'user-agent': 'Moofzilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

class finder(object):

    urls = []
    manager = Manager()
    found = manager.list()

    def __init__(self, sites, words, thread_count):
        self.sites = sites
        self.words = words
        self.thread_count = thread_count

    def make_list(self, found, url):
            found.append(url)

    def log(self, data):
        f = open('found.txt', 'a')
        f.write(data + "\n")
        f.close()

    def check(self, url):
        result = True
        if url.startswith('http'):
            print("\x1b[0;1mChecking if site " + url + " is online.. " + "\x1b[0m")
            try:
                urllib.request.urlopen(url, data = bytes(json.dumps(header), encoding = "utf-8"))
            except(urllib.error.HTTPError, urllib.error.URLError):
                print("\x1b[31;1mSite seems down, skipping!\x1b[0m")
                result = False
        else:
            print("\x1b[31;1mInvalid URL: " + url + " skipping!\x1b[0m")
            result = False
        return result

    def find(self, url):
        try:
            resp = requests.get(url, headers = header)
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            if resp.status_code == 403:
                self.log(url + "\t(403 Forbidden)")
                self.make_list(self.found, "\x1b[33;1m" + url + "\t(403 Forbidden)\x1b[0m")
                print("\x1b[33;1mForbidden: " + url + "\x1b[0m")
            else:
                print("Not found: " + url)
        except socket.error:
            print("Not found: " + url)
        else:
            self.log(url)
            self.make_list(self.found, url)
            print("\x1b[32;1mFound: " + url + "\x1b[0m")

    def run(self):
        if self.thread_count == 1: print("\x1b[0;1mRunning in single thread (slow)..\x1b[0m")
        for site in self.sites:
            if self.check(site) == True:
                for word in self.words:
                    url = site + "/" + word
                    self.urls.append(url)
                with Pool(self.thread_count) as finder_pool:
                    finder_pool.map(self.find, self.urls)
                    finder_pool.close()
                    finder_pool.join()

def clear():
    if name == 'nt': _ = system('cls')
    else: _ = system('clear')

def main():

    sites = words = extensions = None
    thread_count = 1
    open('found.txt', 'w').close()

    if len(argv) > 1:
        if argv[1].lower() == 'file':
            try:
                sites = open(input("Enter sitelist file path: "), 'r').read().split('\n')
            except IOError:
                exit("Sitelist not found")
        else:
            exit("Error, unknown option")
    else:
        sites = input("Enter your sites to scan: ").split(' ')

    try:
        words = open(input("Enter wordlist file path: "), 'r').read().split('\n')
    except IOError:
        exit("Wordlist not found!")

    extensions = tuple(input("Enter extensions: ").split(' '))
    thread_count = input("Enter amount of threads: ")
    if not thread_count: thread_count = 1
    else: thread_count = int(thread_count)

    if not sites or not words: exit("One of your inputs returned empty")
    if extensions:
        wtemp = words
        words = []
        for word in wtemp:
            if '.' in word:
                if word.endswith(extensions): words.append(word)
            else: words.append(word)

    finderObj = finder(sites, words, thread_count)
    finderObj.run()

    clear()
    if len(finderObj.found) > 0:
        print("\x1b[0;1mFound items:\x1b[0m\n")
        for item in finderObj.found:
            print(item)
        exit("\nDone")
    else:
        exit("Nothing found\n")

if __name__ == '__main__':
   main()