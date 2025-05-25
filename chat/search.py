import hashlib
import requests
from django.core.cache import cache

def make_cache_key(prefix: str, query: str) -> str:
    return f"{prefix}:{hashlib.md5(query.encode('utf-8')).hexdigest()}"

def extract_text_from_related(topics):
    texts = []
    for topic in topics:
        if "Text" in topic:
            texts.append(topic["Text"])
        elif "Topics" in topic:
            texts.extend(extract_text_from_related(topic["Topics"]))
    return texts

def search_duckduckgo(query: str) -> str:
    cache_key = make_cache_key("ddg_search", query)
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        response = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_redirect": 1, "skip_disambig": 1},
            timeout=5
        )
        data = response.json()
        answer = data.get("AbstractText", "")
        if not answer:
            related = extract_text_from_related(data.get("RelatedTopics", []))
            answer = " ".join(related[:3]) if related else "Извините, не нашёл ответа по вашему запросу."
    except Exception:
        answer = "Извините, произошла ошибка при поиске. Попробуйте позже."

    cache.set(cache_key, answer, timeout=3600)
    return answer
