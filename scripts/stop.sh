#!/bin/sh

/usr/bin/tmux send -t minecraft save-all ENTER
/usr/bin/tmux send -t minecraft stop ENTER
echo "Killing minecraft session"
/usr/bin/tmux kill-session -t minecraft
