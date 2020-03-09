from os import listdir, getcwd, remove
from os.path import isfile, join
import time
from sys import argv

line_to_add_in_file = '#include "./../../utility/Tracker.h"'
line_to_add_in_func = 'Tracker __t(std::string(__FUNCTION__));'
ignore_files = ['Tracker.h', 'Tracker.cpp']

def stripcomments(__in_filename, __out_filename):
    c = ''
    start_time = time.time()
    with open(__out_filename, 'w') as _out:
        with open(__in_filename, 'r') as _in:
            while True:
                c = _in.read(1)
                if not c:
                    break
                elif c == '/':
                    c = _in.read(1)
                    if c == '/':
                        while c != '\n':
                            c = _in.read(1)
                        _out.write('\n')
                    elif c == '*':
                        while True:
                            c = _in.read(1)
                            cur_pos = _in.tell()
                            if c == '*':
                                c = _in.read(1)
                                if c == '/':
                                    break
                                else:
                                    _in.seek(cur_pos)
                            elif c == '\n':
                                _out.write(c)
                    else:
                        _out.write('/' + c)
                elif c == '"':
                    _out.write(c)
                    while True:
                        c = _in.read(1)
                        _out.write(c)
                        if c == '\\':
                            c = _in.read(1)
                            _out.write(c)
                        elif c == '"' or not c:
                            break
                else:
                    _out.write(c)
    end_time = time.time()
    print("stripcomments \t-- %s seconds --" % (end_time - start_time))
    return __out_filename


def pad(line):
    return '\n\t' + line + '\n'


def isalpha(__c):
    if __c == '':
        return False
    elif (ord('A') <= ord(__c) <= ord('Z')) or (ord('a') <= ord(__c) <= ord('z')) or __c == '_':
        return True
    else:
        return False


def isnum(__c):
    if __c == '':
        return False
    elif ord('0') <= ord(__c) <= ord('9'):
        return True
    else:
        return False


def isalnum(__c):
    if isalpha(__c) or isnum(__c):
        return True
    else:
        return False


def iswhitespace(__c):
    if __c == ' ' or __c == '\t' or __c == '\n':
        return True
    else:
        return False


