# from .base import BaseTestCase
# from black_market.model.oauth.client import OAuthClient
# from black_market.model.user.consts import AccountType
# from black_market.model.oauth.scopes import OAuthScope
#
# REDIRECT_URI = 'http://pkublackmarket.cn'
# CLIENT_NAME = 'device-1'
#
#
# class OAuthClientTest(BaseTestCase):
#
#     def test_add_client(self):
#         id_ = OAuthClient.add(
#             name=CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['student', 'basic'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         assert client.id is not None
#         assert len(client.client_id) == 30
#         assert len(client.client_secret) == 30
#         assert client.redirect_uris == [REDIRECT_URI]
#         assert client.default_redirect_uri == REDIRECT_URI
#         assert OAuthScope.student.name in client.allowed_scopes
#
#     def test_add_client_without_callback(self):
#         id_ = OAuthClient.add(
#             name=CLIENT_NAME, allowed_scopes=['student', 'basic'],
#             account_type=AccountType.student)
#         client = OAuthClient.get(id_)
#         assert client.id is not None
#         assert len(client.client_id) == 30
#         assert len(client.client_secret) == 30
#         assert client.redirect_uris == []
#         assert client.default_redirect_uri is None
#         assert client.default_scopes == ['student', 'basic']
#
#     def test_edit_client(self):
#         id_ = OAuthClient.add(
#             name=CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['student', 'basic'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#
#         assert client.name == CLIENT_NAME
#         assert client.redirect_uris == [REDIRECT_URI]
#
#         client.edit('blackmarket', 'http://mrhaohaos.com')
#         client = OAuthClient.get(client.id)
#         assert client.name == 'blackmarket'
#         assert client.redirect_uris == ['http://mrhaohaos.com']
#
#     def test_get_by_client_id(self):
#         id_ = OAuthClient.add(
#             name=CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['student', 'basic'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         assert client.get_by_client_id(client.client_id).id == client.id
#
#     def test_validate_scopes(self):
#         id_ = OAuthClient.add(
#             name=CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['student'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         assert client.validate_scopes([])
#         assert client.validate_scopes(['student'])
#         assert not client.validate_scopes(['admin'])
