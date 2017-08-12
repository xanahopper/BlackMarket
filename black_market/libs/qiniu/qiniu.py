# from qiniu import Auth, put_file, etag, urlsafe_base64_encode
# from black_market.config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET
#
#
# class QiniuBucket():
#     def __init__(self, access_key, secret_key, bucket_name):
#         self.access_key = access_key
#         self.secret_key = secret_key
#         self.bucket_name = bucket_name
#
#     @property
#     def client(self):
#         return Auth(self.access_key, self.secret_key)
#
#     def upload(self):
#         # #需要填写你的 Access Key 和 Secret Key
#         # access_key = 'Access_Key'
#         # secret_key = 'Secret_Key'
#         #
#         # #构建鉴权对象
#         # q = Auth(access_key, secret_key)
#         #
#         # #要上传的空间
#         # bucket_name = 'Bucket_Name'
#         #
#         # #上传到七牛后保存的文件名
#         # key = 'my-python-logo.png';
#         #
#         # #生成上传 Token，可以指定过期时间等
#         # token = q.upload_token(bucket_name, key, 3600)
#         #
#         # #要上传文件的本地路径
#         # localfile = './sync/bbb.jpg'
#         #
#         # ret, info = put_file(token, key, localfile)
#         # print(info)
#         # assert ret['key'] == key
#         # assert ret['hash'] == etag(localfile)
#         pass
#
#
#     def
#
#
#
#
# qiniu_client = QiniuBucket(QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET)
