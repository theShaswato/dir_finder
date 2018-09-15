# -*- coding: utf-8 -*-
# Author: https://www.github.com/theShaswato
from multiprocessing.dummy import Pool
from os import system, name
import requests, socket

site = sites = words = None
found = []
header = {'user-agent': 'Moofzilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

try:
    sites = open(input("Enter sitelist path: "), 'r').read().split('\n')
    words = open(input("Enter wordlist path: "), 'r').read().split('\n')
except IOError: exit("One of your file was not found")
if not words or not sites: exit("One of your file is empty")

filters = tuple(input("Enter extensions: ").split(' '))
if filters:
   w = words
   words = []
   for n in w:
       if '.' in n:
           if n.endswith(filters): words.append(n)
       else: words.append(n)

def clear():
    if name == 'nt': _ = system("cls")
    else: _ = system("clear")

def log(url):
    f = open('found.txt', 'a')
    f.write(url + '\n')
    f.close()

def check(directory):
    global found
    url = site + "/" + directory
    try:
        resp = requests.get(url, headers = header)
        resp.raise_for_status()
    except requests.exceptions.MissingSchema:
        print("\x1b[31;1mInvalid url: " + url + "\x1b[0m")
    except requests.exceptions.HTTPError:
        if resp.status_code == 403:
            found.append("\x1b[33;1m" + url + "\t[403:forbidden]\x1b[0m")
            print("\x1b[33;1mFound: " + url + "\t[403:forbidden]\x1b[0m")
            log(url + "\t[403:forbidden]")
        else:
            print("Not Found: " + url)
    except socket.error:
        print("Not Found: " + url)
    else:
        found.append(url)
        log(url)
        print("\x1b[32;1mFound: " + url +"\x1b[0m")

def start(threads):
    open('found.txt', 'w').close()
    if not threads or int(threads) == 1:
        threads = 1
        print("Running in single thread mod (slow)\nuse 100 or more for good performance")
    else: threads = int(threads)
    for n in sites:
        global site
        site = n
        with Pool(threads) as pool:
            pool.map(check, words)
            pool.close()
            pool.join()
                
    clear()
    print("Found items:\n")
    for n in found: print(n)
    exit("\ndone, result saved in found.txt")

start(input("Enter thread amount: "))