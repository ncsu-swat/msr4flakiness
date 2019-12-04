import glob
import os
import re

features = ["action","file","service", "time", "start", "execut", 
    "call", "wait", "close", "url", "connect", "message", "host", 
    "thread", "shutdown", "sleep", "http", "open", "join", "receive", 
    "task", "send", "concur", "sync", "finish", "expire", "flush", 
    "transaction", "event", "job", "run", "hour", "minute", "second", 
    "fetch", "read", "write", "pause", "fragile", "ignore", "fail", 
    "fork", "http"]
word_frequency = {}

if __name__ == '__main__':
    coverage_matrix = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pathname = dir_path + "/test_tokens"
    for filename in glob.glob(pathname + "/*"):
        with open(filename, 'r') as file:
            presence = set()
            data = file.read().replace('\n', '')
            for feature in features:
                if re.search(feature, data, re.IGNORECASE):
                    presence.add(feature)
                    if word_frequency.get(feature) == None:
                        word_frequency[feature] = 1
                    else:   
                        tmp = word_frequency[feature]
                        word_frequency[feature] = tmp + 1
            coverage_matrix[filename] = presence
            # print one line of the matrix
            tmp = [1 if x in presence else 0 for x in features]
            # print coverage matrix
            print(tmp)
            #print(presence)
            

    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    print(sorted_word_frequency)