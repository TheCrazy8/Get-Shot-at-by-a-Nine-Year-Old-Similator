"""Bullet data structures for unified bullet tracking (Step 3).

This transitional module introduces a Bullet dataclass and light-weight
registration helpers. Existing per-pattern lists remain the source of
truth until Step 5 migrates logic fully; we maintain a unified view for
future dispatch, collision optimization, and replay compression.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass(slots=True)
class Bullet:
    item_id: int            # Canvas item id
    kind: str               # Pattern/category name (e.g., 'vertical', 'spiral')
    vx: float = 0.0         # Optional velocity X (may be unused for some kinds)
    vy: float = 0.0         # Optional velocity Y
    life: int = -1          # Generic life counter / ttl frames (-1 = infinite)
    extra: Dict[str, Any] = field(default_factory=dict)  # Arbitrary pattern-specific fields

    def set(self, **kwargs):  # fluent helper
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self.extra[k] = v
        return self

class BulletRegistry:
    """Central registry for active bullets.

    This sits alongside legacy lists for now. After full migration the
    per-pattern arrays will be removed and update / collision logic will
    iterate registry contents.
    """
    __slots__ = ("bullets_all", "by_id")

    def __init__(self):
        self.bullets_all: list[Bullet] = []
        self.by_id: dict[int, Bullet] = {}

    def register(self, bullet: Bullet) -> Bullet:
        if bullet.item_id in self.by_id:
            return self.by_id[bullet.item_id]
        self.by_id[bullet.item_id] = bullet
        self.bullets_all.append(bullet)
        return bullet

    def get(self, item_id: int) -> Optional[Bullet]:
        return self.by_id.get(item_id)

    def remove(self, item_id: int):
        b = self.by_id.pop(item_id, None)
        if b is None:
            return
        try:
            self.bullets_all.remove(b)
        except ValueError:
            pass

    def clear(self):
        self.bullets_all.clear()
        self.by_id.clear()
