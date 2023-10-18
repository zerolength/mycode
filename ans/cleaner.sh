#!/bin/bash

# Get a list of all network namespaces
namespaces=$(ip netns list)

# Iterate through the list and delete each namespace
for namespace in $namespaces; do
    ip netns delete $namespace
    echo "Deleted namespace: $namespace"
done

echo "All network namespaces have been removed."

