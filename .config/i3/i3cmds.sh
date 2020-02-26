#!/bin/bash
set -e

sub_list_workspaces() {
	i3-msg -t get_workspaces | jq -r '.[].name'
}

sub_prompt_rename_workspace() {
	CUR=$(i3-msg -t get_workspaces | jq -r '.[]|select(.focused)|.name')
	if NEW="$(rofi -dmenu -lines 0 -hide-scrollbar -p "Rename workspace (current $CUR)")"; then
		i3-msg "rename workspace to \"$NEW\""
	fi
}

sub_get_window_title() {
	CUR_ID=$(xprop -root | grep -Po '_NET_ACTIVE_WINDOW\(.*?\K0x.*')
	TITLE=$(xprop -id "$CUR_ID" | grep -Po '_NET_WM_NAME.*?"\K.*?(?=")')
	echo "$TITLE"
}

sub_set_terminal_title() {
	echo -ne "\033]0;${1}\007"
}

sub_prompt_select_workspace() {
	if SEL="$(i3-msg -t get_workspaces | jq -r '.[].name' | rofi -dmenu -lines 10 -p "Select workspace")"; then
		i3-msg "workspace $SEL"
	fi
}

sub_prompt_i3_command() {
	if CMD="$(grep '^bindsym' ~/.config/i3/config | perl -wpe 's/\s+/\|/;s/\s+/\|/' | column -s'|' -t | rofi -dmenu -lines 15 -width 90 -p 'i3-msg' | perl -wpe 's/^bindsym\s*\S+\s*//')"; then
		i3-msg "$CMD"
	fi
}

subcmd=$1
if [ "${subcmd}" == "" ]; then
	compgen -A function | sed 's/sub_//'
	exit 1
fi
shift
sub_"${subcmd}" "$@"
