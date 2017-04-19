# -*- coding: utf-8 -*-

import os, spotipy
from flask import Flask, request, Response, redirect

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

    spotify = spotipy.Spotify()
    results = spotify.search(q='artist:' + text, type='artist', limit=1)

    if len(results['artists']['items']) > 0:
        result = results['artists']['items'][0]['external_urls']['spotify']
    else:
        result = 'No results for "%s"' % text


    return Response(result,
                    content_type='text/plain; charset=utf-8')

if __name__ == "__main__":
    # app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
