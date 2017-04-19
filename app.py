# -*- coding: utf-8 -*-

import os, json, spotipy, webbrowser
import spotipy.util as util
from spotipy import oauth2
from flask import Flask, request, Response, redirect, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return redirect('https://github.com/stellajkimm/spotify-now-playing')

@app.route('/track', methods=['post'])
def track():
    '''
    Example:
        /spotify loyalty kendrick lamar
        /spotify artist kendrick lamar
        /spotify track bitch dont kill my vibe
        /spotify album damn.
        /spotify playlist hip hop
    '''
    text = request.values.get('text')
    query_types = ['artist', 'track', 'playlist', 'album']
    if text.split(' ', 1)[0] in query_types and len(text.split(' ', 1)) > 1:
        query_type = text.split(' ', 1)[0]
        query = text.split(' ', 1)[1]
    else:
        query_type = 'track'
        query = text

    spotify = spotipy.Spotify()
    results = spotify.search(q=query, type=query_type, limit=1)
    items = results['{}s'.format(query_type)]['items']

    if len(items) > 0:
        result = items[0]['external_urls']['spotify']
    else:
        result = 'No results for "{}"'.format(text)

    data = jsonify({
        'response_type': 'in_channel',
        'text': result,
    })

    return data

@app.route('/login', methods=['post'])
def login():
    username = request.values.get('text')
    scope = 'user-read-playback-state'
    prompt_for_user_token(username, scope)

    response_text = "Successfully logged in as {}".format(username) if True else "Something went wrong with logging in."
    data = jsonify({
        'response_type': 'ephemeral',
        'text': response_text,
    })
    return data

@app.route('/callback')
def callback():
    code = request.args['code']
    print "CODE {}".format(code)
    token_info = sp_oauth.get_access_token(code)
    # Auth'ed API request
    if token_info:
        print token_info['access_token']
        return token_info['access_token']
    else:
        return None

def prompt_for_user_token(username, scope=None, client_id = None,
        client_secret = None, redirect_uri = None):
    if not client_id:
        client_id = os.getenv('SPOTIPY_CLIENT_ID')

    if not client_secret:
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

    if not redirect_uri:
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    if not client_id:
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
        scope=scope, cache_path=".cache-" + username )

    # try to get a valid token for this user, from the cache,
    # if not in the cache, the create a new (this will send
    # the user to a web page where they can authorize this app)

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print('''
            User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.
        ''')
        auth_url = sp_oauth.get_authorize_url()
        try:
            webbrowser.open(auth_url)
            print("Opened %s in your browser" % auth_url)
        except:
            print("Please navigate here: %s" % auth_url)

    return

if __name__ == "__main__":
    # app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
