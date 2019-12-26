import os
import csv
from collections import OrderedDict


def consolidate_results(project, project_dir, nonf_outfile, oth_outfile):
    print("Consolidating results for project {}...".format(project))
    all_results = OrderedDict()

    for i in range(10):
        log_file = os.path.join(project_dir, 'run{}.log'.format(i+1))
        log = csv.reader(open(log_file, "r"), delimiter=",")
        for row in log:
            if len(row) == 3:
                classname, name, status = row
            elif len(row) == 4:
                classname, name1, name2, status = row
                name = name1 + name2
            tc = classname.strip() + "---" + name.strip()
            try:
                all_results[tc].append(status.strip())
            except KeyError:
                all_results[tc] = [status.strip()]

    with open(nonf_outfile, "w") as nonf_out, open(oth_outfile, "w") as oth_out:
        for tc in all_results:
            classname, name = tc.split("---")
            if all_results[tc].count("pass") == 10:                
                nonf_out.write("{}.{}\n".format(classname, name))
            else:
                oth_out.write("{}.{}\n".format(classname, name))



if __name__ == '__main__':
    all_projects = [p for p in os.listdir(os.path.join('deflaker', 'reruns')) 
                    if os.path.isdir(os.path.join('deflaker', 'reruns', p))
                    and "-100" not in p]  # skipping 100 runs for now
    
    for project in all_projects:
        if project in ['spring-boot', 'assertj-core', 'okhttp', 'hbase']:  # wrong log format
            continue
        project_dir = os.path.join('deflaker', 'reruns', project)
        nonf_outfile = os.path.join(project_dir, 'nonflaky_list.txt')
        oth_outfile = os.path.join(project_dir, 'other_results.txt')
        consolidate_results(project, project_dir, nonf_outfile, oth_outfile)