#!/usr/bin/python
"""
My way of using searchsploit.
+ I like to sort them according to the exploit date.
+ I do not like seeing the link and location of the exploits so I removed them.

Example of the outputs:
$ ./qsearchsploit.py samba

2017-05-29 Samba 3.5.0 < 4.4.14/4.5.10/4.6.4 - is_known_pipename() Arbitrary Module Load (Metasploit)
2017-05-24 Samba 3.5.0 - Remote Code Execution
2017-03-27 Samba 4.5.2 - Symlink Race Permits Opening Files Outside Share Directory
2015-04-13 Samba < 3.6.2 (x86) - Denial of Service (PoC)
2013-08-22 Samba 3.5.22/3.6.17/4.0.8 - nttrans Reply Integer Overflow
2012-10-10 Samba 3.4.16/3.5.14/3.6.4 - SetInformationPolicy AuditEventsInfo Heap Overflow (Metasploit)
2012-09-24 Samba 3.5.11/3.6.3 - Remote Code Execution
2011-07-27 SWAT Samba Web Administration Tool - Cross-Site Request Forgery
2010-09-04 Samba 3.3.12 (Linux x86) - chain_reply Memory Corruption (Metasploit)
2010-08-18 Samba 3.0.20 < 3.0.25rc3 - Username map script Command Execution (Metasploit)
2010-07-14 Samba 2.2.8 (Linux x86) - trans2open Remote Overflow (Metasploit)
2010-07-14 Samba 3.0.24 (Linux) - lsa_io_trans_names Heap Overflow (Metasploit)
2010-06-21 Samba 2.2.8 (OSX/PPC) - trans2open Remote Overflow (Metasploit)
2010-06-21 Samba 2.2.8 (Solaris SPARC) - trans2open Remote Overflow (Metasploit)

Sorted and clean baby :)

"""

import sys
import subprocess
from datetime import datetime
from colorama import Fore, Back, Style

colors=1
debug=0
j=0

def execute_command(command):
    if len(command) > 0:
        if debug:
            pass
            print("def execute_command(command):")
            print(command)
        result = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        out, err = result.communicate()
        if debug:
            pass
            print(out)
        return out

def searchsploit(word):
    command = "searchsploit -j "+str(word)
    out = execute_command(command)
    out = filter(out)
    out = sort_inputs(out)
    return out

def filter(inputs):
    if debug:
        print("def filter(inputs):")
    inputs = inputs.split("\n\t")
    final_list = []
    for line in inputs:
        one_line=[]
        if "Title" in line:
            #[Title, EDB-ID, Date, Author, Type, Platform, Path]
            line = line.replace("{", "").replace("}", "").replace("{", "")\
                .replace('"', "").replace("'", "").replace("\t", "").split(",")[:-1]
            for p in line:
                one_line.append(p.split(":"))
            if debug:
                pass
                print(line)
        final_list.append(one_line)
    return final_list

def sort_inputs(inputs):
    if debug:
        print("def sort_inputs(inputs):")
    unsortedArray = []
    for exploit in inputs:
        if len(exploit) < 1:
            continue
        pass
        if debug:
            pass
            print("exploit",exploit)
        data = exploit[2][1]
        unsortedArray.append({exploit[0][0]: exploit[0][1], exploit[2][0]: data})
    #2010-07-14
    sortedArray = sorted(
    unsortedArray,
    key=lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'), reverse=True)
    return sortedArray

def print_as_wanted(inputs):
    if debug:
        print("def print_as_wanted(inputs):")
    for exploit in inputs:
        if j:
            pass
        else:
            toPrint = exploit.get("Date")+" "+exploit.get("Title")
            if colors:
                if "Privilege Escalation" in toPrint or "PE" in toPrint:
                    print(Fore.GREEN + toPrint),
                    print(Style.RESET_ALL)
                elif "(Metasploit)" in toPrint:
                    print(Fore.BLUE + toPrint),
                    print(Style.RESET_ALL)
                elif "Remote Command Execution" in toPrint or "RCE" in toPrint:
                    print(Fore.RED + toPrint),
                    print(Style.RESET_ALL)
                elif "SQL Injection" in toPrint:
                    print(Fore.LIGHTCYAN_EX + toPrint),
                    print(Style.RESET_ALL)
                else:
                    print(toPrint)
            else:
                print(toPrint)


def main():
    out = searchsploit("mysql")
    if len(sys.argv) >= 2:
        out = searchsploit(sys.argv[1])
        print_as_wanted(out)
    else:
        print("No arguments")

if __name__ == '__main__':
    main()
