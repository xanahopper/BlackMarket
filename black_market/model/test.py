# from datetime import datetime
# from black_market.ext import db
#
#
# class Registration(db.Model):
#     '''关联表'''
#     __tablename__ = 'registrations'
#     student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
#     class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
#     create_at = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __init__(self, student_id, class_id):
#         self.student_id = student_id
#         self.class_id = class_id
#
#
# class Student(db.Model):
#     __tablename__ = 'students'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     _class = db.relationship('Registration', foreign_keys=[Registration.student_id],
#                              backref=db.backref('student', lazy="select"), lazy="dynamic")
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Student: %r>' %self.name
#
#
# class Class(db.Model):
#     __tablename__ = 'classes'
#     id = db.Column(db.Integer, primary_key=True)
#     students = db.relationship('Registration', foreign_keys=[Registration.class_id],
#                                backref=db.backref('_class', lazy="select"), lazy="dynamic")
#     name = db.Column(db.String(64))
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Class: %r>' %self.name