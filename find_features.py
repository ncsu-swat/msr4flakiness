import glob
import os
from nltk import sent_tokenize, word_tokenize, PorterStemmer, download
from nltk.corpus import stopwords
import collections
from operator import itemgetter 

# tokenization, lemmatization, stop word removal
download('punkt')
download('stopwords')
stop_words = set(stopwords.words('english'))
other_stop_words = [",","?","-","_",";","\"","—","\\n","==","1","-c","got","run","func","end","404","-d","break","}","[","]","error","get","rm","sh","''",">","<",">=","<=","//","c","``","&","OK",")","(","'","=","0","main","function","output","then",":","!","{", "}", "%","r","def", ".", "#", "self", "test", "We", "'get", "fields", "field", "n't", "'/", "", "b","true","return","i++","*","see","second"]
stop_words = stop_words.union(set(other_stop_words))

def read_words(text):
    ## tokenize
    words = word_tokenize(text)
    for a in [w for w in words if "=" in w]:
        words.remove(a)
        words.extend(a.split("="))
    ## stemm
    stemmer = PorterStemmer()
    stems = set()
    for w in words:
        stems.add(stemmer.stem(w))
    ## remove stop words
    filtered_stems = [w for w in stems if not w in stop_words]
    return filtered_stems

def compute_frequency(test_words):
    # calculate frequency of words
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
    txtfiles = []
    ## create dictionary storing list of words for each test
    test_words = {}
    for filename in glob.glob(dir_path + "/data/*.txt"):
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')
            print (filename)
            test_words[filename] = read_words(data)
    
    word_frequency = compute_frequency(test_words)
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    #print(sorted_word_frequency)
    for elem in sorted_word_frequency[:30]:
        print(elem)        
