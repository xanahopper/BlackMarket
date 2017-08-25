from datetime import datetime

from black_market.ext import db
from black_market.model.file.consts import FileStatus


class FilePhoto(db.Model):
    __tablename__ = 'file_photo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    bucket = db.Column(db.String(80))
    file_name = db.Column(db.String(80))
    filesize = db.Column(db.String(80))
    hash = db.Column(db.String(128))
    status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_id, bucket, file_name,
                 status=FileStatus.ready_to_upload, filesize=None, hash=None):
        self.user_id = user_id
        self.bucket = bucket
        self.file_name = file_name
        self.filesize = filesize
        self.hash = hash
        self.status = status.value

    def dump(self):
        return dict(id=self.id, file_name=self.file_name)

    @classmethod
    def add(cls, user_id, bucket, file_name):
        photo = FilePhoto(user_id, bucket, file_name)
        db.session.add(photo)
        db.session.commit()
        return photo.id

    @classmethod
    def get(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def get_by_file_name(cls, file_name):
        return cls.query.filter_by(file_name=file_name).first()

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def update(self, filesize, hash, status=FileStatus.has_uploaded):
        self.filesize = filesize
        self.hash = hash
        self.status = status.value
        db.session.add(self)
        db.session.commit()
