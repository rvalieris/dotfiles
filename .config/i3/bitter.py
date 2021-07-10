#!/usr/bin/env python

import re
import os
import sys
import json
import glob
import html
import shutil
import signal
import datetime
import importlib
import threading
import functools
import subprocess
from collections import OrderedDict

# always flush
print = functools.partial(print, flush=True)

icon_font = sys.argv[1]

def pango(txt):
	return '<span font="%s">%s</span>'%(icon_font,txt)

class Module(object):
	IMPORTS = []

	def __new__(cls, *args):
		try:
			for m in cls.IMPORTS:
				globals()[m] = importlib.import_module(m)
			return super(Module, cls).__new__(cls)
		except ModuleNotFoundError as e:
			print(sys.argv[0]+': '+cls.__name__+' disabled: ModuleNotFoundError: '+e.name, file=sys.stderr)
			return None
		except Exception as e:
			print(e, file=sys.stderr)
			return None

	def name(self): return type(self).__name__
	def get_data(self): return {'full_text': '<empty>', 'name':self.name(), 'markup': 'pango' }
	def on_click(self,data): pass

class LoadAvg(Module):
	icon = pango('🔥')
	n_cores = os.cpu_count()
	def get_data(self):
		t0, _, _ = os.getloadavg()
		d = super().get_data()
		d.update({'full_text': "{:s} {:.2f}".format(self.icon,t0), 'urgent': t0 > self.n_cores })
		return d

class Datetime(Module):
	icon1 = pango('📅')
	icon2 = pango('⌚')
	def get_data(self):
		txt = datetime.datetime.now().strftime(self.icon1+' %b %Y, %A %d '+self.icon2+' %H:%M:%S')
		d = super().get_data()
		d.update({'full_text': txt })
		return d

	def on_click(self,data):
		p = subprocess.run(['cal'],capture_output=True)
		subprocess.run(['notify-send',p.stdout.decode()])

class Volume(Module):
	IMPORTS = ['pulsectl']
	icon = pango('🔊')
	icon2 = pango('🔈')
	increment = 1/100
	pct = 0
	dunstify = None
	sink_name = ''

	def __init__(self, wakeup):
		self.wakeup = wakeup
		self.pulse = pulsectl.Pulse(threading_lock=True)
		self.start_pulse_thread()
		self.dunstify = shutil.which('dunstify')

	def notify(self, msg):
		subprocess.run([self.dunstify,'-r',str(os.getpid()),msg])

	def get_data(self):
		d = super().get_data()
		sink = self.get_sink()
		if sink is None:
			d.update({'full_text': 'no sink'})
			return d

		pct = round(100 * self.pulse.volume_get_all_chans(sink))
		if self.dunstify:
			if self.pct != pct:
				self.notify('Volume {:d}%'.format(pct))
				self.pct = pct
			if self.sink_name != sink.name:
				self.notify('Sink {}'.format(sink.name))
				self.sink_name = sink.name
		if sink.mute: t = self.icon2+' mute'
		else: t = '{:s} {:d}%'.format(self.icon,pct)
		d.update({'full_text': t })
		return d

	def get_sink(self):
		try:
			return self.pulse.get_sink_by_name('@DEFAULT_SINK@')
		except pulsectl.pulsectl.PulseIndexError:
			return None

	def on_click(self,data):
		sink = self.get_sink()
		if sink is None: return

		if data['button'] == 2: # open pavucontrol
			subprocess.Popen(['i3-msg','-q','exec','pavucontrol'])
		if data['button'] == 3: # toggle mute
			self.pulse.mute(sink, not sink.mute)
		if data['button'] == 4: # increase vol
			self.pulse.volume_change_all_chans(sink, self.increment)
		if data['button'] == 5: # decrease vol
			self.pulse.volume_change_all_chans(sink, -self.increment)

	def start_pulse_thread(self):
		self.events_t = threading.Thread(target=self.event_watcher,daemon=True)
		self.events_t.start()

	def event_watcher(self):
		self.pulse2 = pulsectl.Pulse(threading_lock=True)
		self.pulse2.event_mask_set('all')
		self.pulse2.event_callback_set(lambda ev: self.wakeup.set())
		self.pulse2.event_listen()

