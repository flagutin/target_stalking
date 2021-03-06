from flask import Flask, g, request, jsonify, abort
from DB import database
from config import config
app = Flask(__name__)

def get_db():
    if not hasattr(g, 'db'):
        g.db = database()
    return g.db


def Ok(data):
    return jsonify(data), 200


def Not_found():
    return abort(404)


def No_api_key():
    return abort(401)


@app.route('/targets', methods=["GET", "POST"])
def targets():
    if request.method=='GET':
        given_api_key=request.args.get('api_key', None)

        if given_api_key and given_api_key==config['api_read_key']:
            target=request.args.get('target', None)
            if target:
                target_info=get_db().get_target_info(target)
                if target_info:
                    return Ok(target_info)
                else:
                    return Not_found()
            else:
                return Ok(get_db().get_all_targets())
        else:
            return No_api_key()
    else:
        given_api_key=request.args.get('api_key', None)

        if given_api_key and given_api_key==config['api_write_key']:
            return Ok("Only read mode awhile")
        else:
            return No_api_key()


app.run(debug=True)

