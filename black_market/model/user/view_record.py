import pickle
from datetime import datetime

from black_market.ext import db
from black_market.libs.cache.redis import mc, ONE_DAY
from black_market.model.post.consts import PostType


class ViewRecord(db.Model):
    __tablename__ = 'user_view_record'

    _cache_key_prefix = 'user:view:record:'
    _records_by_student_and_post_and_type_cache_key = (
        _cache_key_prefix + 'student:%s:post:%s:type:%s')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(56))
    post_id = db.Column(db.String(56))
    post_type_ = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, student_id, post_id, post_type):
        self.student_id = student_id
        self.post_id = post_id
        self.post_type_ = post_type.value

    @property
    def post_type(self):
        return PostType(self.post_type_)

    @classmethod
    def get(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def gets(cls, student_id, post_id, post_type=PostType.course_post):
        cache_key = cls._records_by_student_and_post_and_type_cache_key % (
            student_id, post_id, post_type.value)
        if mc.get(cache_key):
            return pickle.loads(bytes.fromhex(mc.get(cache_key)))
        records = cls.query.filter_by(
            student_id=student_id, post_id=post_id, post_type_=post_type.value).all()
        if records:
            mc.set(cache_key, pickle.dumps(records).hex())
            mc.expire(cache_key, ONE_DAY)
        return records

    @classmethod
    def add(cls, student_id, post_id, post_type=PostType.course_post):
        record = ViewRecord(student_id, post_id, post_type)
        db.session.add(record)
        db.session.commit()
        record.clear_cache()

    @classmethod
    def delete_records_by_post(cls, post_id, post_type):
        sql = ('delete from user_view_record '
               'where post_id={post_id} '
               'and post_type_={post_type}'.format(
                   post_id=post_id, post_type=post_type.value))
        db.engine.execute(sql)

    def clear_cache(self):
        mc.delete(self._records_by_student_and_post_and_type_cache_key % (
            self.student_id, self.post_id, self.post_type_))
