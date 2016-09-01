from controllers import weibo_oauth
from controllers import weibo_common_service

oauth_service = weibo_oauth.WeiboOauthClient()
weibo_client = weibo_common_service.WeiboBatchUserService(access_tokens=set())
