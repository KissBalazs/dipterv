import os, sys

exts = ['.py', '.ini', '.c', '.h']
count_empty_line = True
here = os.path.abspath(os.path.dirname(sys.argv[0]))

def read_line_count(fname):
    count = 0
    for line in open(fname).readlines():
        if count_empty_line or len(line.strip()) > 0:
            count += 1
    return count
if __name__ == '__main__':
    line_count = 0
    file_count = 0
    for base, dirs, files in os.walk(here):
        for file in files:
            # Check the sub directorys            
            if file.find('.') < 0:
                continue
            ext = (file[file.rindex('.'):]).lower()
            try:
                if exts.index(ext) >= 0:
                    file_count += 1
                    path = (base + '/'+ file)
                    c = read_line_count(path)
                    print (path[len(here):], c)
                    line_count += c
            except:
                pass
    print ('File count : ' + str(file_count))
    print ('Line count : '+ str(line_count))