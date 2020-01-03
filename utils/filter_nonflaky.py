import os
import csv
from collections import OrderedDict


def consolidate_results(project, project_dir, nonf_outfile, oth_outfile):
    print("Consolidating results for project {}...".format(project))
    all_results = OrderedDict()

    for i in range(num_runs):
        log_file = os.path.join(project_dir, 'run{}.log'.format(i+1))
        log = csv.reader(open(log_file, "r"), delimiter=",")
        for row in log:
            if len(row) == 3:
                classname, name, status = row
            elif len(row) == 4:
                classname, name1, name2, status = row
                name = name1 + name2
            tc = classname.strip() + "---" + name.strip()            
            status = status.strip()

            if status not in ['pass', 'fail', 'error', 'skip']:
                print(" --> status not in ['pass', 'fail', 'error', 'skip']")
                exit()
            
            if tc not in all_results:
                all_results[tc] = {}
            
            try:
                all_results[tc][status] += 1
            except KeyError:
                all_results[tc][status] = 1


    with open(nonf_outfile, "w") as nonf_out, open(oth_outfile, "w") as oth_out:
        oth_out.write("TC PASS FAIL ERROR SKIP\n")
        for tc in all_results:
            classname, name = tc.split("---")
            c_pass = all_results[tc]["pass"] if "pass" in all_results[tc] else 0
            c_fail = all_results[tc]["fail"] if "fail" in all_results[tc] else 0
            c_error = all_results[tc]["error"] if "error" in all_results[tc] else 0
            c_skip = all_results[tc]["skip"] if "skip" in all_results[tc] else 0

            if c_pass == num_runs:
                nonf_out.write("{}.{}\n".format(classname, name))
            else:
                res = "{} {} {} {}".format(c_pass, c_fail, c_error, c_skip)
                oth_out.write("{}.{} {}\n".format(classname, name, res))                



if __name__ == '__main__':
    all_projects = [p for p in os.listdir(os.path.join('deflaker', 'reruns')) 
                    if os.path.isdir(os.path.join('deflaker', 'reruns', p))
                    #and "-100" not in p]  # skipping 100 runs for now
                    and p.endswith('-100')]

    #print(all_projects)
    #exit()
    #all_projects = ['assertj-core-100']

    num_runs = 100
    
    skip_list = ['spring-boot', 'assertj-core', 'okhttp', 'hbase']  # wrong log format
    skip_list = ['ninja-100', 'ambari-100', 'Achilles-100', 'assertj-core-100']  # wrong log format
    
    for project in all_projects:
        if project in skip_list:
            continue
        project_dir = os.path.join('deflaker', 'reruns', project)
        nonf_outfile = os.path.join(project_dir, 'nonflaky_list.txt')
        oth_outfile = os.path.join(project_dir, 'results_distribution.txt')
        consolidate_results(project, project_dir, nonf_outfile, oth_outfile)