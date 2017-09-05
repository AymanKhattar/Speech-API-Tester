# Speech-API-Tester
Test Speech To Text SDK accuracy easily  

## Introduction 

There is a plenty of big companies that are developing speech recognition API regarding B2B. Lot of them are claiming to be the best on market for the largest amount of topics. There is an increasing number of companies that are seeking out the most natural interaction between their entity and their clients in a matter of UX and the majority of them is integrating voice control. Most of those companies are only focusing on a specific kind of topic for their voice control interface, they don't care about the recognition of other topics, they just absolutely need the best voice control for their topic.

This python project is about testing the accuracy of the most known Speech API for a specific topic. For now the tester is only available with Google Cloud Speech API and Google API Discovery and for the music topic, it test the recognition of Artists, Albums and Tracks name. 

This project provide an end-to-end solution. You only need to provide your Google API authentications, Spotify SDK identifier and secrets and the ID of the playlists you're following on Spotify and that's it, Speech API Tester will TTS your queries, STT it and test its matching. Follow my instructions step by step. 

## Installation


From source : 
```
$ git clone https://github.com/AymanKhattar/Speech-API-Tester.git
$ cd Speech-API-Tester
$ python setup.py build
$ sudo python setup.py install
```

## Speech to text SDK Authentications

### Google API Discovery Service 

Lucky you are ! This service do not require any authentication, go ahead your Google Api Discovery client should already be installed on your machine otherwise check the instructions they provide [here](https://developers.google.com/discovery/v1/getting_started), you could install it by yourself. 

### Google Cloud Speech API

If you don't already have Google Cloud credential please follow those steps :


* First go their website [here](https://cloud.google.com/?utm_source=google&utm_medium=cpc&utm_campaign=emea-fr-all-en-dr-bkws-all-all-trial-e-gcp-1002258&utm_content=text-ad-none-any-DEV_c-CRE_167377420989-ADGP_BKWS%20%7C%20EXA%20~%201:1_FR_EN_General_Cloud_TOP_clouds%20google-KWID_43700016288679307-kwd-49842666111-userloc_9056139&utm_term=KW_clouds%20google-ST_clouds%20google&ds_rl=1245734&gclid=EAIaIQobChMIl6P_0-ny1QIVpr_tCh3akg9ZEAAYASAAEgL73_D_BwE&dclid=CJ7irNXp8tUCFegD0wod5VEGvw) 
* Click on “Console” or “Go to Console”, if you are not already already subscribed please follow there instruction and subscribe. 
* Click on the button in the blue header on the right of  “Google Cloud Platform” to select create a new project. After creating your project you will see it's name in the blue header.
* Click on the menu button (3 horizontal lines), on the far left of the header. You will see the menu appearing, click on “API & Service” > “Credentials” > “Create a service account ” and follow the steps written on that [page](https://cloud.google.com/docs/authentication/getting-started#creating_the_service_account) to install. Google Cloud for Speech Recognition SDK on your machine. 



* You can also follow the [Quick Start](https://cloud.google.com/speech/docs/getting-started) guide provided by Google !

## Spotify

### Authentification 

* Go to Spotify Developper [website](https://developer.spotify.com/) and follow there steps to subscribe if you aren't already
* Click on the My App button on the right of the header then on “create an app”
* Follow the steps to create an app, then click on your app button in the middle of the [web page](https://developer.spotify.com/my-applications/#!/applications).
*  you're gonna need your “Client ID” and “Client secrets” for the next step. 

### Get Playlists ID

Actually Speech API Tester is going to create the Dataset you need from Spotify. You're going to provide it with the URI of the playlists that you need to get your data from and it will extract Artists names, Albums names or Tracks names from it. 
To get a URI go to your Spotify app or web page web app, right click on the playlist you need and click on “Copy playlist URI”. 

the URI should look like that :
![image 3](https://user-images.githubusercontent.com/17698895/30060593-5dfb3d5e-9244-11e7-90f3-e3dc2661d130.png)

```
spotify:user:spotify:playlist:37i9dQZEVXcWxW89UNRAJd
```

WARNING ! You should have a premium Spotify account & you should be following the playlist 

## Speech API Tester initialization

You now have every thing you need to easily configurate the Speech API Tester. 

## let's run it  !

Once the program is configured, run it on console and follow the instructions. The program should ask you to fill the configuration form, you should connect http://127.0.0.1:5000/ on your browser and fill the form which looks like this : 








eg. Playlists URI : 

```
spotify:user:lalraer:playlist:37i9dQZEVXcWxW89UNRAJd
spotify:user:spotify:playlist:37i9dQZEVXcWxW89UNRAJd
spotify:user:9dQZasfacWxW:playlist:37i9dQZasfacWxW89UNRAJd
spotify:user:yoolllooww:playlist:37i9dQZEVXCAfsfaEFSAFA89UNRAJd
spotify:user:top10Vald:playlist:37i9dQZEWEQRAWxW89UNRAJd
spotify:user:217qnursqpzyypankmyr2zl6a:playlist:2iT5VeumFzJTOCUiNhXi0I
```

## Results : 

### On console : 

```
...

Spotify : 100 Album extracted from Playlist 11!
Spotify : 100 Album extracted from Playlist 12!

 Hooray ! You extracted 777 albums name from Spotify !!

API : Google API Discovery, with alternatives 

1 : UNRECOGNIZED 
     SPOTIFY ---> Hits Of The Decade 2000-2009
     STT -------> its of the decade 2002-2009
2 : RECOGNIZED 
     SPOTIFY ---> 90125  
     STT -------> 90125
3 : UNRECOGNIZED 
     SPOTIFY ---> Ramses Shaffy - Laat Me
     STT -------> Ramsey caffeine love me
...
```

### CSV results :

It output a csv with all the recognized words recognized eg: `recognizedAlbums.csv`, a csv with all the unrecognized eg: `unrecognizedArtists.csv` words followed by a list of their alternatives and and a csv concatenating the scores eg: `score_tracks.csv` of  all tests so you could easily compare STT API performances. 

You can find a sample dataset by clicking  [here](https://drive.google.com/drive/u/0/folders/0BxJU9xchmjmHY21fLW8yRThLcmM)

## Next moves : 

- Add other STT SDK to test
- Dockerization
- Text processing based on ML for further improvement
- All in the cloud solution
