#!/usr/bin/python3

import json
import sys
import os
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
	def handle_data(self, data):
		self.fed.append(data.strip())
	def handle_starttag(self, tag, attrs):
		self.fed.append(self.process_tag(tag, True))
	def handle_endtag(self, tag):
		self.fed.append(self.process_tag(tag, False))
	def get_data(self):
		return ''.join(self.fed)
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
		elif tag == 'p':
			return '\n'
		else:
			return ''

def main(filename):
	#Get chapter selection
	if len(sys.argv) > 2:
		selected = sys.argv[2]
	else:
		selected = -1

	#Load and process epub
	book = epub.read_epub(filename)
	for index, chapter in enumerate(book.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
		if chapter.is_chapter():
			html = chapter.get_content().decode()
			ssml = Parser().feed(html).get_data()

			if selected == str(index) or selected == 'all':
				generateAudio(os.path.splitext(filename)[0], index, ssml)
			elif selected == -1:
				print(str(index) + ': ' + ssml[:40].replace('\n', ' ').strip() + '...\n')

def generateAudio(filename, index, ssml):
	with open(filename + '-part' + str(index) + '.mp3', 'wb') as mp3:
		voice = '<voice-transformation type="Custom" glottal_tension="-80%" rate="20%">'
		data = tts.synthesize(voice + ssml + '</voice-transformation>', accept='audio/mp3', voice='en-US_AllisonVoice')
		mp3.write(data)

if __name__ == '__main__':
	main(sys.argv[1])
