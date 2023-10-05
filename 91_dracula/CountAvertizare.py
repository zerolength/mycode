#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

def main():
    line_num = [];
    faillines = [];
    if len(sys.argv) > 1:
        logname  = sys.argv[1]
    else:
        logname = 'dracula.txt'
    checkstring = 'vampire'
    counter = 0;
    with open(logname,"r") as log_stack:
        for line in log_stack:
            counter+=1
            #if checkstring in line:
            #if re.search('mandy', 'Mandy Pande', re.IGNORECASE):

            if re.search('vampire', line, re.IGNORECASE):
                line_num.append(counter)
                faillines.append(line)

    log_stack.close()

    print (line_num)
    print (faillines)

    with open('vampytimes.txt', 'w') as times:
        for line in faillines:
            times.write(f"{line}")
    times.close()

#    failips = [flin.split(" ")[-1] for flin in faillines]
#    print (failips)


        


if __name__ == '__main__':
  main()
