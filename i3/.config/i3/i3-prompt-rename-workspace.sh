#!/bin/sh
set -e
CUR=$(i3-msg -t get_workspaces | jq -r '.[]|select(.focused)|.name')
NEW="$(echo $CUR | rofi -dmenu -lines 1 -hide-scrollbar -p "Rename workspace")"
if [ $? -eq 0 ]
then
	i3-msg "rename workspace to \"$NEW\""
fi
