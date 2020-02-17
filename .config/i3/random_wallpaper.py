#!/usr/bin/env python3
import sys
import subprocess
import requests
import html
import argparse
import re

collections = [
	'1459961', # photo of the day
	'317099', # unsplash editorial
	'3330448', # nature
	'1065976', # wallpapers
	'3330445', # textures and patterns
]

def get_screen_dims():
	p=subprocess.run(['xrandr'], stdout=subprocess.PIPE)
	l = p.stdout.decode().split('\n')[0]
	m = re.search('current (\d+) x (\d+)',l)
	return m.groups()

def set_wallpaper(path):
	subprocess.run(['feh','--no-fehbg','--no-xinerama','--bg-scale',path])

def download_random_image(path, width, height):

	cs = ','.join(collections)
	url = 'https://source.unsplash.com/collection/{}/{}x{}'.format(cs,width,height)
	r = requests.get(url, allow_redirects=False)

	url = re.search('href="(.+?)"', r.text).groups()[0]
	url = html.unescape(url)

	url = re.sub('fm=[^&]+','fm=png', url)
	url = re.sub('q=[^&]+&?','', url)

	print(url, file=sys.stderr)

	# get image
	r = requests.get(url, stream=True)
	# save image
	with open(path, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=None):
			fd.write(chunk)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--output', help='output file', required=True)
	args = parser.parse_args()

	w, h = get_screen_dims()
	download_random_image(args.output, w, h)
	set_wallpaper(args.output)

if __name__ == '__main__':
	main()

