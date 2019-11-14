import glob
import os
from nltk import sent_tokenize, word_tokenize, PorterStemmer, download
from nltk.corpus import stopwords    

# tokenization, lemmatization, stop word removal
download('punkt')
stop_words = set(stopwords.words('english'))
other_stop_words = [",","?","-","_",";","\"","—","\\n","==","1","-c","got","run","func","end","404","-d","break","}","[","]","error","get","rm","sh","''",">","<",">=","<=","//","c","``","&","OK",")","(","'","=","0","main","function","output","then",":","!"]
stop_words = stop_words.union(set(other_stop_words))

def basic_words(text):
    ## tokenize
    words = word_tokenize(text)
    #print(words)
    #print(len(words))
    
    ## stemm
    stemmer = PorterStemmer()
    stems = set()
    for w in words: 
        stems.add(stemmer.stem(w))
    #print(stems)
    #print(len(stems))

    ## remove stop words
    filtered_stems = [w for w in stems if not w in stop_words]
    #print(filtered_stems)
    #print(len(filtered_stems))

    return filtered_stems

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    txtfiles = []
    for filename in glob.glob(dir_path + "/data/*.txt"):
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')
            #print(data)
            print (filename)
            print(basic_words(data))
