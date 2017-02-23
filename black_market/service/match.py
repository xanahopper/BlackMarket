from collections import namedtuple

from black_market.models.models import User, Post, Demand, Supply
from black_market.libs.api.email import send_email_to

Match_Post = namedtuple("Match_Post",['id', 'supply','demand'])


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

    new_post = Match_Post(id, supply_course_id, demand_course_id)
    all_posts = Post.query.filter(Post.status<1).all()
    posts = [Match_Post(post.id, Supply.query.get(post.id).course_id, Demand.query.get(post.id).course_id) for post in all_posts]
    options = tri_match(new_post, posts)
    if options:
        content = ''
        for index, option in enumerate(options):
            content += 'Opiton %s:\n' % (index + 1)
            for post in option:
                content += 'http://blackmarket.wangzhihao.com.cn/posts/%s\n' % post.id
        send_email_to(User.query.get(Post.query.get(post.id).user_id).email, content)
        send_email_to('mew0629@qq.com', content)

def tri_match(new_post, posts):
    options = []
    for p in posts:
        opt = [new_post, p]
        for p in posts:
            if p.supply == opt[-1].demand:
                option = [p for p in opt]
                option.append(p)
                if option[-1].demand == new_post.supply:
                    options.append(option)
    return options

