from flask import jsonify


def normal_jsonify(data=None, err_msg='', status_code=200):
    return jsonify({'data': data, 'errMsg': err_msg}), status_code