class Battery(Module):
	icon = pango('⚡')
	icon2 = pango('🔌')
	get_pct = re.compile(r'(\d+)%')
	get_chr_time = re.compile(r'(\d+:\d+:\d+)')
	critical = 20

	def __new__(cls, *args):
		if shutil.which('acpi') is None: return None
		p = subprocess.run(['acpi','-b'],stdout=subprocess.PIPE)
		if len(p.stdout) == 0: return None
		return super(Battery,cls).__new__(cls)

	def get_data(self):
		p = subprocess.run(['acpi','-b'],stdout=subprocess.PIPE)
		txt = p.stdout
		if len(txt) == 0: return {}
		txt = txt.decode()
		pct = float(self.get_pct.search(txt).group(1))
		icon2 = ''
		if txt.find('Charging') >= 0:
			icon2 = self.icon2
			t2 = self.get_chr_time.search(txt)
			if t2: icon2 += t2.group(0)
		d = super().get_data()
		d.update({'full_text': "{:s} {:.0f}% {:s}".format(self.icon,pct,icon2), 'urgent': pct < self.critical })
		return d

class Temperature(Module):
	icon = pango('🌡')
	critical = 80

	@staticmethod
	def find_thermal_zone():
		zones = glob.glob("/sys/devices/virtual/thermal/thermal_zone*")
		for z in zones:
			if re.search("pkg_temp",open(z+"/type").read()):
				return z+"/temp"
		return None

	def __new__(cls, *args):
		if Temperature.find_thermal_zone() is not None:
			return super(Temperature,cls).__new__(cls)
		else:
			print(sys.argv[0]+': Temperature disabled: cant find a valid thermal_zone.', file=sys.stderr)
			return None

	def __init__(self):
		self.thermal_zone = Temperature.find_thermal_zone()

	def get_data(self):
		if os.path.isfile(self.thermal_zone):
			temp = int(open(self.thermal_zone).read().rstrip())/1000
			d = super().get_data()
			d.update({'full_text': "{:s}{:.1f}°C".format(self.icon,temp), 'urgent': temp > self.critical })
			return d
		else:
			return {}

class WindowTitle(Module):
	IMPORTS = ['i3ipc']
	icon = pango('💠')
	max_short_text = 45

	def __init__(self, wakeup):
		self.wakeup = wakeup
		self.title = ''
		self.events_t = threading.Thread(target=self.event_watcher,daemon=True)
		self.events_t.start()

	def get_data(self):
		d = super().get_data()
		if self.title is not None and len(self.title) > 0:
			d.update({'full_text': self.icon+' '+html.escape(self.title) })
			if len(self.title) > self.max_short_text:
				d.update({'short_text': self.icon+' '+html.escape(self.title[:self.max_short_text])})
		else: return {}
		return d

	def event_watcher(self):
		def on_workspace(i3, event):
			if event.change in ['focus','rename']:
				self.title = event.current.name
			else: return
			self.wakeup.set()
		def on_window(i3, event):
			if event.change in ['focus','title']:
				self.title = event.container.window_title
			elif event.change == 'close':
				self.title = i3.get_tree().find_focused().name
			else: return
			self.wakeup.set()
		i3 = i3ipc.Connection(auto_reconnect=True)
		self.title = i3.get_tree().find_focused().name
		i3.on(i3ipc.Event.WORKSPACE, on_workspace)
		i3.on(i3ipc.Event.WINDOW, on_window)
		i3.main()

class Bitter(object):
	update_time = 5 # seconds
	stop = False
	wakeup = threading.Event()

	def __init__(self):
		self.modules = OrderedDict(map(lambda m: (m.name(), m),
			filter(lambda m: m is not None, [
				WindowTitle(self.wakeup),
				Volume(self.wakeup),
				Temperature(),
				LoadAvg(),
				#Battery(),
				Datetime()
			])
		))
		signal.signal(signal.SIGTSTP, lambda n,f: self.set_stop(True))
		signal.signal(signal.SIGCONT, lambda n,f: self.set_stop(False))
		self.events_t = threading.Thread(target=self.event_watcher, daemon=True)

	def event_watcher(self):
		while True:
			line = sys.stdin.readline().strip(',')
			try:
				data = json.loads(line)
			except ValueError:
				continue
			else:
				if data['name'] in self.modules:
					self.modules[data['name']].on_click(data)
					self.wakeup.set()

	def set_stop(self, st):
		self.stop = st
		self.wakeup.set()

	def update(self):
		module_data = list(filter(len,map(lambda m: m.get_data(), self.modules.values())))
		print(json.dumps(module_data)+',')

	def run_loop(self):
		self.events_t.start()
		print(json.dumps({
			'version':1,
			'click_events':True,
			'stop_signal':signal.SIGTSTP,
			'cont_signal':signal.SIGCONT
		}))
		print('[')
		while True:
			self.update()
			self.wakeup.wait(None if self.stop else self.update_time)
			self.wakeup.clear()

if __name__ == '__main__':
	Bitter().run_loop()
