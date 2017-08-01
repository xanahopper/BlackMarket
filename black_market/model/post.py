from black_market.ext import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    status = db.Column(db.SmallInteger)
    created_time = db.Column(db.DateTime())
    contact = db.Column(db.String(80))
    message = db.Column(db.String(256))
    # demand = db.relationship('Demand', backref='post', lazy='dynamic')
    # supply = db.relationship('Supply', backref='post', lazy='dynamic')
    # comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, student_id, created_time, contact, message, status=0):
        self.student_id = student_id
        self.created_time = created_time
        self.contact = contact
        self.message = message
        self.status = status

    def __repr__(self):
        return '<Post of %s at %s>' % (self.student_id, self.created_time)

    @classmethod
    def get(cls, id_):
        return Post.query.get(id_)

    @classmethod
    def gets(cls, limit=5, offset=0):
        return Post.query.limit(limit).offset(offset).all()

    @property
    def dict_(self):
        return dict(
            id=self.id, student_id=self.student_id, status=self.status,
            created_time=self.created_time, contact=self.contact, message=self.message)

    def update_self(self, form_data):
        if not form_data:
            return True
        status = form_data.get('status')
        contact = form_data.get('contact')
        message = form_data.get('message')
        if status:
            self.status = status
        if contact:
            self.contact = contact
        if message:
            self.message = message
        db.session.commit()
        return True

    @classmethod
    def create_post(cls, form_data):
        # username = form_data.get('username').strip()
        # phone = form_data.get('phone').strip()
        # email = form_data.get('email').strip()
        # msg = form_data.get('msg').strip()

        # p = Post(student_id, created_time, contact, message)

        # @bp.route('/post', methods=['POST'])
        # def post():
        #     student_id = int(current_user.id)
        #     supply_course_id = int(request.values.get('supplyCourse'))
        #     demand_course_id = int(request.values.get('demandCourse'))
        #     contact = request.values.get('contact').strip()
        #     message = request.values.get('message').strip()
        #     flash_form_data(message=message)
        #     if supply_course_id == 31 and demand_course_id == 32:
        #         return redirect_with_msg(
        #             '/newpost', u'同学你使用姿势不对吼！还要再学习一个！', category='post')
        #     if not contact:
        #         return redirect_with_msg(
        #             '/newpost', u'同学你要留个联系方式啊！', category='post')
        #     if not message:
        #         return redirect_with_msg(
        #             '/newpost', u'同学你好像什么言都没有留呐！', category='post')
        #     msg_max_len = 180
        #     if len(message) > msg_max_len:
        #         return redirect_with_msg(
        #             '/newpost', u'同学你留的言太多啦数据库有小情绪了！', category='post')
        #     created_time = int(time.time())
        #     p = Post(student_id, created_time, contact, message)
        #     db.session.add(p)
        #     db.session.commit()
        #     d = Demand(int(p.id), demand_course_id)
        #     s = Supply(int(p.id), supply_course_id)
        #     db.session.add(d)
        #     db.session.add(s)
        #     db.session.commit()
        #     # 15: EnvironmentEconomics; 12: FinanceEconomics
        #     if supply_course_id == 12:
        #         send_email_to('354240301@qq.com', 'FinanceEconomics!')
        #     # try:
        #     #     find_match(p.id, demand_course_id, supply_course_id)
        #     # except Exception:
        #     #     pass
        #     return redirect('/')

        pass
