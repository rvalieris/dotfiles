#!/home/users/renan.valieris/conda/envs/pulse/bin/python

import re
import os
import sys
import json
import signal
import datetime
import threading
import pulsectl
import subprocess
import multiprocessing
from collections import OrderedDict

sys.stderr = open("/tmp/bitter.stderr","w")
icon_font = sys.argv[1]

def pango(txt):
	return '<span font="%s">%s</span>'%(icon_font,txt)

def wakeup():
	os.kill(os.getpid(), signal.SIGUSR1)

def run_command(*args):
	return subprocess.Popen(
		args,
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE
	).communicate()

class Module(object):
	def name(self): return type(self).__name__
	def getData(self): return {'full_text': '<empty>', 'name':self.name(), 'markup': 'pango' }
	def onClick(self,data): pass

class LoadAvg(Module):
	icon = pango('🔥')
	n_cores = multiprocessing.cpu_count()
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
	increment = 3/100
	def __init__(self):
		self.pulse = pulsectl.Pulse(threading_lock=True)
		self.sink_name = self.pulse.server_info().default_sink_name
		self.start_pulse_thread()
	def getData(self):
		d = super().getData()
		sink = self.getSink()
		pct = round(100 * self.pulse.volume_get_all_chans(sink))

		if sink.mute: t = self.icon+' mute'
		else: t = '{:s} {:d}%'.format(self.icon,pct)
		d.update({'full_text': t })
		return d

	def getSink(self):
		return self.pulse.get_sink_by_name(self.sink_name)

	def onClick(self,data):
		sink = self.getSink()
		if data['button'] == 3: # toggle mute
			self.pulse.mute(sink, not sink.mute)
		if data['button'] == 4: # increase vol
			self.pulse.volume_change_all_chans(sink, self.increment)
		if data['button'] == 5: # decrease vol
			self.pulse.volume_change_all_chans(sink, -self.increment)

	def start_pulse_thread(self):
		self.pulse2 = pulsectl.Pulse(threading_lock=True)
		self.events_t = threading.Thread(target=self.eventWatcher,daemon=True)
		self.events_t.start()

	def eventWatcher(self):
		self.pulse2.event_mask_set('all')
		self.pulse2.event_callback_set(lambda ev: wakeup())
		self.pulse2.event_listen()

class Battery(Module):
	icon = pango('⚡')
	icon2 = pango('🔌')
	get_pct = re.compile(r'(\d+)%')
	get_chr_time = re.compile(r'(\d+:\d+:\d+)')
	critical = 20
	def getData(self):
		txt, _ = run_command('acpi', '-b')
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
	temp_path = '/sys/devices/virtual/thermal/thermal_zone0/temp'
	def getData(self):
		temp = int(open(self.temp_path).read().rstrip())/1000
		d = super().getData()
		d.update({'full_text': "{:s}{:.1f}°C".format(self.icon,temp), 'urgent': temp > self.critical })
		return d

class Bitter(object):
	update_time = 5 # seconds
	def __init__(self):
		self.modules = OrderedDict(
			map(lambda m: (m.name(), m),[
			Volume(),
			Temperature(),
			LoadAvg(),
			#Battery(),
			Datetime()
		]))
		signal.setitimer(signal.ITIMER_REAL, self.update_time, self.update_time)
		signal.signal(signal.SIGALRM, lambda n,f: None)
		signal.signal(signal.SIGUSR1, lambda n,f: None)
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
					wakeup()

	def write(self, data):
		sys.stdout.write('%s\n' % data)
		sys.stdout.flush()

	def run_loop(self):
		self.events_t.start()
		self.write('{"version":1,"click_events":true}')
		self.write('[')
		while True:
			module_data = list(filter(len,map(lambda m: m.getData(), self.modules.values())))
			self.write('%s,' % json.dumps(module_data))
			signal.pause() # wait until SIGALRM or another signal

if __name__ == '__main__':
	Bitter().run_loop()
