#!/usr/bin/env python3
import re
import os
import i3ipc
import subprocess
import Xlib
import Xlib.display

i3 = i3ipc.Connection(auto_reconnect=True)
cache = {}
config = os.path.expanduser("~/.cache/i3-auto-floating.config")
to_ignore = {}

#dpy = Xlib.display.Display()
#DIALOG_ATOM = dpy.get_atom('_NET_WM_WINDOW_TYPE_DIALOG')
#WIN_TYPE_ATOM = dpy.get_atom('_NET_WM_WINDOW_TYPE')
#win = dpy.create_resource_object('window', event.container.window)
#win_types = win.get_full_property(WIN_TYPE_ATOM, Xlib.X.AnyPropertyType)

def read_config():
	fd = open(config)
	for l in fd:
		m = re.search('class="\^(.+?)\$"\s+instance="\^(.+?)\$"', l)
		cache[m.groups()] = True

def get_key(container):
	c = container.window_class
	if c is None: c = ""
	i = container.window_instance
	if i is None: i = ""
	return (c,i)

def write_config():
	fd = open(config, 'w')
	for k in cache.keys():
		c, i = k
		fd.write('for_window [class="^{}$" instance="^{}$"] floating enable\n'.format(c,i))
	fd.close()

def i3_refresh():
	subprocess.run(['yadm','alt'], stdout=subprocess.PIPE)
	i3.command('reload')

def on_window(i3, event):
	if event.change == 'new':
		k = get_key(event.container)
		if event.container.floating == 'user_on' and k not in cache:
			# ignore floating by default
			to_ignore[event.container.window] = True

	if event.change == 'close':
		if event.container.window in to_ignore:
			del to_ignore[event.container.window]
			return

		k = get_key(event.container)
		if event.container.floating == 'user_on' and k not in cache:
			cache[k] = True
			write_config()
			i3_refresh()
		if event.container.floating == 'user_off' and k in cache:
			del cache[k]
			write_config()
			i3_refresh()

read_config()
i3_refresh()
i3.on(i3ipc.Event.WINDOW, on_window)
i3.main()

