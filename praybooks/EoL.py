#!/usr/bin/env python3
import os
print("Hello again my friend! R u reddy for gudby?")
open("/home/student/mycode/stopper.txt", 'a').close() # this line ensures stopper.txt is created

os.remove("/home/student/mycode/stopper.txt")
