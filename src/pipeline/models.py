from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class EpisodeMeta:
    id: str  # "S1E01"
    season: int
    episode: int
    title: str
    premise: str  # The half-baked idea being roasted
    angle: str  # The specific lens/approach


@dataclass
class DataPoint:
    value: str
    source: str
    year: Optional[int] = None


@dataclass
class Source:
    title: str
    url: Optional[str] = None
    type: str = "article"  # article | report | paper | book


@dataclass
class ResearchBrief:
    episode_id: str
    context: str
    key_facts: list[str]
    data_points: list[DataPoint]
    counterarguments: list[str]
    sources: list[Source]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    models_used: list[str] = field(default_factory=list)


@dataclass
class Script:
    episode_id: str
    draft_number: int
    content: str  # Full Markdown script
    word_count: int
    estimated_duration_min: float
    generated_at: datetime = field(default_factory=datetime.utcnow)
    fact_check_status: str = "pending"  # pending | passed | flagged


@dataclass
class ClaimVerification:
    claim: str
    status: str  # verified | unverified | false | uncertain
    source: Optional[str] = None
    confidence: float = 0.0


@dataclass
class AnnotatedScript:
    script: Script
    verifications: list[ClaimVerification]
    flagged_count: int
    verified_count: int
