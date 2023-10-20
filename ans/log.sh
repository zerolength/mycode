net.bridge.bridge-nf-call-iptables = 0
'net.ipv4.ip_forward = 1
 net.ipv6.conf.default.forwarding = 1
 net.ipv6.conf.all.forwarding = 1' | sudo tee /etc/sysctl.d/10-ip-forwarding.conf
bridge name	bridge id		STP enabled	interfaces
obridge		8000.d6f18f0281bc	no		
pbridge		8000.f6996d8c121e	no		
wbridge		8000.2a8a5907a9c1	no		
ybridge		8000.0a71d7b07448	no		
net.ipv4.ip_forward = 1
net.ipv6.conf.default.forwarding = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.ip_forward = 1
net.ipv6.conf.default.forwarding = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.ip_forward = 1
net.ipv6.conf.default.forwarding = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.ip_forward = 1
net.ipv6.conf.default.forwarding = 1
net.ipv6.conf.all.forwarding = 1
net.ipv4.ip_forward = 1
net.ipv6.conf.default.forwarding = 1
net.ipv6.conf.all.forwarding = 1
wrouter (id: 10)
yrouter (id: 9)
orouter (id: 8)
prouter (id: 6)
core (id: 7)
whost
yhost
ohost (id: 12)
phost (id: 11)
10.1.1.0
purple
True
br purple
10.1.5.0
purple-core
False
10.1.4.0
orange
True
br orange
10.1.5.12
orange-core
False
10.1.2.0
yellow
True
br yellow
10.1.5.4
yellow-core
False
10.1.3.0
white
True
br white
10.1.5.8
white-core
False
Showing up bridges
core
[{'name': 'to-purple-core', 'ip': '10.1.5.1', 'subnet': ''}, {'name': 'to-orange-core', 'ip': '10.1.5.13', 'subnet': ''}, {'name': 'to-yellow-core', 'ip': '10.1.5.5', 'subnet': ''}, {'name': 'to-white-core', 'ip': '10.1.5.9', 'subnet': ''}, {'name': 'loopback', 'ip': '', 'subnet': ''}]
{'name': 'to-purple-core', 'ip': '10.1.5.1', 'subnet': ''}
to-purple-core
split to-purple-core None, purple-core
core2urouter
{'name': 'to-orange-core', 'ip': '10.1.5.13', 'subnet': ''}
to-orange-core
split to-orange-core None, orange-core
core2rrouter
{'name': 'to-yellow-core', 'ip': '10.1.5.5', 'subnet': ''}
to-yellow-core
split to-yellow-core None, yellow-core
core2erouter
{'name': 'to-white-core', 'ip': '10.1.5.9', 'subnet': ''}
to-white-core
split to-white-core None, white-core
core2hrouter
{'name': 'loopback', 'ip': '', 'subnet': ''}
loopback
loopback
{'to-purple-core': 'core2urouter', 'to-orange-core': 'core2rrouter', 'to-yellow-core': 'core2erouter', 'to-white-core': 'core2hrouter', 'loopback': 'loopback'}
prouter
[{'name': 'prouter-to-core', 'ip': '10.1.5.2', 'subnet': ''}, {'name': 'prouter2pbridge', 'ip': '10.1.1.1', 'subnet': ''}]
{'name': 'prouter-to-core', 'ip': '10.1.5.2', 'subnet': ''}
prouter-to-core
split prouter-to-core prouter, core
prout2core prouter core
prout2core
{'name': 'prouter2pbridge', 'ip': '10.1.1.1', 'subnet': ''}
prouter2pbridge
split prouter2pbridge prouter, pbridge
prout2pbridge prouter pbridge
prout2pbridge
{'prouter-to-core': 'prout2core', 'prouter2pbridge': 'prout2pbridge'}
orouter
[{'name': 'orouter-to-core', 'ip': '10.1.5.14', 'subnet': ''}, {'name': 'orouter2obridge', 'ip': '10.1.4.1', 'subnet': ''}]
{'name': 'orouter-to-core', 'ip': '10.1.5.14', 'subnet': ''}
orouter-to-core
split orouter-to-core orouter, core
orout2core orouter core
orout2core
{'name': 'orouter2obridge', 'ip': '10.1.4.1', 'subnet': ''}
orouter2obridge
split orouter2obridge orouter, obridge
orout2obridge orouter obridge
orout2obridge
{'orouter-to-core': 'orout2core', 'orouter2obridge': 'orout2obridge'}
yrouter
[{'name': 'yrouter-to-core', 'ip': '10.1.5.9', 'subnet': ''}, {'name': 'yrouter2ybridge', 'ip': '10.1.2.1', 'subnet': ''}]
{'name': 'yrouter-to-core', 'ip': '10.1.5.9', 'subnet': ''}
yrouter-to-core
split yrouter-to-core yrouter, core
yrout2core yrouter core
yrout2core
{'name': 'yrouter2ybridge', 'ip': '10.1.2.1', 'subnet': ''}
yrouter2ybridge
split yrouter2ybridge yrouter, ybridge
yrout2ybridge yrouter ybridge
yrout2ybridge
{'yrouter-to-core': 'yrout2core', 'yrouter2ybridge': 'yrout2ybridge'}
wrouter
[{'name': 'wrouter-to-core', 'ip': '10.1.5.10', 'subnet': ''}, {'name': 'wrouter2wbridge', 'ip': '10.1.3.21', 'subnet': ''}]
{'name': 'wrouter-to-core', 'ip': '10.1.5.10', 'subnet': ''}
wrouter-to-core
split wrouter-to-core wrouter, core
wrout2core wrouter core
wrout2core
{'name': 'wrouter2wbridge', 'ip': '10.1.3.21', 'subnet': ''}
wrouter2wbridge
split wrouter2wbridge wrouter, wbridge
wrout2wbridge wrouter wbridge
wrout2wbridge
{'wrouter-to-core': 'wrout2core', 'wrouter2wbridge': 'wrout2wbridge'}
{'core': <__main__.Router object at 0x7f68def88790>, 'prouter': <__main__.Router object at 0x7f68def88160>, 'orouter': <__main__.Router object at 0x7f68def887f0>, 'yrouter': <__main__.Router object at 0x7f68def881f0>, 'wrouter': <__main__.Router object at 0x7f68def887c0>}
Showing Created Namespaces...
split wrouter-to-core wrouter, core
wrout2core wrouter core
wrout2core
split wrouter2wbridge wrouter, wbridge
wrout2wbridge wrouter wbridge
wrout2wbridge
['wrout2core', 'wrout2wbridge']
split wrouter-to-core wrouter, core
wrout2core wrouter core
wrout2core
split wrouter2wbridge wrouter, wbridge
wrout2wbridge wrouter wbridge
wrout2wbridge
['wrout2core', 'wrout2wbridge']
split wrouter-to-core wrouter, core
wrout2core wrouter core
wrout2core
split wrouter2wbridge wrouter, wbridge
wrout2wbridge wrouter wbridge
wrout2wbridge
['wrout2core', 'wrout2wbridge']
split wrouter-to-core wrouter, core
wrout2core wrouter core
wrout2core
split wrouter2wbridge wrouter, wbridge
wrout2wbridge wrouter wbridge
wrout2wbridge
['wrout2core', 'wrout2wbridge']
{'phost': <__main__.Host object at 0x7f68def88250>, 'ohost': <__main__.Host object at 0x7f68def88610>, 'yhost': <__main__.Host object at 0x7f68def88460>, 'whost': <__main__.Host object at 0x7f68def88700>}
Press Enter to continue...you can check if netns is updel purple
del orange
del yellow
del white
