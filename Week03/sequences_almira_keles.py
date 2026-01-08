from __future__ import annotations

from typing import Any


def remove_duplicates(seq: list) -> list:

    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def list_counts(seq: list) -> dict:

    counts = {}
    for item in seq:
        counts[item] = counts.get(item, 0) + 1
    return counts


def reverse_dict(d: dict) -> dict:

    return {v: k for k, v in d.items()}