def lineadder(__line_to_add_in_file, __line_to_add_in_func, __in_filename, __out_filename):
    c = ''
    word = ''
    paran_count = 0
    paran_pass = False
    block_count = 0
    ignore_words = ['if', 'for', 'while', 'switch', 'Q_ENUM']
    start_time = time.time()
    with open(__out_filename, 'w') as _out:
        _out.write(line_to_add_in_file + '\n')
        with open(__in_filename, 'r') as _in:
            while True:
                c = _in.read(1)
                if not c:
                    break
                while iswhitespace(c):              # keeps traversing till a none whitespace character is encountered
                    _out.write(c)
                    c = _in.read(1)
                if c == '"':                        # if the character is a double quote ... (string)
                    _out.write(c)
                    while True:                     # ... keep traversing ...
                        c = _in.read(1)
                        _out.write(c)
                        if c == '\\':               # ignore the character that comes after backslash
                            c = _in.read(1)
                            _out.write(c)           # ... until the next double quote is encountered.
                        elif c == '"':
                            break
                elif c == '#':                      # if charcter is # ... (macros)
                    _out.write(c)
                    while True:                     # ... keep traversing ...
                        c = _in.read(1)
                        _out.write(c)
                        if c == '\\':               # ignore the character that comes after backslash
                            c = _in.read(1)
                            _out.write(c)
                        elif c == '\n' or not c:    # ... till new line character is encountered.
                            break
                elif isalpha(c):                    # is the character is an alphabet ...
                    _out.write(c)
                    word = ''                   
                    word += c
                    cur_pos = _in.tell()
                    c = _in.read(1)                 # ... read the next character ....
                    if iswhitespace(c):             # ... to see if it is whitespace
                        _out.write(c)
                    elif isalnum(c):                # if the next character is alnum
                        while isalnum(c):           # as long as the next character is alnum
                            _out.write(c)
                            word += c               # keep appending the word with the character (we capture a token which is not a string nor a macro definition)
                            cur_pos = _in.tell()
                            c = _in.read(1)
                        _in.seek(cur_pos)
                    else:                           # if the next character is not alnum nor whitespace ...
                        _in.seek(cur_pos)           # ... start over and re-read the character
                elif c == '(':                      # if the character is an open parenthesis ...
                    _out.write(c)
                    if word not in ignore_words:    # if the captured word is not in ignored words list ...
                        paran_pass = True           # set paran pass to True (possible function block upcoming) -> WORD ( ... 
                        paran_count += 1            
                    while paran_count != 0:         # traverse until parenthesis balanced -> WORD (())
                        c = _in.read(1)
                        _out.write(c)
                        if c == '(':
                            paran_count += 1
                        elif c == ')':
                            paran_count -= 1
                elif c == ';' and paran_pass == True:   # if ; encountered -> WORD (()) ; <- possible function call.
                    _out.write(c)
                    paran_pass = False
                elif (c == ':' or c == ',') and paran_pass == True: # : or , <- Initializer list
                    _out.write(c)
                    cur_pos = _in.tell()
                    c = _in.read(1)
                    if c == ':':                    # -> WORD (()) :: or WORD (()) ,:  [?] - dunno if this is ever entered.
                        _out.write(c)
                        pass
                    else:
                        _in.seek(cur_pos)
                        while c != '(' and c != '{' and c != ';':   # ( { ;
                            c = _in.read(1)
                            _out.write(c)
                        if c == '(':                # WORD (()) : x (
                            while c != ')':         # WORD (()) : x ( .. ) <- doesn't handle WORD : x ({()})
                                c = _in.read(1)
                                _out.write(c)
                        elif c == '}':              # WORD (()) , x {
                            while c != '}':         # WORD (()) , x { .. } <- doesn't handle WORD : x {({})}
                                c = _in.read(1)
                                _out.write(c)
                        elif c == ';':              # WORD (()) : x ; [?] - dunno if this is ever entered. Ternary operator?
                            _out.write(c)
                            paran_pass = False
                elif c == '{':                      # WORD (()) : x () {
                    _out.write(c)
                    if paran_pass == True:          # possible function declaration.
                        _out.write(pad(__line_to_add_in_func))
                        paran_pass = False
                        block_count += 1
                        while block_count != 0:
                            c = _in.read(1)
                            _out.write(c)
                            if c == '{':
                                block_count += 1
                            elif c == '}':
                                block_count -= 1
                else:                               # every other case - ignore.
                    _out.write(c)
    end_time = time.time()
    print("lineadder \t-- %s seconds --" % (end_time - start_time))


def addlinetofilesinfolder(__line_to_add_in_file='/* LINEADDER FILE TEST */',
                           __line_to_add_in_func='/* LINEADDER FUNC TEST */',
                           __folderpath=getcwd()):
    all_files = [f for f in listdir(__folderpath) if isfile(join(__folderpath, f))]
    filtered_files = [f for f in all_files if f not in ignore_files and (f.endswith('.h') or f.endswith('.cpp'))]
    temp = '__temp__'
    for file in filtered_files:
        file = __folderpath + file
        print('Adding line %s to %s' % (__line_to_add_in_func, file))
        stripcomments(file, temp)
        lineadder(__line_to_add_in_file, __line_to_add_in_func, temp, file)
        remove(temp)


if __name__ == '__main__':
    passed_one = 0
    if len(argv) == 1:
        print('Not enough arguments.')
        exit()
    for i, arg in enumerate(argv):
        if i == 0:
            pass
        elif arg == 'C' or arg == 'c':
            passed_one += 1
            addlinetofilesinfolder(line_to_add_in_file, line_to_add_in_func, './../code/Controller/')
        elif arg == 'M' or arg == 'm':
            passed_one += 1
            addlinetofilesinfolder(line_to_add_in_file, line_to_add_in_func, './../code/Model/')
        elif arg == 'V' or arg == 'v':
            passed_one += 1
            addlinetofilesinfolder(line_to_add_in_file, line_to_add_in_func, './../code/View/')
        else:
            print('Unknown argument \'', arg, '\'. Argument ignored.', sep='')
    if len(argv) > 1 and passed_one == 0:
        print('All arguments invalid.')
        exit()
