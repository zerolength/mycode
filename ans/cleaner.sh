#!/bin/bash

# Get a list of all network namespaces
namespaces=$(ip netns list)

# Iterate through the list and delete each namespace
for namespace in $namespaces; do
    ip netns delete $namespace
    echo "Deleted namespace: $namespace"
done


# Specify the list of link names to keep (space-separated)
links_to_keep="lo ens3 docker0 vethb132fcc@if4 br-95097e7166ed veth39916af@if27 veth4b7e70c@if29 vethf36df0a@if31 veth62152f6@if33 vethb138804@if35"

# Get a list of all network links
all_links=$(ip link show | awk -F ": " '{print $2}')

Iterate through all links
for link in $all_links; do
    # Check if the current link is in the list of links to keep
    if [[ $links_to_keep == *"$link"* ]]; then
        echo "Keeping link: $link"
    else
        # Delete the link
        sudo ip link delete "$link"
        echo "Deleted link: $link"
    fi
done

# Get a list of all network links
all_links=$(ip -o link show | awk -F ": " '{print $2}' | awk -F "@" '{print $1}')

# Iterate through all links and delete each one
for link in $all_links; do
    ip link delete "$link"
    echo "Deleted link: $link"
done

echo "All network links have been removed."

echo "All network links have been removed."


echo "Network links have been cleaned."





echo "All network namespaces have been removed."

