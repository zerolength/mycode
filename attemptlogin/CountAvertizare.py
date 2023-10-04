#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def main():
    line_num = [];
    faillines = [];
    if len(sys.argv) > 1:
        logname  = sys.argv[1]
    else:
        logname = 'keystone.common.wsgi'
    #log_stack = open('keystone.common.wsgi','r');
    checkstring = '- - - -] Authorization failed.'
    counter = 0;
    with open(logname,"r") as log_stack:
        for line in log_stack:
            counter+=1
            if checkstring in line:
                line_num.append(counter)
                faillines.append(line)

    log_stack.close()

    print (line_num)
    print (faillines)
    failips = [flin.split(" ")[-1] for flin in faillines]
    print (failips)


        


if __name__ == '__main__':
  main()
