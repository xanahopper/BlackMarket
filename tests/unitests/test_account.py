from .base import BaseTestCase
from black_market.model.user.account import Account
from black_market.model.user.student import Student
from black_market.model.user.consts import AccountStatus, Gender, StudentType


class TestAccount(BaseTestCase):

    def test_add_studnet(self):
        name = 'mew'
        gender = Gender.male
        grade = '2014'
        password = 'passwd'
        mobile = '13000000000'

        id_ = Student.add(
            name, gender, grade, StudentType.double_major,
            password, mobile, AccountStatus.need_verify)

        student = Student.get(id_)

        assert student
        assert student.id

        account = Account.get(id_)

        assert account
        assert account.id == id_

        assert student.password != password
        assert student.need_verify()

        assert student.mobile == mobile

        student.to_normal()
        student = Student.get(id_)
        assert student.is_normal()

    def test_password(self):
        name = 'seeyoon'
        gender = Gender.male
        grade = '2014'
        password = 'passwd'
        mobile = '13000000001'

        id_ = Student.add(
            name, gender, grade, StudentType.double_major,
            password, mobile, AccountStatus.need_verify)

        student = Student.get(id_)
        assert student.verify_password(password)
        assert not student.verify_password('wrongpasswd')

    def test_change_password(self):
        name = 'zhengnan'
        gender = Gender.male
        grade = '2014'
        password = 'passwd'
        mobile = '13000000001'

        id_ = Student.add(
            name, gender, grade, StudentType.double_major,
            password, mobile, AccountStatus.need_verify)

        student = Student.get(id_)

        salt = student.salt

        new_password = 'newpasswd'
        student.change_password(new_password)

        assert student.verify_password(new_password)
        assert not student.verify_password(password)
        assert salt != student.salt

    def test_change_mobile(self):
        name = 'tim'
        gender = Gender.male
        grade = '2014'
        password = 'passwd'
        mobile = '13000000002'

        id_ = Student.add(
            name, gender, grade, StudentType.double_major,
            password, mobile, AccountStatus.need_verify)

        student = Student.get(id_)

        new_mobile = '15600000000'
        student.change_mobile(new_mobile)
        assert student.mobile == new_mobile
