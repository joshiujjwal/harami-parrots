# NotebookLM Research Guide — Harami Parrots

## How to Use This

Upload source documents to NotebookLM, then use these query templates to extract structured research for each episode section.

---

## Query Templates

### 1. Context & Origin
```
What is the historical origin of [IDEA]? When and where did this idea first emerge? 
Who were the key proponents and what was their motivation?
```

### 2. Evidence & Data
```
What quantitative evidence exists about [IDEA]? 
List specific statistics with sources, years, and geographical context.
Focus on India-specific data where available, then global comparisons.
```

### 3. Failures & Precedents
```
Where has [IDEA] been tried before and what were the results?
Give specific country/city examples with outcomes and timeframes.
Include both successes and failures.
```

### 4. Who Benefits
```
Who are the primary beneficiaries of [IDEA]?
What are the economic incentives of those who promote it?
Who bears the costs or risks?
```

### 5. Strongest Counterargument
```
What is the strongest, most well-evidenced argument IN FAVOR of [IDEA]?
What do its most credible supporters say? What evidence do they cite?
```

### 6. Expert Consensus
```
What is the current expert consensus on [IDEA]?
Are there meaningful disagreements among experts? What divides them?
```

---

## Podcast-Specific Extraction

After initial research, run this prompt to format for the show:

```
Based on all the sources, create a research brief for a satirical podcast episode about:
IDEA: [IDEA]

Format your response as:

CONTEXT (2-3 sentences): Why this idea exists and who believes it

KEY_FACTS (5 bullet points): Most important verifiable facts with sources

BEST_STAT (1 devastating statistic): The number that best captures the absurdity

HISTORICAL_PARALLEL: One specific past example of this failing

STRONGEST_DEFENSE: The best argument in favor of the idea

MITHAI_MOMENT: The quote/fact that would make an optimist still believe
KADDU_MOMENT: The historical precedent that destroys the idea  
BIJLI_MOMENT: The data point that closes the argument
```

---

## Source Quality Guide

| Type | Use for | Trust level |
|------|---------|-------------|
| Government reports (NITI Aayog, MoF) | Policy data | High (but check date) |
| IMF / World Bank reports | Economic comparisons | High |
| Academic papers (peer-reviewed) | Research claims | High |
| Think tank reports (CPR, IDFC, PRS) | India policy analysis | High |
| Business journalism (Mint, ET, Bloomberg) | Recent events | Medium |
| LinkedIn / Twitter discourse | Social sentiment | Low (but useful for Grok section) |
| Self-help books / TED talks | What people believe | Low (this is the joke) |
