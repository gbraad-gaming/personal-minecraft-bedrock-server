#!/bin/sh

FILE="$HOME/server.properties"
BASE="/opt/minecraft/"

if [ ! -e "$FILE" ]; then
    echo "Minecraft's server.properties does not exist. Copying from /opt/minecraft/"
    cp -R $BASE/behavior_packs $BASE/config $BASE/definitions $BASE/resource_packs $BASE/server.properties $BASE/allowlist.json $BASE/permissions.json $BASE/profanity_filter.wlist $HOME
fi

/usr/bin/tmux new-session -s minecraft -d
tmux send -t minecraft "LD_LIBRARY_PATH=. /opt/minecraft/bedrock_server" ENTER
tmux send -t minecraft "gamerule showcoordinates true" ENTER
tmux send -t minecraft "gamerule keepInventory true" ENTER
