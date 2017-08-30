#_*_ coding:utf-8 _*_

import os
import base64
import time 
import sys
import spotipy
import json
import datetime
import io
import shutil
import googleapiclient.discovery

from gtts import gTTS
from pydub import AudioSegment
from os import mkdir
from shutil import rmtree
from os.path import join , basename , splitext, isfile, isdir
from spotipy.oauth2 import SpotifyClientCredentials
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

reload(sys)
sys.setdefaultencoding('utf-8')


# intermediate folders stocking mp3 -> wav TTS output 
final_wav_path = 'wav_tts_artist' 
final_mp3_path = 'mp3_tts_artist'

# Instantiates a client
client = speech.SpeechClient()

class DataFromSpotify(object):
	"""docstring for DataFromSpotify
	In this class we will extract data from spotify.

	inputs : Spotify Client ID , Spotify Client Secrets and  Spotify Client Playlists  
	modules : Extract from Album, Artists and Tracks. And a Counter module to display extracting state to user. 
	"""
	iteration = 1
	def __init__(self, client_id,client_secret, playlistsURI, maxSample, maxPlaylist):
		
		'''
			self.maxSample : maximum number of samples we need from every playlists, /!\ max spotify number is 100 
			self.maxPlaylist : maximum number of playlists we need
		'''
		self.client_id = client_id
		self.client_secret = client_secret
		self.playlistsURI = playlistsURI
		self.iteration +=1
		if not maxSample : self.maxSample = 100
		else : self.maxSample = maxSample
		if not maxPlaylist : self.maxPlaylist = 100
		else : self.maxPlaylist = maxPlaylist

		# TODO topFromPlaylist / numOfPlaylists / genre ? 
		
	@classmethod
	def compteur(cls):
		print(cls.iteration)

	def extractAlbums(self) : 
		
		print('Extracting Albums from Spotify ...')

		client_credentials_manager = SpotifyClientCredentials(client_id= self.client_id,client_secret=self.client_secret)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

		albumList = []
		for nb_playlists , uri in enumerate(self.playlistsURI) :
			# extracting user info from URI
			username = uri.split(':')[2]
			playlist_id = uri.split(':')[4]
			results = sp.user_playlist(username, playlist_id)

			# select albums 
			for cmpt , track in enumerate(results['tracks']['items']) :
				albumList.append(track['track']['album']['name'].encode('utf-8'))
				if cmpt >= self.maxSample : 
					break # only process the desired number of music per playlist				
			if len(self.playlistsURI) == 1 or nb_playlists >= self.maxPlaylist:
				break # don't loop if only one playlist in the pack, only processing the desired number of playlist
				# TODO, shuffle playlists   
			self.__class__.iteration += 1
			print('Spotify : {0} Album extracted from Playlist {1}!'.format(cmpt+1,self.__class__.iteration))
		return albumList , len(albumList)


	def extractArtists(self) : 

		print('Extracting Artists from Spotify ...')
		client_credentials_manager = SpotifyClientCredentials(client_id= self.client_id,client_secret=self.client_secret)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

		artistList = []
		for nb_playlists , uri in enumerate(self.playlistsURI) :

			username = uri.split(':')[2]
			playlist_id = uri.split(':')[4]
			results = sp.user_playlist(username, playlist_id)

			# select artists 
			for cmpt , track in enumerate(results['tracks']['items']) :
				for artist in track['track']['album']['artists'] :
					artistList.append(artist['name'].encode('utf-8'))
					break
				if cmpt >= self.maxSample : 
					break				
			if len(self.playlistsURI) == 1 or nb_playlists >= self.maxPlaylist:
				break
			self.__class__.iteration += 1
			print('Spotify : {0} Artists extracted from Playlist {1}!'.format(cmpt+1,self.__class__.iteration))
		return artistList , len(artistList)


	def extractTracks(self) : 

		print('Extracting Tracks from Spotify ...')
		client_credentials_manager = SpotifyClientCredentials(client_id= self.client_id,client_secret=self.client_secret)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

		trackList = []
		for nb_playlists , uri in enumerate(self.playlistsURI) :

			username = uri.split(':')[2]
			playlist_id = uri.split(':')[4]
			results = sp.user_playlist(username, playlist_id)

			# select tracks 
			for cmpt , track in enumerate(results['tracks']['items']) :
				trackList.append(track['track']['name'].encode('utf-8'))
				if cmpt >= self.maxSample : 
					break				
			if len(self.playlistsURI) == 1 or nb_playlists >= self.maxPlaylist:
				break
		self.__class__.iteration += 1
		print('Spotify : {0} Tracks extracted from Playlist {1}!'.format(cmpt+1,self.__class__.iteration))
		return trackList , len(trackList)




