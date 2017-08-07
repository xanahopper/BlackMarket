# from oauthlib.common import generate_token
#
# from .base import BaseTestCase
# from black_market.model.oauth.token import OAuthToken
# from black_market.model.oauth.client import OAuthClient
# from black_market.model.user.consts import AccountType
#
# scopes = ['basic', 'student', 'admin']
# CLIENT_NAME = 'device-1'
# REDIRECT_URI = 'http://pkublackmarket.cn'
#
#
# class OAuthTokenTest(BaseTestCase):
#
#     def test_add_token(self):
#         account = self._add_student()
#         id_ = OAuthClient.add(
#             CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['basic', 'admin'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         access_token = generate_token()
#         refresh_token = generate_token()
#         id_ = OAuthToken.add(client.id, account.id, scopes,
#                              access_token, refresh_token)
#         token = OAuthToken.get(id_)
#
#         assert token.id is not None
#         assert token.client.id == client.id
#         assert token.user.id == account.id
#         assert token.access_token == access_token
#         assert token.refresh_token == refresh_token
#         assert token.scopes == scopes
#
#     def test_delete_token(self):
#         account = self._add_student()
#         id_ = OAuthClient.add(
#             CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['basic'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         access_token = generate_token()
#         refresh_token = generate_token()
#         id_ = OAuthToken.add(client.id, account.id, scopes,
#                              access_token, refresh_token)
#         token = OAuthToken.get(id_)
#         id_ = token.id
#         token.delete()
#         assert not OAuthToken.get(id_)
#
#     def test_get_by_token(self):
#         account = self._add_student()
#         id_ = OAuthClient.add(
#             CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['basic'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         access_token = generate_token()
#         refresh_token = generate_token()
#         id_ = OAuthToken.add(client.id, account.id, 'basic', access_token, refresh_token)
#
#         token = OAuthToken.get(id_)
#         assert OAuthToken.get_by_access_token(access_token).id == token.id
#         assert OAuthToken.get_by_refresh_token(refresh_token).id == token.id
#         assert OAuthToken.gets_by_user_id(account.id)
#         token.delete()
#         assert not OAuthToken.gets_by_user_id(account.id)
