from black_market.ext import db


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_type = db.Column(db.SmallInteger)

    def __init__(self, account_type):
        self.account_type = account_type.value

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def add(cls, account_type):
        account = Account(account_type)
        db.session.add(account)
        db.session.commit()
        return account.id
