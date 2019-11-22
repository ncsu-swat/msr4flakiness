import subprocess
import glob
import os

def main():
    # extract actual test from files
    basedir = os.getcwd()
    filenames = [f for f in glob.glob(basedir + "/test_files/*", recursive=False)]
    for filename in filenames:
        print(os.path.basename(filename))
        parts = filename.split(".")
        testname = parts[len(parts)-1]
        myprocess = subprocess.Popen(['java', '-jar', basedir+'/vis_method/build/libs/vis_method.jar', filename, testname],
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)
        mbody,stderr = myprocess.communicate()
        if (not stderr is None):
            print("fatal error")
            continue
        # create a file with the test case
        with open(basedir+"/test_cases/"+os.path.basename(filename), "wt+") as testfile:
            testfile.write(mbody.decode("utf-8"))

if __name__ == "__main__":
    main()

        

