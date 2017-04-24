#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import re


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "API_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
channel_id = "UCtinbF-Q-fVthA0qrFQTgXQ"



def youtube_get_soundcloud(video_id):
	"""This method creates and executes the api call to retrieve items from the description section of youtube"""

	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
	video_response = youtube.videos().list(
		id=video_id,
		part='snippet'
		).execute()
	
	# This method is taking advantage of the fact that Casey always mentions the music artist in his description. 
	m = video_response['items'][0]['snippet']['localized']['description'].strip(" ")
	l = re.findall('https:.*soundcloud.*', m)
	return l

def youtube_get_videos_from_channel():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  soundcloud_artists = set()
  # Call the playlistitems.list method to retrieve all video id's from casey's vlog
  # playlist. 
  playlistitems_list_request = youtube.playlistItems().list(
    playlistId="PLTHOlLMWEwVy52FUngq91krMkQDQBagYw",
    part="snippet",
  )

  while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    # Get video_id of every video in the vlog playlist
    for playlist_item in playlistitems_list_response["items"]:
      video_id = playlist_item["snippet"]["resourceId"]["videoId"]
      description_response = youtube_get_soundcloud(video_id)
      if len(description_response)!=0:
		soundcloud_artists.update(description_response)

    playlistitems_list_request = youtube.playlistItems().list_next(
      playlistitems_list_request, playlistitems_list_response)

  return soundcloud_artists

if __name__ == "__main__":

  try:
    print youtube_get_videos_from_channel()
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
