import glob
import os
from nltk import sent_tokenize, word_tokenize, PorterStemmer, download
from nltk.corpus import stopwords
import collections
from operator import itemgetter 
from wordsegment import load, segment
import sys

# tokenization, lemmatization, stop word removal
download('punkt')
download('stopwords')
stop_words = set(stopwords.words('english'))
other_stop_words = [",","?","-","_",";","\"","—","\\n","==","0","1","2","3","4","-c","*","=","/","@","$",";",":","(",")","<",">","{","}",".","''","'","``", "get", "set"]
stop_words = stop_words.union(set(other_stop_words))
# word segmentation
load()

## stemming and stop word removal
def read_words(text):
    ## tokenize
    tokens = word_tokenize(text)
    
    ## segmentation
    words = [word for token in tokens for word in segment(token)]

    # stemming
    stemmer = PorterStemmer()
    stems = set()
    for w in words:
        stems.add(stemmer.stem(w))

    ## remove stop words
    filtered_stems = [w for w in stems if not w in stop_words]
    return set(filtered_stems)

## computing word frequency
def compute_frequency(test_words):
    word_frequency = {}
    for testname in test_words: 
        words = test_words[testname]
        for word in words:
            val = word_frequency.get(word)
            if val is None:
                word_frequency[word] = 1
            else:
                word_frequency[word] = val + 1
    return word_frequency

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pathname = dir_path + "/test_tokens"

    ## progress
    numfiles = len(os.listdir(pathname))
    toolbar_width = 100
    print("processing {} files".format(numfiles))
    
    ## create dictionary storing list of words for each test
    test_words = {}
    num_processed_files = 0
    for filename in glob.glob(pathname + "/*"):
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')
            #print (filename)
            test_words[filename] = read_words(data)
            # update the bar
            num_processed_files = num_processed_files + 1
            print(f'\r{100*(num_processed_files/numfiles):.2f}' + "% processed", end='')

    word_frequency = compute_frequency(test_words)
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

    with open("output.log", 'r') as file:
        for elem in sorted_word_frequency:
            file.write(elem)      