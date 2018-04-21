"""
reads a java file and makes a text file for uml diagrams
just place in your working directory and run!

Author: Jack Frate
created on 4/29/18

"""

import os                       # os module imported here


location = os.getcwd()          # get present working directory location here

java_files = []                 # list to store all java files found at location

output = open("LazyUML_output.txt", "w+")  # creates the output file for UML BUDDY\


# reads for the fields in a java file
def pfile(filename):

    f = open(filename, "r")             # opens the file to be read
    class_name = filename.replace('.java', '')      # gets the name of the constructor

    output.write("\n" + 'Fields and methods for ' + class_name + "\n")
    # for each line in the file, check if its a field or a method, then write to file

    output.write("\n--fields--\n\n")
    for line in f:
        output.write(field_read(line))

    # re open the file for re use
    f.close()
    f = open(filename, "r")

    output.write("\n--methods--\n\n")
    for line in f:
        output.write(method_read(line, class_name))

    # end of func
    output.write("\n============================\n")


def field_read(line):
    line = line.strip()
    ret = ''    # line to be written to uml buddy
    check = False

    if line.startswith('public'):
        if line.endswith(";"):
            ret += "+ "     # shows that it is public
            check = True

    elif line.startswith('protected') or line.startswith('private'):
        if line.endswith(";"):
            ret += '- '
            check = True

    if check:
        vals = line.split()
        vals[2] = vals[2].replace(';', ' : ')   # makes a space
        vals[2] = vals[2].replace(',', ' : ')  # makes a space
        # for multiple

        ret += vals[2]
        ret += vals[1]
        ret += "\n"
        # check for multiple items
        if len(vals) > 3:
            tp = vals[1]
            vals = vals[3:]
            for val in vals:
                # setting up
                val = val.replace(';', ' : ')
                val = val.replace(',', ' : ')
                # gets the beginning of the line
                ret += ret[:2]      # adds the + or - and a space
                # add the name
                ret += val
                ret += tp
                ret += "\n"

        return ret
    return ''


def method_read(line, cname):
    const_check = cname
    const_check += '('

    # strip line and compare to this
    line = line.strip()

    ret = ''    # line to be written to uml buddy
    check = False

    # checks for class declaration
    if 'class' in line:
        return ret

    ln = line.replace(' ', '')
    if const_check in ln:
        return ret

    # checks for constructor declaration

    if line.startswith('public'):
        if line.endswith(")") or line.endswith('{'):
            ret += "+ "     # shows that it is public
            check = True

    elif line.startswith('protected') or line.startswith('private'):
        if line.endswith(")") or line.endswith('{'):
            ret += '- '
            check = True

    if check:
        vals = line.split(' ')
        vals[2] = vals[2].replace('{', '')
        end = vals[1]
        # now check to make sure that the method has every part of it
        vals.pop(0)
        vals.pop(0)
        vals[-1] = vals[-1].replace('{', '')
        name = ''
        for val in vals:
            name += val
            name += ' '
        name += ' : '

        ret += name
        ret += end
        ret += "\n"

        return ret
    return ''


# main loop of program
def main():
    counter = 0
    for file in os.listdir(location):
        try:
            if file.endswith(".java"):
                print("java file found:\t", file)
                java_files.append(str(file))
                counter = counter + 1
                pfile(file)
                # just an exception handle
        except Exception as e:
            print("No files found here!")
            raise e
    print("Total files found:\t", counter)


# run program
main()
