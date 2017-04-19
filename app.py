# -*- coding: utf-8 -*-

import os, json, spotipy
from flask import Flask, request, Response, redirect, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return redirect('https://github.com/stellajkimm/spotify-now-playing')

@app.route('/track', methods=['post'])
def track():
    '''
    Example:
        /spotify kendrick lamar humble
    '''
    text = request.values.get('text')

    query_types = ['artist', 'track', 'playlist', 'album']
    if text.split(' ', 1)[0] in query_types and len(text.split(' ', 1)) > 1:
        query_type = text.split(' ', 1)[0]
        query = '{0}:{1}'.format(query_type, text.split(' ', 1)[1])
    else:
        query_type = 'track'
        query = '{0}:{1}'.format(query_type, text)

    spotify = spotipy.Spotify()
    results = spotify.search(q=query, type=query_type, limit=1)
    print results
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

if __name__ == "__main__":
    # app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
