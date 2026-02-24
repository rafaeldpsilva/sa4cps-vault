# Concepts Notes

## Big Five vs. MBTI

### Big Five (OCEAN)
A **scientific/empirical** model developed through factor analysis of personality data. It treats personality as **continuous dimensions** — everyone sits somewhere on a spectrum for each trait:

- **O**penness — curiosity, creativity, openness to new ideas
- **C**onscientiousness — organization, dependability, self-discipline
- **E**xtraversion — sociability, assertiveness, energy from others
- **A**greeableness — cooperation, trust, empathy
- **N**euroticism — emotional instability, anxiety, moodiness

Key property: **gradients**, not boxes. You're not "an extravert", you score 72% on extraversion.

---

### MBTI (Myers-Briggs Type Indicator)
A **typological** model derived from Jungian psychology. It sorts people into **16 discrete types** using 4 binary axes:

- **I/E** — Introversion vs. Extraversion
- **S/N** — Sensing vs. iNtuition (concrete vs. abstract)
- **T/F** — Thinking vs. Feeling (logic vs. values)
- **J/P** — Judging vs. Perceiving (structured vs. flexible)

Key property: **categories**, not spectra. You *are* an INTJ or ENFP.

---

### Big Five vs. MBTI — Core Difference

| | Big Five | MBTI |
|---|---|---|
| Basis | Empirical/statistical | Theoretical (Jungian) |
| Output | 5 continuous scores | 1 of 16 discrete types |
| Scientific standing | High validity & reliability | Widely criticized for low test-retest reliability |
| Granularity | Fine-grained | Coarse but intuitive |
| Use in AI/ML | Easy to use as feature vectors | Needs encoding, loses nuance |

> For this research, **Big Five is more tractable for ML** — scores map naturally to graph node attributes. MBTI is useful as a vocabulary that users and designers understand intuitively.

---

## Psychographic Profiling vs. Relational Psychographics

### Psychographic Profiling (classical)
Originates in **marketing**. It segments people by:
- Values, attitudes, interests, lifestyles (VALS framework)
- Motivations and worldview

It is essentially a **static snapshot** — you assign someone to a profile bucket (e.g., "achiever", "explorer"). The relationship between attributes is ignored; what matters is *which segment* you belong to.

---

### Relational Psychographics
Instead of asking *"what bucket is this person in?"*, it asks **"how do this person's psychological attributes relate to each other and to their behaviors?"**

The word **relational** is doing heavy lifting here — it means:
- Personality traits, interaction styles, and expectations are modeled as **nodes in a graph**
- The **edges** encode how strongly one attribute influences another (e.g., high neuroticism → low trust in automation)
- The profile is not a label but a **structure**

---

### Psychographic Profiling vs. Relational Psychographics — Core Difference

| | Psychographic Profiling | Relational Psychographics |
|---|---|---|
| Output | Segment / category | Graph structure |
| Captures relationships between traits? | No | Yes |
| Comparable across users? | Via shared categories | Via graph isomorphism |
| Dynamic? | Usually static | Can evolve as edges change weight |
| Origin | Marketing | Research framing (this work) |

---

### Why This Matters for This Research

Classical psychographics would tell you *"User A is an Explorer type"*. Relational psychographics tells you *"User A has high autonomy-preference that strongly inhibits trust in proactive automation, which in turn shapes their preferred modality toward manual override"* — a structure that can be compared, clustered, and used to drive system behavior in a principled way.
