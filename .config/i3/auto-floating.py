#!/usr/bin/env python3
import os
import shelve
import i3ipc
import subprocess
import Xlib
import Xlib.display

i3 = i3ipc.Connection(auto_reconnect=True)
cache = shelve.open(os.path.expanduser('~/.cache/i3-auto-floating'))
config = os.path.expanduser("~/.cache/i3-auto-floating.config")
to_ignore = {}

dpy = Xlib.display.Display()
DIALOG_ATOM = dpy.get_atom('_NET_WM_WINDOW_TYPE_DIALOG')
WIN_TYPE_ATOM = dpy.get_atom('_NET_WM_WINDOW_TYPE')

def get_key(container):
	c = container.window_class
	if c is None: c = ""
	i = container.window_instance
	if i is None: i = ""
	return '\x00'.join([c,i])

def split_key(key):
	return key.split('\x00')

def write_config():
	fd = open(config, 'w')
	for k in cache.keys():
		c, i = split_key(k)
		fd.write('for_window [class="^{}$" instance="^{}$"] floating enable\n'.format(c,i))
	fd.close()
	subprocess.run(['yadm','alt'], stdout=subprocess.PIPE)
	subprocess.run(['i3-msg','-q','reload'])

def on_window(i3, event):
	if event.change == 'new':
		win = dpy.create_resource_object('window', event.container.window)
		win_types = win.get_full_property(WIN_TYPE_ATOM, Xlib.X.AnyPropertyType)
		if win_types is not None:
			win_types = list(win_types.value)
			if DIALOG_ATOM in win_types:
				# DIALOG is already floating by default
				to_ignore[event.container.window] = True

	if event.change == 'close':
		if event.container.window in to_ignore:
			del to_ignore[event.container.window]
			return

		k = get_key(event.container)
		if event.container.floating == 'user_on' and k not in cache:
			cache[k] = True
			cache.sync()
			write_config()
		if event.container.floating == 'user_off' and k in cache:
			del cache[k]
			cache.sync()
			write_config()

write_config()
i3.on(i3ipc.Event.WINDOW, on_window)
i3.main()
