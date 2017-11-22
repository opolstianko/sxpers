import os

import base64
from sanic import Sanic
from sanic.response import text
from sanic.response import json
from sanic.exceptions import ServerError
from sanic_cors import CORS, cross_origin

from redis import lookup_segment, set_segment
from utils import extract_mcmid

import config as cfg

app = Sanic(__name__)

@app.route("/get_segment")
@cross_origin(app)
async def get_segment(request):
    amcv_str = request.args.get('amcv', default=None) 

    if not amcv_str:
        return json({'karl_value': False})

    mcmid = extract_mcmid(amcv_str)

    if not mcmid:
        return json({'karl_value': False})

    segment = await lookup_segment(mcmid)

    if not segment:
        return json({'karl_value': False})


    return json({'karl_value': segment}) 


@app.route("/add_record", methods=['POST'])
async def add_record(request):

    USERNAME = os.environ['USERNAME']
    PASS = os.environ['PASSWORD']

    auth_token = request.token
    auth_string = 'Basic ' + base64.b64encode(bytes('%s:%s' % (USERNAME, PASS), 'utf-8')).decode('utf-8')

    if not auth_token == auth_string:
        return ServerError('Not authorized', 403)

    mcmid = request.form.get('mcmid')
    segment = request.form.get('segment')

    if not (mcmid and segment):
        return ServerError('Not authorized', 400)

    await set_segment(mcmid, segment)

    return text('OK')


app.run(host="0.0.0.0", port=5000)


