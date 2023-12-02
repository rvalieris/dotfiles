#!/usr/bin/env python3
import sys
import json
import os
import subprocess

sys.path.append(os.path.expanduser('~/.config/sway'))
import sway_ipc

BG_CONFIG = os.path.expanduser('~/.cache/swaybg')
LOCK_CONFIG = os.path.expanduser('~/.cache/swaylock')

def _rofi_prompt(prompt):
	p = subprocess.run(['rofi', '-dmenu', '-l', '0',
		'-hide-scrollbar', '-p', prompt],
		stdout=subprocess.PIPE, input='')
	if p.returncode != 0:
		return None
	return p.stdout.decode().rstrip()

def prompt_rename_workspace():
	data = sway_ipc.get_workspaces()
	cur, = list(filter(lambda wb: wb['focused'], data))
	new = _rofi_prompt(f"Rename workspace (current {cur['name']})")
	if new is not None and len(new) > 0:
		sway_ipc.cmd(msg=f'rename workspace to {new}')

def prompt_move_container():
	data = sway_ipc.get_workspaces()
	cur, = list(filter(lambda wb: wb['focused'], data))
	new = _rofi_prompt(f"Move container to (current {cur['name']})")
	if new is not None and len(new) > 0:
		sway_ipc.cmd(msg=f'move container to workspace {new}')

def swap_workspaces():
	data = sway_ipc.get_workspaces()
	wss = list(filter(lambda w: w['visible'], data))
	for w in wss:
		if len(w['focus']) > 0:
			sway_ipc.cmd(msg=f'''[con_id="{w['focus'][0]}"] move workspace to output right''')

def _get_bg_file(out):
	return os.path.expanduser(f'~/.cache/wallpaper-{out}.png')

def reload_bg():
	fh1 = open(BG_CONFIG, 'wt')
	fh2 = open(LOCK_CONFIG, 'wt')
	for d in sway_ipc.get_outputs():
		of = _get_bg_file(d['name'])
		fh1.write(f"output {d['name']} bg {of} fill\n")
		fh2.write(f"image={d['name']}:{of}\n")
	fh1.close()
	fh2.close()
	txt = open(BG_CONFIG).read()
	sway_ipc.cmd(msg=txt)

def lock_session():
	os.execvp('swaylock', ['swaylock', '-f', '-F', '-C', LOCK_CONFIG])

if __name__ == '__main__':
	if len(sys.argv) > 1:
		locals()[sys.argv[1]]()
	else:
		print("\n".join(dict(filter(lambda i: not i[0].startswith('_') and callable(i[1]), locals().items())).keys()))

