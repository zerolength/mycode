#https://github.com/zerolength/NetworkAutomationProj/pull/14
#!/usr/bin/env python
#parser.py
import subprocess
import yaml
import re
import ipaddress

def calculate_last(ip_str, cidr_str):
    # Parse the IP address and CIDR notation
    ip_ = ip_str + cidr_str
    ip = ipaddress.IPv4Network(ip_)
      
    # Calculate the broadcast address
    last = ip[-1]
    return str(last)

def importer(filename):
    with open(filename, "r") as stream:
        try:
            assembly = yaml.safe_load(stream)
            #print(assembly)
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


def link_ns (entity,linkname, linkip):
    #given 2 namespace and create veth to link them
    #sudo ip link add crout2orout type veth peer name orout2crout
    #sudo ip link set crout2orout netns crouter
    #sudo ip link set orout2crout netns orouter
    #[ns1,ns2] = interface['name'].split("-to-") #need testning I rather change the yaml
    if linkname == 'loopback':
        return linkname
    [ns1,ns2] = custom_split(linkname)
    
    print(f"split {linkname} {ns1}, {ns2}")
#   rlinkname = ns2+'2'+ns1
    if  ns1 == None:
        ns1 = entity
        linkname = ns1+'2'+ns2[0]+'router'
        fullip = linkip + '/30'
        return linkname
    
    elif ns2 != None:
        linkname = ns1+'2'+ns2
        rlinkname = ns2+'2'+ns1
    
        subprocess.run(["sudo","ip","link","add",linkname,"type","veth","peer","name", rlinkname])
        print (f"{linkname} {ns1} {ns2}")
        subprocess.run(["sudo","ip","link","set",linkname,"netns",entity])
        if "bridge" in ns2:
            subprocess.run(["sudo","ip","link","set","dev", rlinkname, "master", ns2])
        subprocess.run(["sudo","ip","link","set",rlinkname,"netns",ns2])
        
        if ns1 == 'core' or ns2 == 'core':
            fullip = linkip + '/30'
        else:
            fullip = linkip + '/24'
        #sudo ip netns exec yrouter ip addr add 10.1.5.6/30 dev yrout2crout
        #sudo ip netns exec crouter ip link set dev crout2orout up
        #sudo ip netns exec crouter ip link set dev lo up
        subprocess.run(["sudo","ip","netns","exec",entity,"ip","addr","add",fullip, "dev", linkname])
        subprocess.run(["sudo","ip","netns","exec",entity,"ip","link","set", "dev", linkname,"up"])
        subprocess.run(["sudo","ip","netns","exec",entity,"ip","link","set", "dev", "lo","up"])
    else: #ns2 is none
        print(f"badlink: {entity} {linkname}")
#        subprocess.run(["sudo","ip","link","set",linkname,"netns",ns2])
    #add ip
    
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
            brname = self.nsname[0]+'bridge'
        #subprocess.call(['sudo','ip','link','add','name',bridges['name'] + 'brdg','type','bridge'])
            subprocess.run(['sudo','ip','link','add','name', brname,'type','bridge'])
            print(f"br {nsname}")
            subprocess.run(['sudo','ip','link','set','dev', brname,'up'])


    def change_ip(self,new):
        print(f"old ip {self.ip}, new ip{new}")
        self.ip = new
    def add_host(self,host):
        #sudo ip netns exec phost ip route add default via 10.1.1.1
        hname=host.hname
        subnetname=self.nsname
        subprocess.run(["sudo","ip","netns","exec",hname,"ip","route","add","default","via",self.gw])
        
        

    def __del__ (self):
        if self.bridge == True:
            subprocess.run(["sudo","ip","link","del",self.nsname])
            print(f"del {self.nsname}")


