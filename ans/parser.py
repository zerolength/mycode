#https://github.com/zerolength/NetworkAutomationProj/pull/14
#!/usr/bin/env python
#parser.py
import subprocess
import yaml
import re
import ipaddress
import time

def calculate_last(ip_str, cidr_str):
    # Parse the IP address and CIDR notation
    ip_ = ip_str + cidr_str
    ip = ipaddress.IPv4Network(ip_)
      
    # Calculate the broadcast address
    last = ip[-2]
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
        time.sleep (1)
        print (f"sudo ip link add {linkname} type veth peer name {ns2} 2 {ns1}")
        subprocess.run(["sudo","ip","link","set",linkname,"netns",ns1])
        if "bridge" in ns2:
            
            subprocess.run(["sudo","ip","link","set","dev", rlinkname, "master", ns2])
            subprocess.run(["sudo","ip","link","set","dev", rlinkname, "up"])
            
        else:
            subprocess.run(["sudo","ip","link","set",rlinkname,"netns",ns2])
        
        if ns1 == 'core' or ns2 == 'core':
            fullip = linkip + '/30'
        else:
            fullip = linkip + '/24'
        #sudo ip link add yrouter2core type veth peer name core2yrouter
        #sudo ip netns exec yrouter ip addr add 10.1.5.6/30 dev yrout2crout
        #sudo ip netns exec yrouter ip link set dev yrout2crout up
        #sudo ip netns exec yrouter ip link set dev lo up

        #sudo ip netns exec wrouter ip addr add 10.1.3.1/24 dev wrout2wbrg
        #sudo ip netns exec wrouter ip link set dev wrout2wbrg up
        #sudo ip netns exec wrouter ip link set dev lo up

        #sudo ip netns exec ohost ip addr add 10.1.4.21/24 dev ohost2obrg
        #sudo ip netns exec ohost ip link set dev ohost2obrg up
        #sudo ip netns exec ohost ip link set dev lo up#sudo ip netns exec pbridge ip link set dev pbridge2prouter up
        #
        print("ip problems") 
        subprocess.run(["sudo","ip","netns","exec",ns1,"ip","addr","add",fullip, "dev", linkname])
        subprocess.run(["sudo","ip","netns","exec",ns1,"ip","link","set", "dev", linkname,"up"])
        subprocess.run(["sudo","ip","netns","exec",ns1,"ip","link","set", "dev", "lo","up"])
        print("end ip")
    else: #ns2 is none
        print(f"badlink: {entity} {linkname}")


    
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

        if self.bridge == True:
            brname = self.nsname[0]+'bridge'
        #subprocess.call(['sudo','ip','link','add','name',bridges['name'] + 'brdg','type','bridge'])
            subprocess.run(['sudo','ip','link','add','name', brname,'type','bridge'])
            
            subprocess.run(['sudo','ip','link','set','dev', brname,'up'])


    def change_ip(self,new):
        print(f"old ip {self.ip}, new ip{new}")
        self.ip = new
    def add_host(self,host):
        #sudo ip netns exec phost ip route add default via 10.1.1.1
        hname=host.hname
        subnetname=self.nsname
        subprocess.run(["sudo","ip","netns","exec",hname,"ip","route","add","default","via",self.gw])
        print(f"sudo ip netns exec {hname} ip route add default via {self.gw}")
        
        

    def __del__ (self):
        if self.bridge == True:
            subprocess.run(["sudo","ip","link","del",self.nsname])
            print(f"del {self.nsname}")


class Router ():
    def __init__ (self, rname, interfaces):
        self.rname = rname
        print(self.rname)

        subprocess.run(["sudo","ip","netns","add",rname])
        #sudo ip netns exec orouter sysctl -p /etc/sysctl.d/10-ip-forwarding.conf
        subprocess.run(["sudo","ip","netns","exec",rname,"sysctl","-p","/etc/sysctl.d/10-ip-forwarding.conf"])
        
        self.inf = interfaces
        print(self.inf)
        self.links = {}
        #connect interfaces
        for interface in interfaces:
            
            linkname = interface['name']
            print(linkname)
            linkip = interface['ip']
                        
            newlink=link_ns (self.rname,linkname,linkip)
            self.links[linkname]=newlink
            
        print (self.links)
        
    #routing
    #sudo ip netns exec crouter ip route add 10.1.1.0/24 via 10.1.5.2
    def add_net(self,subnetEdge,subnetCore):
        last = calculate_last(subnetCore.ip, subnetCore.cidr)
        print(f"sudo ip netns exec {self.rname} ip route add {subnetEdge.ip}{subnetEdge.cidr} via {last}")
        subprocess.run(["sudo","ip","netns","exec",self.rname,"ip","route","add",subnetEdge.ip+subnetEdge.cidr,"via",last])
        
    
    #sudo ip netns exec prouter ip route add default via 10.1.5.1
    def add_default(self,subnetCore):
        rname = self.rname
        print(f"sudo ip netns exec {self.rname} ip route add default via {subnetCore.gw}")
        subprocess.run(["sudo","ip","netns","exec",rname,"ip","route","add","default","via",subnetCore.gw])
    
    #def __del__ (self):
    #    subprocess.run(["sudo","ip","netns","del",self.rname])

