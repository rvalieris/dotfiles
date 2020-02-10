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
import threading
import subprocess
from collections import OrderedDict

icon_font = sys.argv[1]

def pango(txt):
	return '<span font="%s">%s</span>'%(icon_font,txt)

class Module(object):
	def name(self): return type(self).__name__
	def getData(self): return {'full_text': '<empty>', 'name':self.name(), 'markup': 'pango' }
	def onClick(self,data): pass

class LoadAvg(Module):
	icon = pango('🔥')
	n_cores = os.cpu_count()
	def getData(self):
		t0, _, _ = os.getloadavg()
		d = super().getData()
		d.update({'full_text': "{:s} {:.2f}".format(self.icon,t0), 'urgent': t0 > self.n_cores })
		return d

class Datetime(Module):
	icon1 = pango('📅')
	icon2 = pango('⌚')
	def getData(self):
		txt = datetime.datetime.now().strftime(self.icon1+' %b %Y, %A %d '+self.icon2+' %H:%M:%S')
		d = super().getData()
		d.update({'full_text': txt })
		return d

class Volume(Module):
	icon = pango('🔊')
	icon2 = pango('🔈')
	increment = 3/100
	pct = 0
	dunstify = None
	sink_name = ''

	def __new__(cls, *args):
		try:
			global pulsectl
			import pulsectl
			return super(Volume,cls).__new__(cls)
		except:
			return None

	def __init__(self, wakeup):
		self.wakeup = wakeup
		self.pulse = pulsectl.Pulse(threading_lock=True)
		self.start_pulse_thread()
		self.dunstify = shutil.which('dunstify')

	def getData(self):
		d = super().getData()
		sink = self.getSink()
		pct = round(100 * self.pulse.volume_get_all_chans(sink))
		if self.dunstify:
			if self.pct != pct:
				subprocess.run([self.dunstify,'-r',str(os.getpid()),'Volume {:d}%'.format(pct)])
				self.pct = pct
			if self.sink_name != sink.name:
				subprocess.run([self.dunstify,'-r',str(os.getpid()),'Sink {}'.format(sink.name)])
				self.sink_name = sink.name
		if sink.mute: t = self.icon2+' mute'
		else: t = '{:s} {:d}%'.format(self.icon,pct)
		d.update({'full_text': t })
		return d

	def getSink(self):
		return self.pulse.get_sink_by_name('@DEFAULT_SINK@')

	def onClick(self,data):
		sink = self.getSink()
		if data['button'] == 2: # open pavucontrol
			subprocess.Popen(['i3-msg','-q','exec','pavucontrol'])
		if data['button'] == 3: # toggle mute
			self.pulse.mute(sink, not sink.mute)
		if data['button'] == 4: # increase vol
			self.pulse.volume_change_all_chans(sink, self.increment)
		if data['button'] == 5: # decrease vol
			self.pulse.volume_change_all_chans(sink, -self.increment)

	def start_pulse_thread(self):
		self.events_t = threading.Thread(target=self.eventWatcher,daemon=True)
		self.events_t.start()

	def eventWatcher(self):
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

	def getData(self):
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
		d = super().getData()
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
			return None

	def __init__(self):
		self.thermal_zone = Temperature.find_thermal_zone()

	def getData(self):
		if os.path.isfile(self.thermal_zone):
			temp = int(open(self.thermal_zone).read().rstrip())/1000
			d = super().getData()
			d.update({'full_text': "{:s}{:.1f}°C".format(self.icon,temp), 'urgent': temp > self.critical })
			return d
		else:
			return {}

class WindowTitle(Module):
	icon = pango('💠')
	max_short_text = 45

	def __new__(cls, *args):
		try:
			global i3ipc
			import i3ipc
			return super(WindowTitle,cls).__new__(cls)
		except:
			return None

	def __init__(self, wakeup):
		self.wakeup = wakeup
		self.title = ''
		self.events_t = threading.Thread(target=self.eventWatcher,daemon=True)
		self.events_t.start()

	def getData(self):
		d = super().getData()
		if len(self.title) > 0:
			d.update({'full_text': self.icon+' '+html.escape(self.title) })
			if len(self.title) > self.max_short_text:
				d.update({'short_text': self.icon+' '+html.escape(self.title[:self.max_short_text])})
		else: return {}
		return d

	def eventWatcher(self):
		def on_workspace(i3, event):
			if event.change == 'focus':
				self.title = event.current.name
			else: return
			self.wakeup.set()
		def on_window(i3, event):
			if event.change in ['focus','title']:
				self.title = event.container.window_title
			elif event.change == 'close':
				self.title = ''
			else: return
			self.wakeup.set()
		i3 = i3ipc.Connection()
		i3.on(i3ipc.Event.WORKSPACE, on_workspace)
		i3.on(i3ipc.Event.WINDOW, on_window)
		i3.main()

class Bitter(object):
	update_time = 5 # seconds
	stop = False
	wakeup = threading.Event()

	def __init__(self):
		modules = filter(lambda m: m is not None, [
			WindowTitle(self.wakeup),
			Volume(self.wakeup),
			Temperature(),
			LoadAvg(),
			#Battery(),
			Datetime()
		])
		self.modules = OrderedDict(map(lambda m: (m.name(), m),modules))
		signal.signal(signal.SIGTSTP, lambda n,f: self.setStop(True))
		signal.signal(signal.SIGCONT, lambda n,f: self.setStop(False))
		self.events_t = threading.Thread(target=self.eventWatcher, daemon=True)

	def eventWatcher(self):
		while True:
			line = sys.stdin.readline().strip(',')
			try:
				data = json.loads(line)
			except ValueError:
				continue
			else:
				if data['name'] in self.modules:
					self.modules[data['name']].onClick(data)
					self.wakeup.set()

	def write(self, data):
		sys.stdout.write('%s\n' % data)
		sys.stdout.flush()

	def setStop(self, st):
		self.stop = st
		self.wakeup.set()

	def update(self):
		module_data = list(filter(len,map(lambda m: m.getData(), self.modules.values())))
		self.write('%s,' % json.dumps(module_data))

	def run_loop(self):
		self.events_t.start()
		self.write(json.dumps({
			'version':1,
			'click_events':True,
			'stop_signal':signal.SIGTSTP,
			'cont_signal':signal.SIGCONT
		}))
		self.write('[')
		while True:
			self.update()
			self.wakeup.wait(None if self.stop else self.update_time)
			self.wakeup.clear()

if __name__ == '__main__':
	Bitter().run_loop()