class Router ():
    def __init__ (self, rname, interfaces):
        self.rname = rname
        print(self.rname)

        subprocess.call(["sudo","ip","netns","add",rname])
        #sudo ip netns exec orouter sysctl -p /etc/sysctl.d/10-ip-forwarding.conf
        subprocess.call(["sudo","ip","netns","exec",rname,"sysctl","-p","/etc/sysctl.d/10-ip-forwarding.conf"])
        
        self.inf = interfaces
        print(self.inf)
        self.links = {}
        #connect interfaces
        for interface in interfaces:
            print(interface)
            linkname = interface['name']
            print(linkname)
            linkip = interface['ip']
            
            newlink=link_ns (self.rname,linkname,linkip)
            self.links[linkname]=newlink
            print (newlink)
        print (self.links)
        
    #routing
    #sudo ip netns exec crouter ip route add 10.1.1.0/24 via 10.1.5.2
    def add_net(self,subnetEdge,subnetCore):
        last = calculate_last(subnetCore.ip, subnetCore.cidr)
        subprocess.run(["sudo","ip","netns","exec",self.rname,"ip","route","add",subnetEdge.ip+subnetEdge.cidr,"via",last])
    
    #sudo ip netns exec prouter ip route add default via 10.1.5.1
    def add_default(self,router,subnetCore):
        rname = router.rname
        subprocess.run(["sudo","ip","netns","exec",rname,"ip","route","add","default","via",subnetCore.gw])
    
    def __del__ (self):
        subprocess.run(["sudo","ip","netns","del",self.rname])

class Host ():
    def __init__(self, hname, interfaces):
        self.hname = hname
        self.inf= interfaces

        subnet = interfaces[0]['subnet']
        self.subnet=subnet

        self.links = []
        
        subprocess.run (['sudo','ip','netns','add',hname])
        
        for interface in interfaces:
            linkname = interface['name']
            linkip = interface['ip']
            newlink = link_ns(self.hname,linkname,linkip)
            
            self.links.append(newlink)
            print(newlink)
        print (self.links)
def main ():
    filename = "network_topology.yml"
    assembly = importer(filename)

    subnets = assembly ['subnets']
    sholder = {}
    for object in subnets:
        
        nsname = object['name']
        new_subnet = Subnet (nsname=object['name'],bridge=object['bridge'],ip=object['subnet_ip'],cidr=object['cidr'],gw=object['gw'],dhcp_range=object['dhcp_range'])
        sholder[nsname] = new_subnet
    
    subprocess.run(['sudo','sysctl','net.bridge.bridge-nf-call-iptables=0'])
    subprocess.run(['echo','\'net.ipv4.ip_forward','=','1\n','net.ipv6.conf.default.forwarding','=','1\n','net.ipv6.conf.all.forwarding','=','1\'','|','sudo','tee','/etc/sysctl.d/10-ip-forwarding.conf'])

    print("Showing up bridges")
    subprocess.run(['sudo','brctl','show'])
    
    routers = assembly ['routers']
    rholder = {}
    for object in routers: #missing nexthop
        rname = object ['name']
        new_router = Router (rname = object['name'], interfaces = object['interfaces'])
        rholder[rname] = new_router
    print(rholder)
    print("Showing Created Namespaces...")
    subprocess.run(['sudo','ip','netns'])
    
    hosts = assembly ['hosts']
    hholder = {}
    for host in hosts: #missiong vlan, need to implement dhcp
        hname = host['name']
        new_host = Host (hname = host['name'], interfaces = object['interfaces'])
        hholder[hname]=new_host
    print(hholder)
    input("Press Enter to continue...you can check if netns is up")

    #actual routing
    #add hosts 
    ##Need to pick the host's subnet property later
    purplehost= hholder['phost']
    yellohost= hholder['yhost']
    whitehost= hholder['whost']
    oranghost= hholder.get('ohost')
    sholder['purple'].add_host(purplehost)
    sholder['yellow'].add_host(yellohost)
    sholder.get('white').add_host(whitehost)
    sholder.get('orange').add_host(oranghost)

    #add route to core
    rholder.get('core').add_net(sholder.get('purple'),sholder.get('purple-core'))
    rholder.get('core').add_net(sholder.get('orange'),sholder.get('orange-core'))
    rholder.get('core').add_net(sholder.get('yellow'),sholder.get('yellow-core'))
    rholder.get('core').add_net(sholder.get('white'),sholder.get('white-core'))
    #add default from core subnets

    rholder.get('core').add_default(rholder['purple'],sholder.get('purple-core'))
    rholder.get('core').add_default(rholder['orange'],sholder.get('orange-core'))
    rholder.get('core').add_default(rholder.get('yellow'),sholder.get('yellow-core'))
    rholder.get('core').add_default(rholder.get('white'),sholder.get('white-core'))




if __name__ == "__main__":
    main()
