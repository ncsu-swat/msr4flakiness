import subprocess
import csv
import os
import shutil
import tempfile
import sys
import re
from shutil import copyfile


dict = {}

def main():
    with open('historical_projects.csv') as urls_file:
        csv_reader = csv.DictReader(urls_file)
        for row in csv_reader:
            dict[row["Project Name"]] = row["Project Address"]
    
    basedir = os.getcwd()
    ## assuming the rows are ordered per project
    with open('historical_rerun_flaky_tests.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #isFirstTime = True
        dir = None
        lastdir = None
        for row in csv_reader:
            ## go back to base directory
            os.chdir(basedir)

            project = row["\ufeffProject"]
            url = dict[project]
            parts = url.split("/")
            tmp = parts[-1] # read the last element
            dir = tmp.split(".git")[0]
            if dir == None:
                raise Exception("fatal error")            
            sha = row["sha"]

            # clone the repository
            print("checking out revision: {}:{}".format(url, sha))
            myprocess = subprocess.Popen(['git', 'clone', url],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()
            tmp = stdout.decode("utf-8")
            if tmp.startswith("Cloning into '{}'...\nERROR: Repository not found.".format(dir)):
                print("......could not clone from this URL: {}".format(url))
                continue
            
            ## delete previous project
            if ((lastdir is not None) and (not lastdir == dir)):
                if (os.path.exists(lastdir)):
                    shutil.rmtree(lastdir, ignore_errors=True)
            lastdir = dir

            ## cd to project directory
            os.chdir(dir)

            #print("checking out revision {}".format(sha))
            myprocess = subprocess.Popen(['git', 'checkout', sha],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()
            tmp = stdout.decode("utf-8")
            if tmp.startswith("error: pathspec"):
                print("......checkout aborted. could not find this revision: {}".format(sha))
                continue
                
            # get test file name
            testfile = row["Test class"].split(".")[-1]
            testcase = row["Test class"] + "." + row["Test method"]
            
            # find location where the test file is
            myprocess = subprocess.Popen(['find', '.', '-name', "{}.*".format(testfile)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            stdout,stderr = myprocess.communicate()
            # download file at a given revision

            result = stdout.decode("utf-8")

            if (len(stdout)==0):
                print("......empty file {}:{}:{}".format(dir, sha, testfile))
                continue                

            ## Marcelo wrote --> Is this to handle multiple answers? are we picking the first entry? are you sure this is correct?
            if(len(re.findall('un', result)) == 1):
                path_to_testfile = result.strip(" \n")
            else:
                path_to_testfile = result.split("\n")[0] 

            ## copying test file to test_files directory
            testfile=basedir+"/test_files/"+testcase
            copyfile(path_to_testfile, testfile)

            ## copying test method to test_cases directory
            testname = row["Test method"]
            myprocess = subprocess.Popen(['java', '-jar', basedir+'/../utils/vis_method/build/libs/vis_method.jar', testfile, testname],
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT)
            mbody,stderr = myprocess.communicate()
            parseError = b'com.github.javaparser.ParseProblemException' in mbody
            # create a file with the test case
            pathto_testcase = basedir+"/test_cases/"+testcase
            if not parseError and len(mbody) > 400:
                with open(pathto_testcase, "wt+") as testfile:
                    testfile.write(mbody.decode("utf-8"))
            else:
                print("......could not find this test case. It may be defined in a superclass.")
                continue

            ## generating tokens for the test case
            myprocess = subprocess.Popen(['java', '-jar', basedir+'/../utils/vis_ids/build/libs/vis_ids.jar', pathto_testcase],
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT)
            mbody,stderr = myprocess.communicate()
            parseError = b'com.github.javaparser.ParseProblemException' in mbody
            if not parseError :
                with open(basedir+"/test_tokens/"+testcase, "wt+") as testfile:
                    testfile.write(mbody.decode("utf-8"))
            else:
                print("......problems when trying to generate tokens for test case.")
                continue

    # delete directory of last project
    os.chdir(basedir)
    if (os.path.exists(lastdir)):
        shutil.rmtree(lastdir, ignore_errors=True)                

if __name__ == "__main__":
    main()