class Host ():
    def __init__(self, hname, interfaces):
        self.hname = hname
        self.inf= interfaces
        first = interfaces[0]
        self.subnet = first['subnets']
        
        self.links = []
        
        subprocess.run (['sudo','ip','netns','add',self.hname])
        
        for interface in interfaces:
            
            linkname = interface['name']
            linkip = interface['ip']
            print(linkname)
            newlink = link_ns(self.hname,linkname,linkip)
            
            self.links.append(newlink)
            print(newlink)
        print (self.links)

# from mark rodriguez        
def configure_nat():
    # sudo ip link add crout2nat type veth peer name nat2crout
    # sudo ip link set crout2nat netns crouter
    subprocess.call(['sudo','ip','link','add','core2nat','type','veth','peer','name','nat2core'])
    subprocess.call(['sudo','ip','link','set','core2nat','netns','core'])

    subprocess.call(['sudo','ip','netns','exec','core','ip','addr','add','10.1.5.17/30','dev','core2nat'])
    subprocess.call(['sudo','ip','netns','exec','core','ip','link','set','dev','core2nat','up'])

    subprocess.call(['sudo','ip','addr','add','10.1.5.18/30','dev','nat2core'])

    subprocess.call(['sudo','ip','addr','add','192.168.90.3/24','dev','pbridge2prouter'])
    subprocess.call(['sudo','ip','addr','add','192.168.90.4/24','dev','pbridge'])

    subprocess.call(['sudo','iptables','-t','nat','-F'])
    subprocess.call(['sudo','iptables','-t','nat','-A','POSTROUTING','-s','10.1.0.0/16','-o','ens3','-j','MASQUERADE']) 
    subprocess.call(['sudo','iptables','-t','filter','-A','FORWARD','-i','ens3','-o','nat2core','-j','ACCEPT'])  
    subprocess.call(['sudo','iptables','-t','filter','-A','FORWARD','-o','ens3','-i','nat2core','-j','ACCEPT'])
    subprocess.call(['sudo','ip','route','add','10.1.0.0/16','via','10.1.5.17']) 

    subprocess.call(['sudo','iptables','-t','filter','-A','FORWARD','-i','ens3','-o','nat2crout','-j','ACCEPT'])  
    subprocess.call(['sudo','iptables','-t','filter','-A','FORWARD','-o','ens3','-i','nat2crout','-j','ACCEPT'])
    subprocess.call(['sudo','ip','netns','exec','core','ip','route','add','default','via','10.1.5.18']) 



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
    print(sholder)
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
        new_host = Host (hname = host['name'], interfaces = host['interfaces'])
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
    print("purple add to subnet")
    sholder['yellow'].add_host(yellohost)
    sholder.get('white').add_host(whitehost)
    sholder.get('orange').add_host(oranghost)

    #add route to core
    rholder.get('core').add_net(sholder.get('purple'),sholder.get('purple-core'))
    rholder.get('core').add_net(sholder.get('orange'),sholder.get('orange-core'))
    rholder.get('core').add_net(sholder.get('yellow'),sholder.get('yellow-core'))
    rholder.get('core').add_net(sholder.get('white'),sholder.get('white-core'))
    #add default from core subnets

    prouter=holder['prouter']
    prouter.add_default(sholder.get('purple-core'))
    orouter=rholder['orouter']
    orouter.add_default(sholder.get('orange-core'))
    yrouter=rholder['yrouter']
    yrouter.add_default(sholder.get('yellow-core'))
    wrouter=rholder['wrouter']
    wrouter.add_default(sholder.get('white-core'))

# need to add default specific for core

# deploy nat
    configure_nat()

if __name__ == "__main__":
    main()
