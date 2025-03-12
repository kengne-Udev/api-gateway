import requests
import jwt
from jwcrypto import jwk
from django.conf import settings


def get_jwks():
    response = requests.get(settings.AUTH_SERVICE_JWKS_URL)
    response.raise_for_status()

    print("res: ", response.json())
    return response.json()


def validate_jwt(token):
    header = jwt.get_unverified_header(token)
    print("header: ", header)
    try:
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
        jwks = get_jwks()

        print("jwks: %s" % jwks)
        matching_key = next((key for key in jwks if key["kid"] == kid), None)

        if not matching_key:
            return None
        
        public_key = jwk.JWK(**matching_key)
        payload = jwt.decode(token, public_key.export_to_pem().decode('utf-8'), algorithms=['RS256'])
        return payload
    except Exception as e:
        print(f"JWT Validation Error: {e}")
        return None