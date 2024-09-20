import json
import subprocess

def cmd(msg_type=None, msg=''):
	if msg_type is None:
		return json.loads(subprocess.check_output(['swaymsg', '-r', msg]))
	else:
		return json.loads(subprocess.check_output(['swaymsg', '-r', '-t', msg_type, msg]))

def get_outputs():
	return cmd(msg_type='get_outputs')

def get_workspaces():
	return cmd(msg_type='get_workspaces')

def get_focused_workspaces():
	return list(filter(lambda ws: ws['focused'], get_workspaces()))

def get_headless_outputs():
	return list(filter(lambda d: 'HEADLESS' in d['name'], get_outputs()))

