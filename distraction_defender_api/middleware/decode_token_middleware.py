from apps.users.models import User
import jwt

class TokenDecodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        middleware_enabled = getattr(request, 'middleware_enabled', False)

        if middleware_enabled:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

            try:
                decoded_payload = jwt.decode_token(token)

                if decoded_payload and 'user_id' in decoded_payload:
                    user_id = decoded_payload['user_id']
                    user = User.objects.get(pk=user_id)
                    request.user = user

            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass
            except User.DoesNotExist:
                pass

        response = self.get_response(request)
        return response