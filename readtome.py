#!/usr/bin/python3

import json
import sys
from html.parser import HTMLParser
import ebooklib
from ebooklib import epub
from watson_developer_cloud import TextToSpeechV1

#IBM Watson Cognitive Service API Setup
auth = json.loads(open('auth.json').read())
tts = TextToSpeechV1(
	username=auth['username'],
	password=auth['password'],
	x_watson_learning_opt_out=True)

#Convert Epub HTML to SSML
class Parser(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def handle_starttag(self, tag, attrs):
		self.fed.append(self.process_tag(tag, True))
	def handle_endtag(self, tag):
		self.fed.append(self.process_tag(tag, False))
	def get_data(self):
		out = '<voice-transformation type="Custom" glottal_tension="-80%" rate="fast">'
		out += ''.join(self.fed)
		out += '</voice-transformation>'
		return out
	def feed(self, data):
		super().feed(data)
		return self
	def process_tag(self, tag, start):
		#Convert an HTML tag to SSML data
		tagstart = '<' if start else '</'
		if tag == 'b':
			return tagstart + 'emphasis level="strong">'
		elif tag == 'i':
			return tagstart + 'emphasis level="strong">'
		#elif tag == 'p':
		#	return tagstart + 'paragraph>'
		else:
			return ''

def main(filename):
	#Load and process epub
	book = epub.read_epub(filename)
	for index, chapter in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
		if chapter.is_chapter():
			html = chapter.get_content().decode()
			ssml = Parser().feed(html).get_data()
			#generateAudio(index, ssml)
			print(ssml)

def generateAudio(index, ssml):
	with open('chapter' + index + '.mp3', 'wb') as mp3:
		data = tts.synthesize(ssml, accept='audio/mp3', voice='en-US_AllisonVoice')
		mp3.write(data)

if __name__ == '__main__':
	main(sys.argv[1])
