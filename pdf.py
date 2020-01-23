#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import zlib
import struct
#import urllib.request

separator = ''
pdf_file = open('sample.pdf', 'rb').read()
#pdf_file = urllib.request.urlopen('https://github.com/jankais3r/PDF-Text-Extract/raw/master/sample.pdf').read()

def decode_escapes(original_text):
	regex = re.compile(r'(\\)([0-7]{1,3})', re.UNICODE)
	def decode_match(match):
		return (struct.pack('B', int(match.group(2), 8)).decode('cp1252'))
	return regex.sub(decode_match, original_text)

def extract_text(pdf):
	stream = re.compile(rb'.*?FlateDecode.*?stream(.*?)endstream', re.S)
	text_fragments = []
	for s in stream.findall(pdf):
		s = s.strip(b'\r\n')
		try:
			deflated = zlib.decompressobj().decompress(s).decode('UTF-8')
			strings = re.findall('\[(.*)\]', deflated)
			for string in strings:
				text_fragments.append(re.findall('\((.*?)\)', string))
		except Exception as e:
			pass
	text = separator.join(separator.join(elems) for elems in text_fragments)
	return decode_escapes(text)

print(extract_text(pdf_file))
