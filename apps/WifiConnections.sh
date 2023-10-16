#!/bin/sh

dunstify "  Searching for networks..." -r 2

#Trovo la lista di connessioni
list=$(nmcli -f ssid,rate,bars d wifi list --rescan yes)

#Mostro il menu e trovo la selezione dell'utente
selection=$(echo "$list" | sed '1d' | rofi -dmenu -i -l 20 -p 'Select a network ' | awk '{print $1}')

if [ "$selection" = "" ]; then
    return
fi

#Controllo se la connessione è autoconnessa
autoconnect=$(nmcli -f 'NAME,AUTOCONNECT' con show | grep "$selection" | grep -c "yes")

#Se è autoconnessa la connetto, altrimenti chiedo la password
if [ "$autoconnect" = "1" ]; then
    dunstify "  Connecting..." -r 2
    nmcli d disconnect wlp0s20f3
    nmcli d wifi connect "$selection"
else
    password=$(echo "" | rofi -dmenu -i -p 'Password ')
    nmcli d disconnect wlp0s20f3
    nmcli d wifi connect "$selection" password "$password"
fi

#Controllo se la connessione è andata a buon fine
sleep 5
state=$(nmcli -t device show wlp0s20f3| grep "GENERAL.CONNECTION:" | grep -c "$selection")

if [ "$state" = "1" ]; then
        dunstify "  Connected succesfully!" -r 2
    else
        dunstify -u critical "󰚽  Could not connect to network" -r 2
fi

return