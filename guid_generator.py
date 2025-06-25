from hashlib import sha1
from uuid import UUID

from typing import Any

def _transform_for_rfc4122(hash_bytes: bytes) -> bytes:
    new_hash_bytes = [hash_bytes[index : index + 1] for index in range(len(hash_bytes))]
    new_hash_bytes[6] = int.to_bytes((hash_bytes[6] & 0x0F) | 0x40, 1, "big")
    new_hash_bytes[8] = int.to_bytes((hash_bytes[8] & 0x3F) | 0x80, 1, "big")
    return b"".join(new_hash_bytes)

def _compute_hash(value: str) -> bytes:
    return sha1(value.encode()).digest()[:16]

def get_guid_from_value(value: Any) -> str:
    value = str(value)

    hash_bytes: bytes = _compute_hash(value)
    hash_bytes = _transform_for_rfc4122(hash_bytes)
    return UUID(bytes=hash_bytes, version=4).__str__()
