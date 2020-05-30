from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.db import database_sync_to_async
from django.conf import LazySettings
from django.contrib.auth.models import User
import traceback
from django.contrib.sessions.models import Session
from urllib.parse import urlparse, parse_qs

settings = LazySettings()


@database_sync_to_async
def get_session(session_key):
    try:
        return Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return AnonymousUser()


@database_sync_to_async
def close_connections():
    close_old_connections()


@database_sync_to_async
def get_user(user_token):
    try:
        token = Token.objects.get(key=user_token)
        return User.objects.get(id=token.user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = scope
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_connections()
        headers = dict(self.scope['headers'])

        import pprint
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(headers)

        query_string = self.scope['query_string']
        # Login with TOKEN
        try:
            if query_string:
                try:
                    parsed_query = parse_qs(query_string)
                    token_key = parsed_query[b'token'][0].decode()
                    self.scope['user'] = await get_user(token_key)
                    close_connections()
                    inner = self.inner(self.scope)
                    return await inner(receive, send)
                except Token.DoesNotExist:
                    self.scope['user'] = AnonymousUser()
                except KeyError:
                    traceback.print_exc()
                    pass
                except Exception as e:  # NoQA
                    print(self.scope)
                    traceback.print_exc()
            elif b'authorization' in headers:
                try:
                    token_name, token_key = headers[b'authorization'].decode().split()
                    if token_name == 'Token':
                        self.scope['user'] = await get_user(token_key)
                        inner = self.inner(self.scope)
                        return await inner(receive, send)
                except Token.DoesNotExist:
                    self.scope['user'] = AnonymousUser()
            else:
                raise
        # Try Session login
        except:
            try:
                session_key = ''
                for name, value in self.scope['headers']:
                    if name == b'cookie':
                        session_key = value.decode('utf-8').split('sessionid=')[1]
                        session = await get_session(session_key)
                        session_data = session.get_decoded()
                        uid = session_data.get('_auth_user_id')
                        self.scope['user'] = await get_user(uid)
                        break

            # No credentials found so Set Anonymous user
            except:
                self.scope['user'] = AnonymousUser()
            inner = self.inner(self.scope)
            return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))