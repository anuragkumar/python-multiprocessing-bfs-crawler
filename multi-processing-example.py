from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re
import requests
import datetime
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from string import punctuation
from collections import defaultdict
import numpy as np
import math
import operator
from lxml.html.clean import Cleaner
import multiprocessing


def rem_classes(soup, tag, class_name):
    element_list = soup.findAll(tag, {'class': class_name})
    if len(element_list) > 0:
        for element in element_list:
            element.decompose()


def get_cleaner():
    cleaner = Cleaner()
    cleaner.embedded = True
    cleaner.frames = True
    cleaner.style = True
    cleaner.remove_unknown_tags = True
    cleaner.processing_instructions = True
    cleaner.annoying_tags = True
    cleaner.remove_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'a', 'u', 'i', 'body', 'div', 'span', 'p']
    cleaner.kill_tags = ['table', 'img', 'semantics', 'script', 'noscript', 'style', 'meta', 'label', 'li', 'ul',
                         'ol', 'sup', 'math', 'nav', 'dl', 'dd', 'sub']
    return cleaner


def parseURL(URL, caseFolding=True, punctuationHandling=True):
    html = urlopen(URL)
    soup = BeautifulSoup(html, 'html.parser')

    tag_class_data = [
        {'tag': 'a', 'class': 'mw-jump-link'},
        {'tag': 'table', 'class': 'wikitable'},
        {'tag': 'div', 'class': 'printfooter'},
        {'tag': 'span', 'class': 'mw-redirectedfrom'},
        {'tag': 'div', 'class': 'noprint'},
        {'tag': 'span', 'class': 'mw-headline'},
        {'tag': 'span', 'class': 'mw-editsection'}]

    for entry in tag_class_data:
        rem_classes(soup, entry["tag"], entry["class"])

    cleaner = get_cleaner()
    soup = cleaner.clean_html(str(soup.find('title')) + " " + str(soup.find('div', {'id': 'bodyContent'})))

    finaltext = BeautifulSoup(soup, 'lxml').get_text()
    finaltext = finaltext.replace(u'\xa0', u' ')
    finaltext = finaltext.replace("\n", " ").replace("\t", " ")
    finaltext = re.sub(' +', ' ', finaltext)

    if caseFolding:
        finaltext = finaltext.casefold()

    if punctuationHandling:
        finaltext = ''.join(c for c in finaltext if (c not in punctuation and c != '-'))

    return finaltext


def getTrigrams(text):
    token = nltk.word_tokenize(text)

    trigrams = set([' '.join(grams) for grams in nltk.trigrams(token)])

    return trigrams

def my_func(corpustext, myList, myDict, process_name):
    print(process_name + ": started")
    i = 1
    now = time.time()
    for val in myList:
        myDict[val] = corpustext.count(val)
        if(i == 10000):
            then = time.time()
            print(process_name + ": 10000 done")
            print(str(int(then-now)))
        if(i == 100000):
            then = time.time()
            print(process_name + ": 100000 done")
            print(str(int(then-now)))
        if(i == 600000):
            then = time.time()
            print(process_name + ": 1000000 done")
            print(str(int(then-now)))

        i += 1

def main():
    with open("./BFS.txt") as f:
        lines = f.readlines()

    trigrams = set()
    corpustext = ""
    i = 1
    for line in lines:
        finaltext = parseURL(line.strip())
        trigrams = trigrams.union(getTrigrams(finaltext))
        corpustext = corpustext + "<> "+finaltext
        print(i)
        i = i + 1
        if(i == 1001):
            break

    x = list(trigrams)
    print(len(x))
    list1 = x[0:600000]
    list2 = x[600001:1200000]
    list3 = x[1200001:1800000]
    list4 = x[1800001:]
    trigram_freq1 = dict.fromkeys(list1,0)
    trigram_freq2 = dict.fromkeys(list2,0)
    trigram_freq3 = dict.fromkeys(list3,0)
    trigram_freq4 = dict.fromkeys(list4,0)
    processes=[]
    list1_process = multiprocessing.Process(target=my_func, args=(corpustext, list1, trigram_freq1, "process1"))

    list2_process = multiprocessing.Process(target=my_func, args=(corpustext, list2, trigram_freq2, "process2"))

    list3_process = multiprocessing.Process(target=my_func, args=(corpustext, list3, trigram_freq3, "process3"))

    list4_process = multiprocessing.Process(target=my_func, args=(corpustext, list4, trigram_freq4, "process4"))

    processes.append(list1_process)
    processes.append(list2_process)
    processes.append(list3_process)
    processes.append(list4_process)

    for t in processes:
        t.start()

    for t in processes:
        t.join()

if __name__ == "__main__":
    main()
