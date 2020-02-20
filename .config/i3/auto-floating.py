#!/usr/bin/env python3
import os
import shelve
import i3ipc

i3 = i3ipc.Connection()
cache = shelve.open(os.path.expanduser('~/.cache/i3-auto-floating'))

def on_window(i3, event):
	if event.change == 'new':
		# new window apply floating if any
		m = event.container.window_class + '|' + event.container.window_instance
		if m in cache:
			if cache[m]: event.container.command('floating enable')
			else: event.container.command('floating disable')
			#print(event.change, m, cache[m])
		#else:
		#	print(event.change, m)
	elif event.change == 'close':
		# closed window save floating mode
		m = event.container.window_class + '|' + event.container.window_instance
		cache[m] = event.container.floating == 'user_on'
		cache.sync()
		#print(event.change, m, cache[m])

i3.on(i3ipc.Event.WINDOW, on_window)
i3.main()
