from black_market.models.models import User, Post, Demand, Supply
from black_market.libs.api.email import send_email_to

def find_match(id, demand_course_id, supply_course_id):
    supplies = Supply.query.filter_by(course_id=demand_course_id).all()
    post_ids = []
    for supply in supplies:
        demand = Demand.query.get(supply.id)
        if demand.course_id == supply_course_id:
            if not Post.query.get(demand.id).status:
                post_ids.append(demand.id)
    content = 'There are some posts that might match your need:\n\n'
    content += 'http://blackmarket.wangzhihao.com.cn/posts/{id}\n'.format(id=id)
    user_ids = set()
    for post_id in post_ids:
        content += 'http://blackmarket.wangzhihao.com.cn/posts/{id}\n'.format(id=post_id)
        user_ids.add(Post.query.get(post_id).user_id)
    for user_id in user_ids:
        email = User.query.get(user_id).email
        if email:
            send_email_to(email, content)
            send_email_to('mew0629@qq.com', content)
