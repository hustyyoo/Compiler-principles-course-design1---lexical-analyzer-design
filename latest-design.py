# latest-design.py - The lexical_analyzer.
# Author: Zehan Li
# Date: June 02
########################################
#
import string
#
########## set global data #############
#
# 32 Key words
keywords = {
    'auto':101,    'int':102,    'double':103,    'long':104,
    'char':105,    'float':106,    'short':107,    'signed':108,
    'unsigned':109,    'struct':110,    'union':111,    'enum':112,
    'static':113,    'switch':114,    'case':115,    'default':116,
    'break':117,    'register':118,    'const':119,    'volatile':120,
    'typedef':121,    'extern':122,    'return':123,    'void':124,
    'continue':125,    'do':126,    'while':127,    'if':128,
    'else':129,    'for':130,    'goto':131,    'sizeof':132
    }
# Symbol
keywords['+'] = 201
keywords['-'] = 202
keywords['*'] = 203
keywords['/'] = 204
keywords['='] = 205
keywords[':'] = 206
keywords['<'] = 207
keywords['>'] = 208
keywords['%'] = 209
keywords['&'] = 210
keywords['!'] = 211
keywords['('] = 212
keywords[')'] = 213
keywords['['] = 214
keywords[']'] = 215
keywords['{'] = 216
keywords['}'] = 217
keywords['#'] = 218
keywords['|'] = 219
keywords[','] = 220
# Symbolic representation of output
signlist = {}
#
### The preprocessing function handles whitespace, newline, and other unrelated characters in the file #
#
def pretreatment(file_name):
    try:
        fp_read = open(file_name, 'r')
        fp_write = open('file.tmp', 'w')
        sign = 0
        while True:
            read = fp_read.readline()
            if not read:
                break
            length = len(read)
            i = -1
            while i < length - 1:
                i += 1
                if sign == 0:
                    if read[i] == ' ':
                        continue
                if read[i] == '#':  #Notes
                    break
                elif read[i] == ' ':
                    if sign == 1:
                        continue
                    else:
                        sign = 1
                        fp_write.write(' ')
                elif read[i] == '\t':
                    if sign == 1:
                        continue
                    else:
                        sign = 1
                        fp_write.write(' ')
                elif read[i] == '\n':
                    if sign == 1:
                        continue
                    else:
                        fp_write.write(' ')
                        sign = 1
                elif read[i] == '"':
                    fp_write.write(read[i])
                    i += 1
                    while i < length and read[i] != '"':
                        fp_write.write(read[i])
                        i += 1
                    if i >= length:
                        break
                    fp_write.write(read[i])
                elif read[i] == "'":
                    fp_write.write(read[i])
                    i += 1
                    while i < length and read[i] != "'":
                        fp_write.write(read[i])
                        i += 1
                    if i >= length:
                        break
                    fp_write.write(read[i])
                else:
                    sign = 3
                    fp_write.write(read[i])
    except Exception:
        print(file_name, ': This FileName Not Found!')
#
### Identifying and saving reserved words and operators in text ######
#
def save(string):
    if string in keywords.keys():
        if string not in signlist.keys():
            signlist[string] = keywords[string]
    else:
        try:
            float(string)
            save_const(string)
        except ValueError:
            save_var(string)
#
### Identifying and saving variables in text ##########################
#
def save_var(string):
    if string not in signlist.keys():
        if len(string.strip()) < 1:
            pass
        else:
            if is_signal(string) == 1:
                signlist[string] = 301
            else:
                signlist[string] = 501
#
##### Identifying and saving constants in text ##################
#
def save_const(string):
    if string not in signlist.keys():
        signlist[string] = 401
#
###### Identifying and saving error characters in text ###########
#
def save_error(string):
    if string not in signlist.keys():
        signlist[string] = 501
#
############## Judge identifiers #####################
#
def is_signal(s):
    if s[0] == '_' or s[0] in string.ascii_letters:
        for i in s:
            if i in string.ascii_letters or i == '_' or i in string.digits:
                pass
            else:
                return 0
        return 1
    else:
        return 0
#
####### Identifying and writes the recognized text to file.tmp ###########
#
def recognize(filename):
    try:
        fp_read = open(filename, 'r')
        string = ""
        sign = 0
        while True:
            read = fp_read.read(1)
            if not read:
                break

            if read == ' ':
                if len(string.strip()) < 1:
                    sign = 0
                    pass
                else:
                    if sign == 1 or sign == 2:
                        string += read
                    else:
                        save(string)
                        string = ""
                        sign = 0
            elif read == '(':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('(')
            elif read == ')':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save(')')
            elif read == '[':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('[')
            elif read == ']':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save(']')
            elif read == '{':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('{')
            elif read == '}':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save('}')
            elif read == '<':
                save(string)
                string = ""
                save('<')
            elif read == '>':
                save(string)
                string = ""
                save('>')
            elif read == ',':
                save(string)
                string = ""
                save(',')
            elif read == "'":
                string += read
                if sign == 1:
                    sign = 0
                    save_const(string)
                    string = ""
                else:
                    if sign != 2:
                        sign = 1
            elif read == '"':
                string += read
                if sign == 2:
                    sign = 0
                    save_const(string)
                    string = ""
                else:
                    if sign != 1:
                        sign = 2
            elif read == ':':
                if sign == 1 or sign == 2:
                    string += read
                else:
                    save(string)
                    string = ""
                    save(':')
            elif read == '+':
                save(string)
                string = ""
                save('+')
            elif read == '=':
                save(string)
                string = ""
                save('=')
            else:
                string += read

    except Exception as e:
        print(e)
#
###### main ########
#
def main():
    file = input("Please Input FileName: ")
    pretreatment(file)
    recognize('file.tmp')
    key_list=signlist.keys()
    for i in key_list:
        print(i,signlist[i])
#

main()
##########################
