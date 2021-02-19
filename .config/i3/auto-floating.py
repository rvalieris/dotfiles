#!/usr/bin/env python3
import datetime
import re
import os
import i3ipc
import subprocess
import Xlib
import Xlib.display

i3 = i3ipc.Connection()
cache = {}
config = os.path.expanduser("~/.cache/i3-auto-floating.config")
ignore_window = {}

#dpy = Xlib.display.Display()
#DIALOG_ATOM = dpy.get_atom('_NET_WM_WINDOW_TYPE_DIALOG')
#WIN_TYPE_ATOM = dpy.get_atom('_NET_WM_WINDOW_TYPE')
#win = dpy.create_resource_object('window', event.container.window)
#win_types = win.get_full_property(WIN_TYPE_ATOM, Xlib.X.AnyPropertyType)

def read_config():
	if not os.path.exists(config): return
	fd = open(config)
	dtnow = datetime.datetime.now()
	dtprev = datetime.datetime.now()
	for l in fd:
		if l.startswith('#'):
			if 'datetime' in l:
				m = re.search(' = (.+)', l)
				if m:
					dtprev = datetime.datetime.strptime(m.groups()[0], '%Y-%m-%d %H:%M:%S.%f')
			elif 'ignore_window' in l:
				if (dtnow - dtprev) < datetime.timedelta(hours=1):
					m = re.search(' = (\S+)', l)
					if m:
						wids = m.groups()[0].split(',')
						for i in wids:
							ignore_window[int(i)] = True
		elif l.startswith('for_window'):
			v = ()
			for ks in ['class','instance','window_role']:
				m = re.search(ks+'="\^(.+?)\$"', l)
				if m:
					v += (m.groups()[0],)
				else:
					v += ("",)
			cache[v] = True

def get_key(container):
	c = container.window_class
	if c is None: c = ""
	i = container.window_instance
	if i is None: i = ""
	r = container.window_role
	if r is None: r = ""
	return (c,i,r)

def write_config():
	fd = open(config+'.new', 'w')
	fd.write('# datetime = '+str(datetime.datetime.now())+'\n')
	fd.write('# ignore_window = '+','.join(map(str,ignore_window.keys()))+'\n')
	for k in cache.keys():
		c, i, r = k
		txt = 'for_window ['
		txt += 'class="^{}$" '.format(c)
		txt += 'instance="^{}$" '.format(i)
		if r != '': txt += 'window_role="^{}$" '.format(r)
		txt += '] floating enable'
		fd.write(txt+'\n')
	fd.close()
	os.rename(config+'.new', config)

def i3_refresh():
	subprocess.run(['yadm','alt'], stdout=subprocess.PIPE)
	i3.command('reload')

def on_window(i3, event):
	if event.change == 'new':
		k = get_key(event.container)
		if (event.container.floating == 'user_on' or event.container.floating == 'auto_on') and k not in cache:
			# ignore floating by default
			ignore_window[event.container.window] = True
			write_config()

	if event.change == 'close':
		if event.container.window in ignore_window:
			del ignore_window[event.container.window]
			write_config()
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

