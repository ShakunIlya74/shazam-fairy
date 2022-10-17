#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from config import DEVELOPER_KEY

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
# https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(q, max_results=25, order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=q,
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                       search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                         search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                          search_result['id']['playlistId']))

    # print('Videos:\n', '\n'.join(videos), '\n')
    # print('Channels:\n', '\n'.join(channels), '\n')
    # print('Playlists:\n', '\n'.join(playlists), '\n')
    # we can also  return videos, channels, playlists
    return videos


if __name__ == '__main__':

    try:
        videos = youtube_search(q='Britney Spears Criminal')
        first_result = videos[0].split('(')[-1][:-1]
        print(first_result)

        os.system(f"youtube-dl -o 'music/%(title)s.%(ext)s' -x --audio-format mp3 {first_result}")

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
