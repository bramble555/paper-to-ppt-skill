from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class PaperMetadata(BaseModel):
    title: str = "Untitled Paper"
    authors: List[str] = Field(default_factory=list)
    venue: str | None = None
    year: str | None = None


class ParsedSection(BaseModel):
    name: str
    content: str


class ParsedPaper(BaseModel):
    metadata: PaperMetadata
    abstract: str | None = None
    sections: List[ParsedSection] = Field(default_factory=list)
    references_count: int = 0


class Slide(BaseModel):
    section: str
    title: str
    bullets: List[str]
    speaker_notes: str


class SlidePlan(BaseModel):
    deck_title: str
    slides: List[Slide]
