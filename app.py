import os

import base64
from sanic import Sanic
from sanic.response import file
from sanic.response import text
from sanic.exceptions import ServerError
from redis import lookup_segment, set_segment
from utils import extract_mcmid

app = Sanic(__name__)

@app.route("/get_segment/img.png")
async def get_segment(request):
    amcv_str = None
    dir_path = os.path.dirname(os.path.realpath(__file__))

    for cook_str in request.cookies:
        if 'AMCV_' in cook_str:
            amcv_str = request.cookies[cook_str]
            break

    if not amcv_str:
        return text('Not found')

    mcmid = extract_mcmid(amcv_str)

    if not mcmid:
        return await file(dir_path + '/img.png')

    segment = await lookup_segment(mcmid)

    if not segment:
        return await file(dir_path + '/img.png')

    response = await file(dir_path + '/img.png')
    response.cookies['pers'] = 'I am value!'
    response.cookies['pers']['max-age'] = 3600

    return response


@app.route("/add_record", methods=['POST'])
async def add_record(request):

    ADMIN_USERNAME = os.environ('USERNAME')
    ADMIN_PASS = os.environ('PASSWORD')

    auth_token = request.token
    auth_string = 'Basic ' + base64.b64encode(bytes('%s:%s' % (ADMIN_USERNAME, ADMIN_PASS), 'utf-8')).decode('utf-8')

    if not auth_token == auth_string:
        return ServerError('Not authorized', 403)

    mcmid = request.form.get('mcmid')
    segment = request.form.get('segment')

    if not (mcmid and segment):
        return ServerError('Not authorized', 400)

    await set_segment(mcmid, segment)

    return text('OK')


app.run(host="0.0.0.0", port=8080, debug=True)
