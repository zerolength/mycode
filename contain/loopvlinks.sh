#!/bin/bash

# Define an array of namespace names
namespaces=("phost" "prouter" "yhost" "yrouter" "whost" "wrouter" "ohost" "orouter" "crouter")

# Iterate through the namespaces and bridge names
for i in "${!namespaces[@]}"; do
  ns1="${namespaces[i]}2"
  ns2=""
  if [ "$i" -eq 8 ]; then
    ns2="crout2"
  else
    ns2="${namespaces[i]}2"
  fi
  
  # Connect the first end of the veth pair to the current namespace
  sudo ip link add "${ns1}${ns2}" type veth peer name "${ns2}${ns1}"
  sudo ip link set "${ns1}${ns2}" netns "${namespaces[i]}"
  sudo ip link set dev "${ns2}${ns1}" master "${ns1%2*}bridge"
  sudo ip link set dev "${ns2}${ns1}" up
done

# Connect the last set (nat and crouter) (13)
sudo ip link add crout2nat type veth peer name nat2crout
sudo ip link set crout2nat netns crouter
# Leave the other end of the veth DANGLE in the root namespace.

# Verification
ip link