class  CleaningDB():
	"""docstring for  CleaningDB
		module remove duplicate. 
		arg : data to clean
		return : cleaned dataset , new dataset size
	"""
	
	def __init__(self):
		pass

	def removeDuplicated(self,data):

		seen = set(data)
		for x in data:
		    if x not in seen:
		        seen.add(x)
		return seen , len(seen)



def getCleanedSpDB(dataList,listsToClean,focus=None) :
	'''
		Tacks cleaning modules and apply them to 3 types of data, Tracks, Artists and Albums
	'''
	if focus == 'tracks' :
		trackList , size_trackList = dataList.extractTracks()
		return listsToClean.removeDuplicated(trackList)[0]
	elif focus == 'albums' :
		albumList , size_albumList = dataList.extractAlbums()
		return listsToClean.removeDuplicated(albumList)[0]
	elif focus == 'artists':
		artistList , size_artistList = dataList.extractArtists()
		return listsToClean.removeDuplicated(artistList)[0]
	else :
		print("Exception in degCleanedSpDB() , focus= 'albums' , 'artists' or 'tracks' " ) 


def clean_memory() :
	'''
		replace audio output files and folders if its already saved
		keep only one file for every iteration 
	'''
	# remove audio output files and folder
	if isdir(final_wav_path):
		rmtree(final_wav_path)
	if isdir(final_mp3_path):
		rmtree(final_mp3_path)
	# creat audio output folder 
	mkdir(final_mp3_path)
	mkdir(final_wav_path)

def tts(text): 
	'''
		this function will be used as a for loop array, it takes list and yield one by one each of its values 
		take a list of strings and tts each of those strings 
	'''
	lan = 'en-us' # 'English (United States)'
	for speech_text in text :
		speech_text = speech_text.lower()
		time.sleep(0.5)

		try:
			# calls Google TTS API and yield its output 
			yield gTTS(text= speech_text, lang=lan, slow = False) , speech_text
		except Exception:
		    print("Connection refused to gTTS")
		    yield (None,None)

def SpeechContextProcess(text):
	'''
		This function would help you making sure the string data list extracted from Spotify will fits the Speech Context limits 
		requierd by Google.

		Args : text (list of str)
		returns [resized text (below Google limits), rejecter phrases].  
			google limits are : 
				500 phrases per request
				10,000 total character per request
				100 character per phrase. 
	'''
	totChar = 0
	rejected = []
	# make sur there is less than 100 character per phrase
	for i in text:
		totChar = totChar + len(i)
		if len(i) >= 100 :
			rejected.extend(text[text.index(i)]) 
			del text[text.index(i)] 


	# make sur there is less than 10,000 character per request
	cmpt= 0
	while totChar >= 10000:
		rejected.append(text[-1])
		text.pop()
		cmptChar = 0
		for i in text: # I'm not convinced, there might be a better solution 
			cmptChar = cmptChar + len(i)
		totChar = cmptChar
		cmpt +=1 
	# make sur there is less than 500 phrases per request
	if len(text) >= 500 :
		text = text[:499]
		rejected.extend(text[500:])
	return text , rejected


