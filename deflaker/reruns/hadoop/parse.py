import sys
from bs4 import BeautifulSoup as Soup

def parseLog(file):
    with open(file) as f:
        handler = f.read()
        soup = Soup(handler,"html.parser")
        for testcase in soup.findAll('testcase'):
            status = "pass"
            # check for failure
            if testcase.contents != []:
                p = testcase.contents[0]
                while p != None:
                    if (p.name == "failure"):
                        status = "fail"
                        break
                    elif (p.name == "skipped"):
                        status = "skip"
                        break
                    elif (p.name == "error"):
                        status = "error"
                        break
                    p = p.next
            print ("{}, {}, {}".format(testcase["classname"],testcase["name"],status))

if __name__ == "__main__":
    parseLog(sys.argv[1])
