"""Static URL feature extraction. Never resolves or requests the submitted URL."""
from __future__ import annotations
import ipaddress
import math
import re
from collections import Counter
from urllib.parse import urlsplit

SUSPICIOUS_TERMS = {
    "login", "verify", "update", "secure", "account", "password",
    "confirm", "wallet", "signin", "payment", "bank", "suspend"
}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "ow.ly"}

def extract_features(raw_url: str) -> dict[str, float]:
    if not isinstance(raw_url, str) or not raw_url.strip():
        raise ValueError("url must be a non-empty string")
    candidate = raw_url.strip()
    if len(candidate) > 2048:
        raise ValueError("url exceeds 2048 characters")
    parsed = urlsplit(candidate if "://" in candidate else "//" + candidate)
    host = (parsed.hostname or "").lower().rstrip(".")
    if not host:
        raise ValueError("URL must contain a hostname")
    try:
        ipaddress.ip_address(host)
        host_is_ip = 1
    except ValueError:
        host_is_ip = 0

    labels = [part for part in host.split(".") if part]
    tokens = re.findall(r"[a-z0-9]+", candidate.lower())
    entropy_counts = Counter(candidate.lower())
    entropy = -sum((count / len(candidate)) * math.log2(count / len(candidate))
                   for count in entropy_counts.values())
    lowered = candidate.lower()
    return {
        "url_length": float(len(candidate)),
        "host_length": float(len(host)),
        "host_is_ip": float(host_is_ip),
        "https": float(parsed.scheme.lower() == "https"),
        "at_symbol": float("@" in candidate),
        "hyphen_count": float(host.count("-")),
        "dot_count": float(host.count(".")),
        "subdomain_count": float(max(0, len(labels) - 2)),
        "digit_ratio": float(sum(ch.isdigit() for ch in host) / max(1, len(host))),
        "suspicious_term_count": float(sum(term in tokens for term in SUSPICIOUS_TERMS)),
        "has_punycode": float("xn--" in host),
        "has_nonstandard_port": float(parsed.port not in (None, 80, 443)),
        "path_depth": float(len([p for p in parsed.path.split("/") if p])),
        "query_parameter_count": float(len([p for p in parsed.query.split("&") if p])),
        "fragment_present": float(bool(parsed.fragment)),
        "known_shortener": float(host in SHORTENERS),
        "url_entropy": float(entropy),
    }

FEATURE_NAMES = list(extract_features("https://example.test/").keys())