def stt_gCloud(file_name,hints): # with google cloud, No speechContexts and no MaxAlternatives (new version)
	# Loads the audio into memory
	with io.open(file_name, 'rb') as audio_file:
	    content = audio_file.read()
	    audio = types.RecognitionAudio(content=content)

	config = types.RecognitionConfig(
	    encoding='FLAC', #enums.RecognitionConfig.AudioEncoding.LINEAR16,
	    # sample_rate_hertz=16000, # gives error message  
	    language_code='en-US')
	    # maxAlternative=30, #
	    # speechContext = {
	    # 'phrases' : hints})

	# Detects speech in the audio file
	response = client.recognize(config, audio)
	alternatives = response.results[0].alternatives # find transcript value in provided JSON output 
	for alternative in alternatives:
		return alternative.transcript # return provided string value



def stt(file,guesses,ishint): # with google apis (older version)
	
	with open(file, 'rb') as speech:
		# Base64 encode the binary audio file for inclusion in the JSON
		speech_content = base64.b64encode(speech.read())
	try : 
		service = googleapiclient.discovery.build('speech', 'v1')
		if ishint :
			recognized_text = [] #'Transcribed Text: \n'
			cmpt=0
			while len(guesses) >= cmpt*500: # im not convinced yet, there is a better way in think
			    try : # feed Google Cloud Speech API with the required amount of hints and loop it back until trying all provided hints 
				    guessesFit = guesses[cmpt*500:(cmpt+1)*500]
			    except IndexError :
			    	guessesFit = guesses[cmpt*500:] 
			    guessesFit , rejects = SpeechContextProcess(guessesFit)
			    service_request = service.speech().recognize(
			        body={"config": { 
			                "maxAlternatives": 30, # max amount of provided alternatives 
			                "languageCode": "en_US",
			                "encoding": "FLAC",
			                "speechContexts": {
			                	"phrases" : guessesFit} # input hints 
			                	},
			                'audio': {'content': speech_content}})
			    response = service_request.execute()
			    if response != {} : 
			      for i in range(len(response['results'][0]['alternatives'])):
			        recognized_text.append(response['results'][0]['alternatives'][i]['transcript']) # concate all alternatives
			    cmpt += 1
			
			return recognized_text # return list of alternatives

		else : 
		    service_request = service.speech().recognize(
		        body={"config": {
		                "maxAlternatives": 30,
		                "languageCode": "en_US",
		                "encoding": "FLAC",
		                },
		                'audio': {'content': speech_content}})
		    response = service_request.execute()
		    recognized_text = [] 
		    if response != {} : 
		      for i in range(len(response['results'][0]['alternatives'])):
		        recognized_text.append(response['results'][0]['alternatives'][i]['transcript'])
		    return recognized_text
	except :
		print(Exception('Google API Discovery Client with alternative did not respond'))
		return ''



def stt_no_alt(file,guesses,ishint): # with google apis (old version)
	  # STT with no alternatives 

    with open(file, 'rb') as speech:
        # Base64 encode the binary audio file for inclusion in the JSON
        # request.
        speech_content = base64.b64encode(speech.read())
	# Construct the request
	try : 
		service = googleapiclient.discovery.build('speech', 'v1')
		if ishint :
			recognized_text =[]
			cmpt = 0 
			while len(guesses) >= cmpt*500: 
			    try : 
				    guessesFit = guesses[cmpt*500:(cmpt+1)*500]
			    except : # IndexError :
			    	guessesFit = guesses[cmpt*500:]
			    guessesFit , rejects = SpeechContextProcess(guessesFit)

			    service_request = service.speech().recognize(
			        body={"config": {
			                "maxAlternatives": 1,
			                "languageCode": "en_US",
			                "encoding": "FLAC",
			                "speechContexts": {
			                	"phrases" : guessesFit}
			                	},
			                'audio': {'content': speech_content}})
			    response = service_request.execute()

			    recognized_text.append(response['results'][0]['alternatives'][0]['transcript'])
			    cmpt+=1
			return recognized_text
		else : 
			service_request = service.speech().recognize(
			    body={"config": {
			            "maxAlternatives": 1,
			            "languageCode": "en_US",
			            "encoding": "FLAC",
			            },
			            'audio': {'content': speech_content}})
			response = service_request.execute()
			return response['results'][0]['alternatives'][0]['transcript']
	except :
		print('Exception : STT with NO alternative did not respond')
		return []


