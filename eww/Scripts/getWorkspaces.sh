#!/bin/sh

# Get the list of workspaces
ws=()

# for of 10
for i in {1..10}
do
    ws[$i]="\"\""
done

while read -r line
do
    ws[$line]="\"\""
done < <(hyprctl workspaces -j | jq -r '.[] | .name')

ws[$(hyprctl monitors -j | jq -r '.[] | .activeWorkspace | .name')]="\"\""

echo "[$(echo ${ws[@]} | sed 's/ /,/g')]"