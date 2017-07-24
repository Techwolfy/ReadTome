#!/usr/bin/python3

import json
import sys
from watson_developer_cloud import TextToSpeechV1

print('ok');


tts = TextToSpeechV1(
	username='0626b63b-1739-41e8-8905-949e68da4ed7',
	password='aI6VbIywQoPB',
	x_watson_learning_opt_out=True)

with open(sys.argv[1], 'r') as f:
	input = f.read()

with open('out.wav', 'wb') as wav:
	data = tts.synthesize(input, accept='audio/wav', voice='en-US_AllisonVoice')
	wav.write(data)
