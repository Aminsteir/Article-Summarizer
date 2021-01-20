# Code credited to Pushkara Sharma and his medium.com article on text summarization

import urllib.request as url
import bs4
import regex as re
import heapq

from nltk import sent_tokenize
from nltk import word_tokenize


def main():
    is_art = input('Is url? (y/n) ')

    if is_art.lower() == 'y':
        article_url = input('Url of article: ')

        html = url.urlopen(article_url)
        page = bs4.BeautifulSoup(html, features='lxml')

        # Find all paragraphs
        paragraphs = page.find_all('p')
        text = reformat(paragraphs)
    else:
        paragraphs = input('Text: \n')
        text = reformat(paragraphs, False)

    n_sent = int(input('Number of sentences in summary: '))
    summary = process(text, n_sent)

    print(summary)


def reformat(paragraphs, is_arr=True):
    text = paragraphs
    if is_arr:
        text = ''.join([i.text for i in paragraphs])
    text = text.replace(r'^\s+|\s+?$', '')
    text = text.replace('\n', ' ')
    text = text.replace('\\', '')
    text = text.replace(',', '')
    text = text.replace('"', '')
    return re.sub(r'\[[0-9]*\]', '', text)


def process(text, out_sent=4):
    freq = {}
    word_arr = word_tokenize(text.lower())
    for word in word_arr:
        if word in freq.keys():
            continue
        freq[word] = word_arr.count(word)

    max_freq = max(freq.values())
    for word in freq.keys():
        freq[word] = (freq[word] / max_freq)

    sentence_score = {}
    sentences = sent_tokenize(text)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq.keys():
                if sentence not in sentence_score.keys():
                    sentence_score[sentence] = freq[word]
                    continue
                sentence_score[sentence] += freq[word]

    summary = heapq.nlargest(out_sent, sentence_score, key=sentence_score.get)
    return ' '.join(summary)


if __name__ == '__main__':
    main()
