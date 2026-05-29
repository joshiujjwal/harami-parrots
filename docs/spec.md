# Harami Parrots — Feature Spec

## Overview

**Problem**: Quality satirical content about Indian society and global half-baked ideas is either too polished (loses edge) or too shallow (no research). There's no podcast that combines genuine research depth with unhinged parrot personas.

**Solution**: A production pipeline that uses AI (Grok + Gemini + NotebookLM) to generate research briefs and script drafts, which humans then refine and record. The output is a Hinglish podcast where three parrot personas dismantle one idea per episode.

---

## Functional Requirements

### Research Pipeline
- [ ] Accept episode ID (e.g., `S1E01`) and return structured research brief
- [ ] Pull real-time social/news context via Grok API
- [ ] Synthesize long-form sources (reports, articles) via Gemini 1.5 Pro
- [ ] Output brief as structured Markdown with sections: Context, Key Facts, Data Points, Counterarguments, Sources
- [ ] Support manual NotebookLM workflow via prompt templates

### Script Generation
- [ ] Accept research brief + episode premise → return full script draft
- [ ] Script must follow structure: Cold Open → Setup → Teardown → Chaos → Verdict
- [ ] Each parrot's voice must match persona definitions in `prompts/parrot_personas.md`
- [ ] Language: Hinglish (configurable per episode if needed)
- [ ] Output as Markdown with speaker labels: `**MITHAI:**`, `**KADDU:**`, `**BIJLI:**`

### Fact Checking
- [ ] Extract factual claims from a script
- [ ] Verify each claim via Grok/Gemini with source citations
- [ ] Flag unverified or potentially wrong claims
- [ ] Output annotated script with verification status per claim

### CLI Scripts
- [ ] `generate_research.py --episode S1E01` → research brief
- [ ] `generate_script.py --episode S1E01 --draft 1` → script draft
- [ ] `fact_check_script.py --script path/to/script.md` → annotated script
- [ ] `new_episode.py --id S2E01 --title "..." --idea "..."` → episode scaffold

---

## Non-Functional Requirements

- [ ] All API calls must be async (no blocking I/O)
- [ ] Graceful degradation if one AI provider is unavailable (fallback order: Gemini → Grok)
- [ ] API rate limiting with exponential backoff
- [ ] No API keys in code — env vars only
- [ ] Test coverage > 80% on `src/pipeline/`
- [ ] Script generation < 60 seconds for a full episode draft

---

## Data Model

```python
@dataclass
class EpisodeMeta:
    id: str              # "S1E01"
    season: int
    episode: int
    title: str
    premise: str         # The half-baked idea being roasted
    angle: str           # The specific lens/approach

@dataclass
class ResearchBrief:
    episode_id: str
    context: str         # Why does this idea exist? Who believes it?
    key_facts: list[str] # Verified facts with sources
    data_points: list[DataPoint]
    counterarguments: list[str]
    sources: list[Source]
    generated_at: datetime
    models_used: list[str]

@dataclass
class Script:
    episode_id: str
    draft_number: int
    content: str         # Full Markdown script
    word_count: int
    estimated_duration_min: float
    generated_at: datetime
    fact_check_status: str  # "pending" | "passed" | "flagged"
```

---

## API / Interface Design

### `researcher.py`
```python
async def generate_research_brief(episode: EpisodeMeta) -> ResearchBrief
async def fetch_realtime_context(query: str) -> str   # Grok
async def synthesize_sources(sources: list[str]) -> str  # Gemini
```

### `script_writer.py`
```python
async def generate_script(episode: EpisodeMeta, brief: ResearchBrief, draft: int = 1) -> Script
async def rewrite_section(script: Script, section: str, notes: str) -> Script
```

### `fact_checker.py`
```python
async def check_script(script: Script) -> AnnotatedScript
async def verify_claim(claim: str) -> ClaimVerification
```

---

## Test Plan

### Unit Tests
- `researcher.py`: mock Grok/Gemini responses, test output schema validation
- `script_writer.py`: mock brief input, verify all three parrots appear in output
- `fact_checker.py`: mock claim extraction, test verification flow

### Integration Tests
- Full pipeline: `EpisodeMeta → ResearchBrief → Script` (with mocked APIs)
- CLI scripts: test argument parsing and output file creation

### Edge Cases
- API timeout → should retry with backoff, not crash
- Empty research brief → script generation should refuse, not hallucinate
- Missing parrot in generated script → flag as error, not silently pass
- Non-Hinglish output → add language validation check

---

## Open Questions

- [ ] NotebookLM API access — public API not available as of 2024. Use manual prompt workflow or monitor for API release?
- [ ] TTS voice design — which engine best captures parrot-like cadence? Needs A/B test.
- [ ] Gemini Nano vs Gemini 1.5 Pro — Nano is on-device, not available via API. Use 1.5 Pro for pipeline.
- [ ] Episode length target — 25 min vs 35 min? Affects script word count target.
- [ ] Video generation — Gemini video gen or Sora/Runway for animated parrot visuals?