def clean_filename(name) : 
	'''
		when filenames are automatically generated we need to ensure they are valid, no space and no special character 
		only, alphabet and _ 
	'''
	for character in name : 
		name = name.replace('$', 's').replace(' + ', ' and ').replace(' & ', ' and ')
		if not character.isalnum() : 
			name = name.replace(character, '')
	return name


def handled_open(file):
	'''
		The results are outputted to csv file. this fonction will make sure users won't lose their results. 
		Users will be ask if they want to archive their existing output file or archive it. 	
	'''
	
	if isfile(file) :
		print('\nIt seems like {} already exist and contain data : \n If you want to : \n  -Replace it, enter R \n  -Archive it, enter [A]'.format(file))
		if sys.version_info[0] < 3:
		    input_var = raw_input("\n Answer : ").lower()
		else :
			input_var = input("\n Answer : ").lower()


		if input_var in ['r','replace'] : 
			pass			
		else :
			prefix , csv = file.split('.')
			newfile = prefix + str(datetime.datetime.today()) + '.' + csv
			
			try : 
				os.rename(file, join('archive/',newfile))
			except :#Exception as e: 
				print(Exception('From Handler open, not able to move file'))
				# print(' {} to archive'.format(newfile))
				if not isdir('archive') :
					try : 
						os.mkdir('archive/')
						os.rename(file, join('archive/',newfile))
					except : 
						Exception('Something when wrong while creating /archive or moving {} to archive'.format(newfile))
				else : 
					try : 
						shutil.move(file, join('archive',newfile))
					except Exception as e: 
						raise Exception(e)
		f = open(file,'w+')
		f.close()
		return open(file, 'r+')
	else :
		return os.open(file, os.O_RDWR | os.O_CREAT) 
		# return os.fdopen(fd, *args, **kwargs)


def recognitionTest(text,focus,alt,api,hints) :
	'''
	This function is a manager one which handle STT and TTS, it takes the text 
	output from Spotify and gives lists of recognized and unrecognized tracks from the Speech recognition API.
	
	Args :
		text : list of strings containing albums, artists or tracks    
		focus : string containing Albums, Artists or Tracks
		alt = boolean, is the user would like to see the total guesses that the Api had about the unrecognized sentences ? 
	Returns :
		output_recognized : list of strings containing all recognized albums, artists or tracks
		output_unrecogized : list of strings containging all unrecognized albums, artists or tracks  
	'''
	c = ['albums','artists','tracks'].index(focus) # 0 Albums , 1 Artists , 2 Tracks
	output_text = [['recognizedAlbums.csv' , 'unrecognizedAlbums.csv'] , ['recognizedArtists.csv' , 'unrecognizedArtists.csv'] , ['recognizedtracks.csv' , 'unrecognizedtracks.csv']][c]
	
	output_recognized = handled_open(output_text[0])
	output_unrecognized = handled_open(output_text[1])
	clean_memory()
	
	recognition = False
	out_unrec = []
	out_rec = []
	i = 0 

	for speech , filename in tts(text) : # process every yield audio file one by one 
		i+=1 # counter used for a displaying purpose. 
		try : 
			# print('\nExtracting TTS audio output as a file')
			filename = clean_filename(filename)
			speech.save(join(final_mp3_path,filename)) # save mp3
			# os.popen('mpg321 '+ final_mp3_path + '/' + filename) # read mp3 (just to verify)
			if isfile(join(final_wav_path,filename)) == False: 
				sound = AudioSegment.from_mp3(join(final_mp3_path,filename))
				sound.export(join(final_wav_path,filename), format="flac") # save flac
		except : #AttributeError :
			print('Exception : could not extract TTS audio output as a file')
		try:
			
			# Speech recognition depending on The API and parameters we need
			if alt == 1 and api == 'googleapi':
				if i == 1 : print '\nAPI : Google API Discovery, with alternatives \n'
				stt_ = stt(join(final_wav_path,filename),text,hints)
			elif alt == 0 and api == 'googleapi' : 
				if i == 1 : print '\nAPI : Google API Discovery, without alternatives \n'
				stt_ = stt_no_alt(join(final_wav_path,filename),text,hints)		
			elif alt == 0 and api == 'googlecloud' :
				if i == 1 : print '\nAPI : Google Cloud Speech API, without alternatives \n'
				stt_ = stt_gCloud(join(final_wav_path,filename),text)
			else : 
				raise Exception('\nYou parameters do not match with what these STT API offer you. Please check the possibilities in "sttParameterSheet.csv"')
				# TODO make an object for all STT modules, make it cleaner.  
			if isinstance(stt_, (str, unicode)) : # make sure <type(stt_) , 'list' > 
				stt_ = [stt_]
			
			try:
				for STT in stt_ : 
					if clean_filename(STT).lower() == filename :
						recognition = True 
						break 
				if recognition :
					# print STT, '  ---- OK'
					STT = STT.encode('utf-8')
					output_recognized.write(STT + '\n')
					out_rec.append(STT)
					print('{0} : RECOGNIZED \n 	SPOTIFY ---> {1}  '.format(i,text[i-1]))
					print(' 	STT -------> {}'.format(STT))
				else : 
					output_unrecognized.write(filename)
					for STT1 in stt_ : 
						output_unrecognized.write(',' + STT1)
					output_unrecognized.write('\n')
					out_unrec.append(STT1)
					print('{0} : UNRECOGNIZED \n 	SPOTIFY ---> {1}'.format(i,text[i-1]))
					print(' 	STT -------> {}'.format(STT1))
				recognition = False
			except TypeError , IOError:
				print('STT could not open audio file')
				# print(IOError('STT could not open audio file'))
				# raise TypeError('STT function returned a None object')
		except (AttributeError , UnicodeEncodeError , TypeError) as e : # only except : if you don't want any crash (Dangerous)
			print('STT did not respond')
			# print(AttributeError('Could not STT the TTS audio output'))
			# print(UnicodeEncodeError('"ascii" codec cannot encode character u \ xf6'))	
			clean_memory()
	return out_rec , out_unrec
			 	

