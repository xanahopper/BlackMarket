from black_market.ext import db
from .consts import AliasType


class StudentAccountAlias(db.Model):
    __tablename__ = 'student_account_alias'
    __table_args__ = (db.UniqueConstraint('alias', 'type'),
                      db.PrimaryKeyConstraint('alias', 'type', name='student_alias_pk'))

    id = db.Column(db.Integer, db.ForeignKey('account.id'))
    alias = db.Column(db.String(80))
    type = db.Column(db.SmallInteger)

    def __init__(self, id, alias, type):
        self.id = id
        self.alias = alias
        self.type = type.value

    @classmethod
    def existed(cls, alias, type_):
        return bool(cls.get_by_alias_and_type(alias, type_))

    @classmethod
    def get_by_alias_and_type(cls, alias, type_):
        r = cls.query.filter_by(alias=alias, type=type_.value).first()
        return cls.query.get(r.id_) if r else None

    @classmethod
    def get_by_id_and_type(cls, id_, type_):
        return cls.query.filter_by(id=id_, type=type_).first()

    @classmethod
    def add(cls, id_, alias, type_):
        student_account_alias = cls(id_, alias, type_)
        db.session.add(student_account_alias)
        db.session.commit()

    @classmethod
    def get_aliases_by_id(cls, id_):
        # TODO what if one/None?
        rs = cls.query.filter_by(id=id_).all()
        return {AliasType(r.type): r.alias for r in rs}

    @classmethod
    def update_alias(cls, id_, alias, type_):
        account_alias = cls.get_by_id_and_type(id_, type_.value)
        account_alias.alias = alias
        db.session.add(account_alias)
        db.session.commit()

    def remove_alias(self, type_):
        alias = self.aliases.get(type_)
        # TODO should test here
        if alias is None:
            return

        db.session.delete(self)
        db.session.commit()

    @property
    def display_mobile(self):
        if self.mobile:
            return '{0}****{1}'.format(self.mobile[:3], self.mobile[-4:])
        return ''
