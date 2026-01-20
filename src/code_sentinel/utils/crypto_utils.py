import hashlib
import hmac
import logging

from code_sentinel.config import config

logger = logging.getLogger(__name__)

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    verify git webhook signature

    args:
        payload_body: bytes: the request body
        signature_header: header from webhook request
    """
    secret = config.GIT_WEBHOOK_SECRET
    if not secret:
        logger.error("GIT_WEBHOOK_SECRET not set")
        return False

    if not signature_header or  not signature_header.startswith("sha256="):
        logger.error("signature_header not set")
        return False

    hash_obj = hmac.new(
        key=secret.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_obj.hexdigest()

    return hmac.compare_digest(expected_signature, signature_header)
