# from .base import BaseTestCase
#
# from black_market.model.oauth.grant import OAuthGrant
# from black_market.model.oauth.client import OAuthClient
# from black_market.model.user.consts import AccountType
#
# CODE = '123456789'
# REDIRECT_URI = 'http://www.black_market.com'
# scopes = ['basic', 'student', 'admin']
# CLIENT_NAME = 'device-1'
#
#
# class OAuthGrantTest(BaseTestCase):
#
#     def test_add_grant(self):
#         account = self._add_student()
#         id_ = OAuthClient.add(
#             CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['basic'],
#             redirect_uri=REDIRECT_URI)
#         client = OAuthClient.get(id_)
#         id_ = OAuthGrant.add(
#             id_, CODE, REDIRECT_URI, scopes, account.id)
#         grant = OAuthGrant.get(id_)
#         assert grant.id is not None
#         assert grant.client.id == client.id
#         assert grant.user.id == account.id
#
#     def test_delete_grant(self):
#         account = self._add_student()
#         id_ = OAuthClient.add(
#             CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['basic', 'student'],
#             redirect_uri=REDIRECT_URI)
#         id_ = OAuthGrant.add(
#             id_, CODE, REDIRECT_URI, scopes, account.id)
#         grant = OAuthGrant.get(id_)
#         id_ = grant.id
#         grant.delete()
#         assert not OAuthGrant.get(id_)
#
#     def test_get_by_code(self):
#         account = self._add_student()
#         id_ = OAuthClient.add(
#             CLIENT_NAME,
#             account_type=AccountType.student,
#             allowed_scopes=['basic', 'student'],
#             redirect_uri=REDIRECT_URI)
#         id_ = OAuthGrant.add(
#             id_, CODE, REDIRECT_URI, scopes, account.id)
#         grant = OAuthGrant.get(id_)
#         assert OAuthGrant.get_by_code(grant.client_id, CODE).id == grant.id
#         grant.delete()
#         assert not OAuthGrant.get_by_code(grant.client_id, CODE)
