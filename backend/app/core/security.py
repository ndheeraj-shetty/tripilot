import hmac
import hashlib
import time
import base64
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

SECRET_KEY = "trainpilot_super_secret_production_key_change_in_env"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 # 24 Hours

def hash_password(password: str) -> str:
    """Secure password hashing using SHA256 HMAC digest with salt."""
    salt = "trainpilot_salt_v1"
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return base64.b64encode(key).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against the stored hash."""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Generates a secure HMAC-SHA256 signed JSON Web Token (JWT)."""
    to_encode = data.copy()
    expire = time.time() + (expires_delta or ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": int(expire)})

    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip("=")

    signature_base = f"{header}.{payload}"
    signature = base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), signature_base.encode(), hashlib.sha256).digest()
    ).decode().rstrip("=")

    return f"{signature_base}.{signature}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and verifies a JWT token signature and expiration."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts
        signature_base = f"{header_b64}.{payload_b64}"

        # Recompute signature
        expected_sig = base64.urlsafe_b64encode(
            hmac.new(SECRET_KEY.encode(), signature_base.encode(), hashlib.sha256).digest()
        ).decode().rstrip("=")

        if not hmac.compare_digest(expected_sig, signature_b64):
            logger.warning("JWT verification failed: Signature mismatch")
            return None

        # Decode payload
        padded_payload = payload_b64 + "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded_payload).decode())

        if payload.get("exp", 0) < time.time():
            logger.warning("JWT verification failed: Token expired")
            return None

        return payload
    except Exception as e:
        logger.error(f"JWT decode error: {e}")
        return None
