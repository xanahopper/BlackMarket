import unittest
from black_market.app import create_app
from black_market.ext import db
from black_market.libs.cache.redis import rd


# class BaseTestCase(unittest.TestCase):
#
#     def setUp(self):
#         self.app = create_app()
#         self.db = db
#         self.db.init_app(self.app)
#         self.app.app_context().push()
#         self.db.reflect()
#         self.db.drop_all()
#         self.db.create_all()
#
#     def tearDown(self):
#         self.db.session.remove()
#         self.db.reflect()
#         self.db.drop_all()


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.app_context().push()
        db.reflect()
        db.create_all()
        rd.flushdb()

    def tearDown(self):
        db.session.remove()
        rd.flushdb()
        try:
            db.drop_all()
            db.reflect()
            db.create_all()
        except Exception:
            pass

    @staticmethod
    def _add_student():
        import random
        from black_market.model.user.student import Student
        from black_market.model.user.consts import Gender, StudentType, AccountStatus
        name = 'mew' + str(random.randint(0, 100)) + str(random.randint(0, 100))
        gender = Gender.male
        grade = '2014'
        password = 'passwd'
        mobile = '1300000' + str(random.randint(0, 9)) + str(random.randint(0, 9)) + \
                 str(random.randint(0, 9)) + str(random.randint(0, 9))

        id_ = Student.add(
            name, gender, grade, StudentType.double_major,
            password, mobile, AccountStatus.need_verify)

        return Student.get(id_)


if __name__ == "__main__":
    unittest.main()
