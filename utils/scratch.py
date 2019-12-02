import javalang
import os
import glob

def main():
    basedir = os.getcwd()
    filenames = [f for f in glob.glob(basedir + "/test_files/*", recursive=False)]
    onefile = filenames[1]
    print(onefile)
    with open(onefile, 'r') as file:
        data = file.read().replace('\n', '')
        tree = javalang.parse.parse(data)
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            if node.name == "anyMissingClassesWithMixtureOfClassesPerformsAdd": ## found
                print("---")
                for x, y in javalang.ast.walk_tree(node):
                    if isinstance(y, javalang.tree.MethodDeclaration):
                        print(y.name)
                    elif isinstance(y, javalang.tree.MethodInvocation):
                         print(y.member)
                    elif isinstance(y, javalang.tree.Literal):
                        print(y.value)
                    elif isinstance(y, javalang.tree.VariableDeclarator):
                        print(y.value)
            

if __name__ == "__main__":
    main()
