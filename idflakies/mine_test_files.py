import subprocess
import csv
import os
import shutil
import tempfile
import sys
import re

def main():
    basedir = os.getcwd()
    urls = set()
    ## assuming the rows are ordered per project
    with open('list-flaky.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #isFirstTime = True
        dir = None
        for row in csv_reader:
            #if isFirstTime:
            #    isFirstTime = False
            #    continue
            # skip if category of the test is OD
            if (row["Category"] == "OD"):
                continue
            url = row["URL"]
            # clone the repository if this is the first time it is seen
            if (not url in urls):
                # cleanup state related with previous project
                if (not dir is None):
                    os.chdir("..")
                    if (os.path.exists(dir)):
                        shutil.rmtree(dir, ignore_errors=True)
                # get the name of the project
                parts = url.split("/")
                dir=parts[len(parts)-1]
                if dir == None:
                    raise Exception("fatal error")
                # delete corresponding directory if, for some reason, a dir with this name exists
                if (os.path.exists(dir)):
                    #shutil.rmtree(dir, ignore_errors=True)
                    pass
                # clone the repository
                if (not os.path.exists(dir)):
                    print("cloning project " + url)
                    myprocess = subprocess.Popen(['git', 'clone', url],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
                    stdout,stderr = myprocess.communicate()
                    # change directory to this project
                os.chdir(dir)
                # add url to the list of urls
                urls.add(url)
            # process each test on that directory
            sha = row["SHA"]
            # get test file name
            testcase = row["Test Name"]
            testcase = testcase.split()[0]
            parts = testcase.split(".")
            testname = parts[len(parts)-1]
            testfile = parts[len(parts)-2]
            # find location where the test file is
            myprocess = subprocess.Popen(['find', '.', '-name', "{}.java".format(testfile)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()
            # download file at a given revision

            result = stdout.decode("utf-8")

            ## Marcelo wrote --> Is this to handle multiple answers? are we picking the first entry? are you sure this is correct?
            if(len(re.findall('un', result)) == 1):
                path_to_testfile = result.strip(" \n")
            else:
                path_to_testfile = result.split("\n")[0] 

            myprocess = subprocess.Popen(['git', 'show', "{}:{}".format(sha, path_to_testfile)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()

            # Marcelo wrote --> I guess it is OK in this case to retrieve the file anyways. It should not matter as we are looking at the identifiers...
            if (b"exists on disk, but not in" in stdout):
                print("  exists on disk, but not in...{}:{}".format(sha,testcase))
                continue

            # Marcelo wrote --> From what I observed, the are only two cases of this error. So, it is not as critical.
            if (b"fatal" in stdout):
                print("  fatal error in git show...{}:{}:{}".format(dir, sha, path_to_testfile))
                continue

            if (len(stdout)==0):
                print("  empty file {}:{}:{}".format(dir, sha, path_to_testfile))
                continue                

            #print("  processing file {}:{}:{}".format(dir, sha, path_to_testfile))            
            testfile=basedir+"/test_files/"+testcase
            with open(testfile, "w") as tmp:
                tmp.write(stdout.decode("utf-8"))

        # after processing the last line, delete the dir of last repo
        print(">>>"+dir)
        print(os.path.exists(dir))
        if (os.path.exists(dir)):
            print("oh boy")
            shutil.rmtree(dir, ignore_errors=True)

if __name__ == "__main__":
    main()

