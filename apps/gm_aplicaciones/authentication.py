from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomUser:
    def __init__(self, user_id):
        print(f"CustomUser {user_id}")
        self.id = user_id
        self.is_authenticated = True

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        print(f"werfano {header}")
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        try:
            user_id = validated_token['user_id']
            user = CustomUser(user_id)
            print(f"nino {user}")
            return (user, validated_token)
        except KeyError:
            raise AuthenticationFailed('Invalid token', code='invalid_token')
