#!/bin/sh
set -e
CUR=$(i3-msg -t get_workspaces | jq -r '.[]|select(.focused)|.name')
NEW="$(rofi -dmenu -lines 0 -hide-scrollbar -p "Rename workspace (current $CUR)")"
if [ $? -eq 0 ]
then
	i3-msg "rename workspace to \"$NEW\""
fi
