# -*- coding: latin-1 -*-

import unittest

from spotipy.oauth2 import SpotifyClientCredentials

import spotipy

'''
    Client Credentials Requests tests
'''

class ClientCredentialsTestSpotipy(unittest.TestCase):
    '''
        These tests require user authentication
    '''

    muse_urn = 'spotify:artist:12Chz98pHFMPJEknJQMWvI'

    def test_request_with_token(self):
        artist = spotify.artist(self.muse_urn)
        self.assertTrue(artist['name'] == 'Muse')


if __name__ == '__main__':
    spotify_cc = SpotifyClientCredentials()
    spotify = spotipy.Spotify(client_credentials_manager=spotify_cc)
    spotify.trace = False
    unittest.main()
