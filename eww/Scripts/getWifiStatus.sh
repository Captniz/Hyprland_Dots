networkData=$(nmcli d status | jc --nmcli )
connectionState="$(echo $networkData | jq -r '.[] | select(.type == "wifi") | .state')"

if [ "$connectionState" == "connected" ]; then
    echo "$(echo $networkData | jq -r '.[] | select(.type == "wifi") | .connection')"
else
    echo "No connection"
fi