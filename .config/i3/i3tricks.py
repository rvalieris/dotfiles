#!/usr/bin/env python3
import i3ipc
import sys
import subprocess
import os
i3 = i3ipc.Connection()

def list_workspaces():
	print('\n'.join(map(lambda i: i.name, i3.get_workspaces())))

def prompt_rename_workspace():
	cur, = list(filter(lambda i: i.focused, i3.get_workspaces()))
	new = subprocess.run(['rofi','-dmenu','-l','0','-hide-scrollbar','-p',
		"Rename workspace (current "+cur.name+")"], stdout=subprocess.PIPE).stdout
	new = new.decode().rstrip()
	if len(new) > 0:
		i3.command('rename workspace to '+new)

def prompt_move_container():
	cur, = list(filter(lambda i: i.focused, i3.get_workspaces()))
	new = subprocess.check_output(['rofi','-dmenu','-l','0','-hide-scrollbar','-p',
		"Move container to (current "+cur.name+")"])
	new = new.decode().rstrip()
	if len(new) > 0:
		i3.command('move container to workspace '+new)

def prompt_select_workspace():
	ws = list(map(lambda i: i.name, i3.get_workspaces()))
	p = subprocess.Popen(['rofi','-dmenu','-p','workspace'],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = p.communicate(input="\n".join(ws).encode())
	out = out.decode().rstrip()
	i3.command('workspace '+out)

def prompt_swap_window():
	out = subprocess.check_output(['rofi','-show','window','-run-command','echo {cmd}'])
	out = out.decode().rstrip()
	if len(out) > 0:
		i3.command('workspace '+out)

def swap_workspaces():
	ws_names = list(map(lambda i: i.name, filter(lambda i: i.visible, i3.get_workspaces())))
	for w in i3.get_tree().workspaces():
		if w.name in ws_names:
			w.command('move workspace to output right')
			w.command('focus')

if len(sys.argv) > 1:
	locals()[sys.argv[1]]()
else:
	print("\n".join(dict(filter(lambda i: callable(i[1]), locals().items())).keys()))

