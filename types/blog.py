from dataclasses import dataclass, field
from typing import Optional

@dataclass
class BlogPostInput:
    topic: str
    tone: str = 'informative'
    length: str = 'medium'
    language: str = 'ko'
    tags: list = field(default_factory=list)
    seo_keywords: list = field(default_factory=list)
    created_by: str = 'opencrew'

@dataclass
class BlogPostDraft:
    title: str
    content: str
    topic: str
    raw_output: str = ''

@dataclass
class BlogPostResult:
    success: bool
    title: object = None
    content_preview: object = None
    error: object = None

LENGTH_MAP = {'short':300,'medium':600,'long':1200}