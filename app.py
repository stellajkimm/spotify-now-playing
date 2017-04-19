# -*- coding: utf-8 -*-

import os

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

    resp_qs = ['now playing %s\n' % text]

    return Response('\n'.join(resp_qs),
                    content_type='text/plain; charset=utf-8')

if __name__ == "__main__":
    # app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
