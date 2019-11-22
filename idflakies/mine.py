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
                        pass
                        #shutil.rmtree(dir, ignore_errors=True)
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
            print(' processing file {}:{}'.format(sha, testname))
            # find location where the test file is
            myprocess = subprocess.Popen(['find', '.', '-name', "{}.java".format(testfile)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()
            # download file at a given revision

            result = stdout.decode("utf-8")

            if(len(re.findall('un', result)) == 1):
                path_to_testfile = result.strip(" \n")
            else:
                path_to_testfile = result.split("\n")[0]

            myprocess = subprocess.Popen(['git', 'show', "{}:{}".format(sha, path_to_testfile)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()

            if (b"exists on disk, but not in" in stdout):
                print("git show {}:{}".format(sha,testcase))
                continue

            if (b"fatal" in stdout):
                print("could not locate file for {}:{}:{}".format(dir,testcase,sha))
                continue

            # absolute path to test file within project repo
            tmpfile = "/tmp/idflakies.tmp"
            with open(tmpfile, "w") as tmp:
                tmp.write(stdout.decode("utf-8"))

            # extract actual test from files
            myprocess = subprocess.Popen(['java', '-jar', basedir+'/vis_method/build/libs/vis_method.jar', tmpfile, testname],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
            mbody,stderr = myprocess.communicate()
            # create a file with the test case
            with open(basedir+"/tests/"+testcase, "wt+") as testfile:
                testfile.write(mbody.decode("utf-8"))


if __name__ == "__main__":
    main()
