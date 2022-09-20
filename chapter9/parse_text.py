from bs4 import BeautifulSoup
from collections import Counter
from urllib.request import urlopen
import re
import string


def cleanSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation + string.whitespace)
                for word in sentence]
    sentence = [word for word in sentence if len(word) > 1
                or (word.lower() == 'a') or word.lower() == 'i']
    return sentence


def cleanInput(content):
    content = content.upper()
    content = re.sub('\n|[[\d+\]]', ' ', content)
    content = bytes(content, 'UTF-8')
    content = content.decode('ascii', 'ignore')
    sentences = content.split('. ')
    return [cleanSentence(sentence) for sentence in sentences]


def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output


def getNgrams(content, n):
    content = cleanInput(content)
    ngrams = Counter()
    ngram_list = []
    for sentence in content:
        newNgrams = [' '.join(ngram) for ngram in 
                     getNgramsFromSentence(sentence, n)]
        ngram_list.extend(newNgrams)
        ngrams.update(newNgrams)
    return (ngrams)


def isCommon(ngram):
    commonWords = ['THE', 'BE', 'AND', 'OF', 'A', 'IN', 'TO', 'HAVE', 'IT', 'I',
                   'THAT', 'FOR', 'YOU', 'HE', 'WITH', 'ON', 'DO', 'SAY', 'THIS',
                   'THEY', 'IS', 'AN', 'AT', 'BUT', 'WE', 'HIS', 'FROM', 'THAT',
                   'NOT', 'BY', 'SHE', 'OR', 'AS', 'WHAT', 'GO', 'THEIR', 'CAN',
                   'WHO', 'GET', 'IF', 'WOULD', 'HER', 'ALL', 'MY', 'MAKE', 'ABOUT',
   ]
    for word in ngram:
        if word in commonWords:
            return True
    return False


content = str(
        urlopen('https://en.wikipedia.org/wiki/Python_(programming_language)')
        .read(), 'utf-8')
ngrams = getNgrams(content, 2)
print(ngrams)