def score(inputs,recognized, unrecognized, focus, api, hints, alt) : 

	'''
		output the final score in a csv file. Concatenate old results and new ones so you can compare it. 
	'''

	# create score output csv file
	if any(focus in s for s in ['artists', 'albums' , 'tracks']) :
		output_score = open('score_' + focus + '.csv' , 'a')
		nb_input = len(inputs)
		if recognized :
			nb_recognized = len(recognized)
			# print(recognized)
		else : print('Weird ... Nothing have been recognized')
		if unrecognized:
			nb_unrecognized = len(unrecognized)
			# print('\n\n\n\n {}'.format(unrecognized))
		elif recognized :  
			print('Cool ! but weird ... Everything have been recognized')
		
		if recognized and unrecognized :
			unprocessed_input = nb_input - (nb_recognized + nb_unrecognized)
			real_nb_input = nb_input - unprocessed_input
			percent = float(100*(float(nb_recognized)/float(real_nb_input)))

			output_score.write("{0} :\n {1} [hints : {8}] and  [alternatives : {9}] \n 	 has recognize {2} {3} from {4},\n 	 \
has unrecognize {5} {3} from {4}, \n 	 {6} {3} could not have been processed by Speech API tester,\n\n\
And the final recognition score of this test is : {7} \n\n\n \
			  ".format(datetime.datetime.today(),api,nb_recognized,focus,real_nb_input,nb_unrecognized,unprocessed_input,percent,hints,alt))


			print("{0} :\n {1}  [hints : {8}] and  [alternatives : {9}], \n 	 has recognize {2} {3} from {4},\n 	 \
has unrecognize {5} {3} from {4}, \n 	 {6} {3} could not have been processed by Speech API tester,\n\n\
And the final recognition score of this test is : {7} \n\n\n \
			  ".format(datetime.datetime.today(),api,nb_recognized,focus,real_nb_input,nb_unrecognized,unprocessed_input,percent,hints,alt))
		

		else : 
			print("No need to calculate the score, either it's 100 or it's 0, but I think their is a problem somewhere")
