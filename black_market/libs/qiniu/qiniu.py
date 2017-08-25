from qiniu import Auth
from black_market.config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET, DOMAIN


class QiniuBucket():
    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.client = Auth(access_key, secret_key)

    def get_token(self, file_name):

        # 构建鉴权对象
        client = self.client
        bucket_name = self.bucket_name

        callback_url = DOMAIN + '/api/v1/qiniu/callback'

        # 上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
        policy = {
            'callbackUrl': callback_url,
            'callbackBody': 'filesize=$(fsize)&key=$(key)&hash=$(etag)'
        }

        # 生成上传 Token，可以指定过期时间等
        token = client.upload_token(bucket_name, file_name, 1800, policy=policy)

        return token


qiniu_client = QiniuBucket(QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET)
