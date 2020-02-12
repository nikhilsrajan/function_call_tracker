from sys import argv

if len(argv) == 1:
	print('Not enough arguments.')
	exit()
elif len(argv) > 2:
	print('Too many arguments.')
	exit()

project_name = argv[1]

folderpath = './tracker/'

in_file = folderpath + project_name + '.txt'

START = 'START'
END = 'END'


def GetFirstLast(line:str):
    splits = line.split()
    return splits[0], splits[-1]

def PrintList(list):
    for item in list:
        print(item)
        
def ExportList(list, filename:str, end='\n'):
    with open(filename, 'w+') as f:
        for item in list:
            f.write(str(item) + end)
        
def ReadList(list, int):
    return list[int], int+1

def Format(key:int, string:str):
	return "{k:10}   {s}".format(k=key, s=string)


key = 0
key_subseq = dict()
key_count = dict()
key_func = dict()
subseq_key = dict()
seqofsubseq = list()
subseq = list()
subseq_balance = 0

seqofsubseq.append('SubSeq Key   Root Func')
seqofsubseq.append('----------   ---------')

with open(in_file, 'r') as f:
    lines = f.readlines()
    len_lines = len(lines)
    index = 0
    while index < len_lines:
        line, index = ReadList(lines, index)
        subseq.append(line)
        first, root_func = GetFirstLast(line)
        if first == START:
            subseq_balance = 1
            while subseq_balance != 0 and index < len_lines:
                line, index = ReadList(lines, index)
                first, last = GetFirstLast(line)
                subseq.append(line)
                if first == START:
                    subseq_balance += 1
                elif first == END:
                    subseq_balance -= 1
        t_subseq = tuple(subseq)
        if t_subseq in subseq_key.keys():
        	k = subseq_key[t_subseq]
        	seqofsubseq.append(Format(k, root_func))
        	count = key_count[k]
        	key_count[k] = count + 1
        else:
            key_subseq[key] = t_subseq
            subseq_key[t_subseq] = key
            seqofsubseq.append(Format(key, root_func))
            key_count[key] = 1
            key_func[key] = root_func
            key += 1
        subseq.clear()


ExportList(seqofsubseq, folderpath + project_name + '_SeqOfSubSeqs.txt')

print('SubSeq Key   No. of steps   No. of reps   Root Func')
print('----------   ------------   -----------   ---------')
for key, value in key_subseq.items():
    print('%10i   %12i   %11i   %s' % (key, len(list(value)) / 2, key_count[key], key_func[key]) , sep='')
    ExportList(list(value), folderpath + project_name + '_SubSeq_' + str(key) + '.txt', end='')