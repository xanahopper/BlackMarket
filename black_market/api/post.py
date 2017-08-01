# from ._bp import create_blueprint
#
# bp = create_blueprint('post', __name__, url_prefix='/post')
#
#
# @bp.route('/post/<int:limit>/<int:offset>', methods=['GET'])
# def get_posts(limit, offset):
#     # posts = Post.gets(limit=limit, offset=offset)
#     # return normal_jsonify([post.dict_ for post in posts])
#     return
#
#
# @bp.route('/post/<int:post_id>', methods=['GET'])
# def get_post(post_id):
#     # return normal_jsonify(Post.get(post_id).dict_)
#     return
#
#
# @bp.route('/post', methods=['POST'])
# def create_post():
#     return 'create_post!'
#
#
# @bp.route('/post/<int:post_id>', methods=['PUT'])
# def edit_post(post_id):
#     # form_data = request.form
#     # post = Post.get(post_id)
#     # post.update_self(form_data)
#     # return normal_jsonify('')
#     return
