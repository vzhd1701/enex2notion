import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class EvernoteResource(object):
    data_bin: bytes
    size: int
    md5: str
    mime: str
    file_name: str


@dataclass
class EvernoteNote(object):
    title: str
    created: datetime
    updated: datetime
    content: str  # noqa: WPS110
    tags: List[str]
    author: str
    url: str
    is_webclip: bool
    resources: List[EvernoteResource]
    _note_hash: str = None

    def resource_by_md5(self, md5):
        for resource in self.resources:
            if resource.md5 == md5:
                return resource
        return None

    @property
    def note_hash(self):
        if self._note_hash is None:
            hashable = [
                self.title,
                self.created.isoformat(),
                self.updated.isoformat(),
                self.content,
                "".join(self.tags),
                self.author,
                self.url,
            ]

            s1_hash = hashlib.sha1()
            for h in hashable:
                s1_hash.update(h.encode("utf-8"))
            self._note_hash = s1_hash.hexdigest()  # noqa: WPS601

        return self._note_hash
