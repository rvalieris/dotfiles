#!/usr/bin/env python3
import i3ipc
import sys
import subprocess
i3 = i3ipc.Connection()

def list_workspaces():
	print('\n'.join(map(lambda i: i.name, i3.get_workspaces())))

def prompt_rename_workspace():
	cur, = list(filter(lambda i: i.focused, i3.get_workspaces()))
	new = subprocess.check_output(['rofi','-dmenu','-lines','0','-hide-scrollbar','-p',
		"Rename workspace (current "+cur.name+")"])
	new = new.decode().rstrip()
	if len(new) > 0:
		i3.command('rename workspace to '+new)

def prompt_select_workspace():
	ws = list(map(lambda i: i.name, i3.get_workspaces()))
	p = subprocess.Popen(['rofi','-dmenu','-lines','10','-p','workspace'],
		stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = p.communicate(input="\n".join(ws).encode())
	out = out.decode().rstrip()
	i3.command('workspace '+out)

def swap_workspaces():
	ws = i3.get_workspaces()
	ws = list(filter(lambda i: i.visible, ws))
	for i,w in enumerate(ws):
		i3.command('workspace --no-auto-back-and-forth '+w.name)
		i3.command('move workspace to output right')

if len(sys.argv) > 1:
	locals()[sys.argv[1]]()
else:
	print("\n".join(dict(filter(lambda i: callable(i[1]), locals().items())).keys()))

