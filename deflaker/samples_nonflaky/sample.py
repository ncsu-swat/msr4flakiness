import glob
import os
import statistics
import random

if __name__ == '__main__':

    # median size of flaky test cases  -- median_sz
    # number of flaky test cases  -- num_flaky
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pathname = dir_path + "/../samples_flaky/test_cases"
    tmp = []
    for filename in glob.glob(pathname + "/*"):
        tmp.append(os.stat(filename).st_size)
    median_sz = statistics.median(tmp)
    num_flaky = len(tmp)
    print("flaky stats: {} files with median {}".format(num_flaky, median_sz))

    # associative arrays of file names and sizes for nonflaky test cases -- names_gte, names_lt
    pathname = dir_path + "/../samples_nonflaky/test_cases"
    names_gte = [] # greater than median_sz
    sizes_gte = []
    names_lt = [] # lower than median_sz
    sizes_lt = []    
    num_nonflaky = 0
    for filename in glob.glob(pathname + "/*"):
        name = filename
        sz = os.stat(filename).st_size
        if (sz < median_sz):
            names_lt.append(name)
            sizes_lt.append(sz)
        else:
            names_gte.append(name)
            sizes_gte.append(sz)
        num_nonflaky = num_nonflaky + 1

    # sampling half of tests from above the median and half of the tests below the median
    sample = []
    sample_median = []
    for x in range(num_flaky//2):
        index = random.randint(0, len(names_gte)-1)
        sample.append(names_gte[index])
        sample_median.append(sizes_gte[index])
    for x in range(num_flaky//2):
        index = random.randint(0, len(names_lt)-1)
        sample.append(names_lt[index])
        sample_median.append(sizes_lt[index])        
    print("sample of nonflaky stats: {} files with median {}".format(len(sample), statistics.median(sample_median)))
