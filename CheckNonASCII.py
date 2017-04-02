'''
Create @ 2017/03/29
Author: zhouchao
'''
# -*- coding: utf-8 -*-

import codecs
import os
import chardet


def main():
    # dir = r"C:\Users\zhouchao\SkyDrive\Python\ISASCII"
    dir = cur_file_dir()
    basfile_array = []
    files_array = []
    tmpstr = ""
    GetFiles(basfile_array, dir, '.bas')
    for file in basfile_array:
        result = find_ASCII_files(file)
        if result != "":
            files_array.append(file)
            tmpstr = tmpstr + '\n' + result

    clsfile_array = []
    GetFiles(clsfile_array, dir, '.cls')
    for file in clsfile_array:
        result = find_ASCII_files(file)
        if result != "":
            files_array.append(file)
            tmpstr = tmpstr + '\n' + result

    # print(tmpstr)
    output = open(dir + r'/output.txt', 'w+')
    # output.write(tmpstr)
    if tmpstr != '':
        output.write(tmpstr)
    else:
        output.write("All files are valid ASCII encoding.")
    output.close
    # files_array = basfile_array + clsfile_array
    print_output_file(files_array, dir)


# to get the path of file with non-ASCII char
def find_ASCII_files(filepath):
    try:
        f = codecs.open(filepath, 'r', encoding='ASCII')
        content = f.read()
        return ""
    except ValueError as err:
        # print("The Error Message is: {0}".format(err))
        return filepath


# to output the index of line with non-ASCII char
def print_output_file(files_array, dir):
    dir = dir + r'/output.csv'
    with open(dir, mode='w') as csvfile:
        for file in files_array:
            csvfile.write(file)
            find_non_ASCII_lines(file, 'utf-8', csvfile)
            csvfile.write('\n')


# to find non ASCII lines index in all found files
def find_non_ASCII_lines(filepath, encoding_mode, csvfile):
    with open(filepath, mode='r', encoding=encoding_mode) as f:
        #
        try:
            line_index = 0
            while True:
                line_index += 1
                line = f.readline()
                if all(ord(c) < 128 for c in line) is False:
                    csvfile.write(',' + str(line_index))
                if len(line) == 0:
                    break
        except ValueError:
            f.close()
            # read the in bytes format to detect the coding format
            with open(filepath, mode='rb') as f:
                f_read = f.read()
                f_charInfo = chardet.detect(f_read)
            return find_non_ASCII_lines(filepath, f_charInfo[
                'encoding'], csvfile)


def GetFiles(files_array, dirname, extname):
    for path in os.listdir(dirname):
        absolutely_path = os.path.join(dirname, path)
        if os.path.isdir(absolutely_path):
            GetFiles(files_array, absolutely_path, extname)
        elif os.path.splitext(absolutely_path)[1] == extname:
            files_array.append(absolutely_path)
        else:
            pass
            # print(path)
            # print("OK")


def cur_file_dir():
    path = os.getcwd()
    return path


'''
    path = sys.path[0]

    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
'''


# to check the VBT header 'Option Explicit'
def check_header():
    pass


if __name__ == '__main__':
    main()
    # a=input("ddddd")
    # print(a)
