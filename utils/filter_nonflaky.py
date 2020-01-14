import os
import csv
from collections import OrderedDict


def consolidate_results(project):
    project_dir = os.path.join('deflaker', 'reruns', project)
    nonf_outfile = os.path.join(project_dir, 'nonflaky_list.txt')
    oth_outfile = os.path.join(project_dir, 'results_distribution.txt')
    prob_outfile = os.path.join(project_dir, 'prob.csv')    
        
    all_results = OrderedDict()

    print("Consolidating results for project {}...".format(project))
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


    with open(nonf_outfile, "w") as nonf_out, open(oth_outfile, "w") as oth_out, \
        open(prob_outfile, "w") as prob_out, open(prob_all_outfile, "a") as proball_out:
        oth_out.write("TC PASS FAIL ERROR SKIP\n")
        prob_out.write("TC,PASS,FAIL,ERROR,SKIP\n")        
        for tc in all_results:
            classname, name = tc.split("---")
            c_pass = all_results[tc]["pass"] if "pass" in all_results[tc] else 0
            c_fail = all_results[tc]["fail"] if "fail" in all_results[tc] else 0
            c_error = all_results[tc]["error"] if "error" in all_results[tc] else 0
            c_skip = all_results[tc]["skip"] if "skip" in all_results[tc] else 0
            c_total = c_pass + c_fail + c_error + c_skip

            #if c_pass == num_runs:
            if c_pass/c_total == 1 or c_fail/c_total == 1 or c_error/c_total == 1 or c_skip/c_total == 1:
                nonf_out.write("{}.{}\n".format(classname, name))
            else:
                res = "{} {} {} {}".format(c_pass, c_fail, c_error, c_skip)
                oth_out.write("{}.{} {}\n".format(classname, name, res))
                # --- Prob
                res_prob = "{},{},{},{}".format(c_pass/c_total, c_fail/c_total, c_error/c_total, c_skip/c_total)
                prob_out.write("{}.{},{}\n".format(classname, name, res_prob))
                # --- Prob_all
                proball_out.write("{},{}.{},{}\n".format(project, classname, name, res_prob))



if __name__ == '__main__':
    all_projects = sorted([p for p in os.listdir(os.path.join('deflaker', 'reruns')) 
                    if os.path.isdir(os.path.join('deflaker', 'reruns', p))
                    and p.endswith('-100')])
    #print(all_projects)
    #exit()
    #all_projects = ['hadoop-100', 'alluxio-100']

    num_runs = 100
        
    skip_list = []
    skip_list = ['hadoop-100', 'alluxio-100']  # wrong log format

    prob_all_outfile = os.path.join('deflaker', 'reruns', 'prob_all.csv')
    if os.path.exists(prob_all_outfile):
        os.remove(prob_all_outfile)
        with open(prob_all_outfile, "w") as proball_out:
            proball_out.write("PROJECT,TC,PASS,FAIL,ERROR,SKIP\n")
    
    for project in all_projects:
        if project not in skip_list:
            consolidate_results(project)
