#https://github.com/zerolength/NetworkAutomationProj/pull/8
#!/usr/bin/env python
#parser.py
import subprocess
import yaml
import re


def importer(filename):
    with open(filename, "r") as stream:
        try:
            assembly = yaml.safe_load(stream)
            print(assembly)
        except yaml.YAMLError as exc:
            print(exc)
    return assembly


def ip2subnet(ip, subnet):
    #this function will check ip against subnet and vice versa, fillin in if one is empty

    return ip, subnet


def custom_split(input_string):
    # Define a regular expression pattern to match "2" or "-to-" or "to-"
    pattern = r"(?:2|-to-|to-)"
    
    # Split the input using the pattern
    parts = re.split(pattern, input_string, maxsplit=1)
    
    # Handle the case where the input starts with the separator
    if parts[0] == '' and len(parts) == 2:
        return None, parts[1]
    return parts

    #results = [custom_split(s) for s in input_strings]


def link_ns (entity,linkname, ip):
    #given 2 namespace and create veth to link them
    #sudo ip link add crout2orout type veth peer name orout2crout
    #sudo ip link set crout2orout netns crouter
    #sudo ip link set orout2crout netns orouter
    #[ns1,ns2] = interface['name'].split("-to-") #need testning I rather change the yaml
    [ns1,ns2] = custom_split(linkname)
    if  ns1 == None:
        ns1 = entity
    if ns2 == None:
        ns2 = 'loopback'
    if len(linkname) > 15:
        linkname = ns1[:5]+'2'+ns2[:5]
        
    if ns2 != 'loopback':
        subprocess.run(["sudo","ip","link","add",linkname,"type","veth","peer","name",linkname])
        subprocess.run(["sudo","ip","link","set",linkname,"netns",ns1])
    else: 
        print(f"badlink: {entity}{linkname}")
#        subprocess.run(["sudo","ip","link","set",linkname,"netns",ns2])

    return linkname


def unlink_ns (linkname):
    #delete veth yet to implement
    subprocess.run(["sudo","ip","link","del",linkname])

class Subnet (): #create bridge when bridge is true
    def __init__ (self, nsname, bridge, ip, cidr, gw, dhcp_range):
        self.nsname =  nsname
        self.bridge = bridge
        self.ip = ip
        self.cidr = cidr
        self.gw = gw
        self.dhcp = dhcp_range #this need to be split into begin and end
        print(self.ip)
        print(self.nsname)
        print(self.bridge)
        if self.bridge == True:
        #subprocess.call(['sudo','ip','link','add','name',bridges['name'] + 'brdg','type','bridge'])
            subprocess.call(['sudo','ip','link','add','name', nsname,'type','bridge'])
            subprocess.call(['sudo','ip','link','set','dev', nsname,'up'])


    def change_ip(new):
        print(f"old ip {self.ip}, new ip{new}")
        self.ip = new

    def __del__ (self):
        subprocess.run(["sudo","ip","link","del",self.nsname])


class Router ():
    def __init__ (self, rname, interfaces):
        self.rname = rname
        #sudo ip netns add ohost
        subprocess.run(["sudo","ip","netns","add",rname])
        self.inf = interfaces
        self.links = []
        for interface in interfaces:
            linkname = interface['name']
            linkip = interface['ip']
            newlink=link_ns (self.rname,linkname,linkip)
            self.links.append(newlink)
            print (newlink)
        print (self.links)
        #add routing code here
        #connect interfaces
    def __del__ (self):
        subprocess.run(["sudo","ip","netns","del",self.rname])

class Host ():
    def __init__(self, hname, interfaces):
        self.hname = hname
        self.inf= interfaces
        self.droute=default_r
        self.adj = adj
        self.links = []
        #subprocess.call(['sudo','ip','netns','add',hosts['name']])
        #subprocess.call(['sudo','ip','link','add',hosts['name'] + '2' + hosts['name'] + 'brdg','type','veth','peer','name',hosts['name'] + 'brdg' + '2' + hosts['name']])
        subprocess.call (['sudo','ip','netns','add',hname])
        for interface in interfaces:
            linkname = interface['name']
            linkip = interface['ip']
            newlink = link_ns(self.hname,linkname,linkip)
            newlink = link_ns (ns1,ns2)
            self.links.append(newlink)
            print(newlink)
        print (self.links)
def main ():
    filename = "network_topology.yml"
    assembly = importer(filename)

    subnets = assembly ['subnets']
    sholder = []
#    print (subnets)
    for object in subnets:
        new_subnets = Subnet (nsname=object['name'],bridge=object['bridge'],ip=object['subnet_ip'],cidr=object['cidr'],gw=object['gw'],dhcp_range=object['dhcp_range'])
        sholder.append(new_subnets)
#    print (sholder)

    routers = assembly ['routers']
    rholder = []
    for object in routers: #missing nexthop
        new_router = Router (rname = object['name'], interfaces = object['interfaces'])
        rholder.append(new_router)
    hosts = asssembly ['hosts']
    hholder = []
    for host in hosts: #missiong vlan, need to implement dhcp
        new_host = Host (hname = host['name'], interfaces = object['interfaces'])
        hholder.append[new_host]
    print(rholder)
    print(hholder)

    input("Press Enter to continue...you can check if netns is up")
if __name__ == "__main__":
    main()
