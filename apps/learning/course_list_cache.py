from hashlib import sha256

from django.core.cache import cache


def _version_key(user_id):
    return f"learning:course-list:version:{user_id}"


def _get_version(user_id):
    key = _version_key(user_id)
    version = cache.get(key)
    if version is not None:
        return version

    if cache.add(key, 1, timeout=None):
        return 1

    version = cache.get(key)
    if version is None:
        raise RuntimeError("course-list cache version unavailable")

    return version


def _payload_key(user_id, version, keyword, page):
    keyword_digest = sha256(keyword.encode("utf-8")).hexdigest()
    return f"learning:course-list:payload:{user_id}:{version}:{keyword_digest}:{page}"


def get_cached_course_payload(*, user_id, keyword, page, loader):
    try:
        version = _get_version(user_id)
        key = _payload_key(user_id, version, keyword, page)
        cached_payload = cache.get(key)
    except Exception:
        return loader()

    if cached_payload is not None:
        return cached_payload

    payload = loader()

    try:
        cache.set(key, payload)
    except Exception:
        pass

    return payload


def invalidate_course_list(user_id):
    key = _version_key(user_id)

    try:
        if cache.add(key, 2, timeout=None):
            return
        cache.incr(key)
    except Exception:
        pass
