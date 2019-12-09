import sys
from bs4 import BeautifulSoup as Soup

def parseLog(file):
    with open(file) as f:
        handler = f.read()
        soup = Soup(handler,"html.parser")
        for testcase in soup.findAll('testcase'):
            failed = False
            # check for failure
            if testcase.contents != []:
                p = testcase.contents[0]
                while p != None:
                    if (p.name == "failure"):
                        failed = True  
                        break              
                    p = p.next
            print ("{}, {}, {}".format(testcase["classname"],testcase["name"],"fail" if failed else "pass"))

if __name__ == "__main__":
    parseLog(sys.argv[1])
