import glob, sys

def save_to_file(name_file, data):
    with open(name_file, 'w') as to_save:
        to_save.write('{}'.format(data))

for filename in glob.glob('*.log'):
    with open(filename) as f:
        lines = f.readlines()
        results = []
        for line in lines:

            if line.startswith("Executing test "):
                columns = line.split(" ")
                test_name = columns[2]
                test_class = columns[3].replace("]","").replace("[","")
                status = columns[6].replace("\n","")

                if status == "SUCCESS":
                    status = "pass"
                elif status == "SKIPPED":
                    status = "skip"
                else:
                    status = "error"

                formatted = test_class +", " + test_name + ", " + status + "\n"
                
                if "[" not in formatted:
                    results.append(formatted)
                
        print (len(results))
        new_file = filename + ".new"
        save_to_file(new_file, "".join(results))
        
