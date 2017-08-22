from datetime import datetime
from flask import request, g

from .._bp import create_blueprint
from black_market.api.utils import normal_jsonify
from black_market.api.decorator import require_session_key
from black_market.api.schema.qiniu import GetUploadTokenSchema
from black_market.libs.qiniu.qiniu import qiniu_client
from black_market.model.user.student import Student
from black_market.model.user.behavior import UserBehavior
from black_market.model.user.consts import UserBehaviorType
from black_market.model.file.photo import FilePhoto
from black_market.model.exceptions import UserNotFoundError


bp = create_blueprint('qiniu', 'v1', __name__, url_prefix='/qiniu')


@bp.route('/token', methods=['POST'])
@require_session_key()
def get_token():
    student = Student.get(g.wechat_user.id)
    if not student:
        raise UserNotFoundError()
    data = GetUploadTokenSchema().fill()
    ext = data.get('ext')
    now = datetime.now().strftime('%y%m%d%H%M%S')
    file_name = 'bm-post-pic-s%s-t%s.%s' % (student.id, now, ext)
    id_ = FilePhoto.add(student.id, qiniu_client.bucket_name, file_name)
    token = qiniu_client.get_token(file_name=file_name)
    return normal_jsonify(dict(id=id_, token=token))


@bp.route('/callback', methods=['POST'])
def callback():
    data = request.form
    key = data.get('key')
    filesize = data.get('filesize')
    hash = data.get('hash')
    photo = FilePhoto.get_by_file_name(key)
    if not photo:
        raise
    photo.update(filesize=filesize, hash=hash)
    UserBehavior.add(photo.user_id, UserBehaviorType.upload_photo, dict(key=key))
    return normal_jsonify()
