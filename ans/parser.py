#!/usr/bin/env python

import subprocess
import yaml

def importer(filename):
    with open(filename, "r") as stream:
        try:
            assembly = yaml.safe_load(stream)
            print(assembly)
        except yaml.YAMLError as exc:
            print(exc)
    return assembly

class Subnet ():
    def __init__ (self, nsname, bridge, ip):
        self.nsname =  nsname
        self.bridge = bridge
        self.ip = ip
        print(self.ip)
        print(self.nsname)
        print(self.bridge)
        #sudo ip netns add ohost
        subprocess.run(["sudo","ip","netns","add",nsname]) 

    def __del__ (self):
        subprocess.run(["sudo","ip","netns","del",self.nsname]) 

def main ():
    filename = "network_topology.yml"
    assembly = importer(filename)
    with open(filename, "r") as stream:
        try:
            assembly = yaml.safe_load(stream)
            print(assembly)
        except yaml.YAMLError as exc:
            print(exc)
    subnets = assembly ['subnets']
    holder = []
    print (subnets)
    for object in subnets:
        new_subnets = Subnet (nsname=object['name'],bridge=object['bridge'],ip=object['subnet_ip'])
        
        holder.append(new_subnets)

    print (holder)
    input("Press Enter to continue...you can check if netns is up")
if __name__ == "__main__":
    main()
