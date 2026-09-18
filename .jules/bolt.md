## 2024-05-24 - Optimizing Redundant NLP Processing

**Learning:** When applying NLP preprocessing (tokenizing, regex matching) to strings that don't change (like a job description) within a loop, use caching or pre-compute to avoid redundant CPU overhead. Python's `functools.lru_cache` provides a drop-in memoization layer for pure functions, easily eliminating duplicated workloads for repeated texts.

**Action:** Whenever looping over data to compare against a static source text, always verify whether the source text is being redundantly processed. Apply `@lru_cache` to text preprocessing, tokenizing, and information extraction functions to ensure repetitive processing hits the cache.
