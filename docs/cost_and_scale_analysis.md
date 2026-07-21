# Cost & Scale Analysis

Data source: LangFuse's public API (`/api/public/traces`, `/api/public/observations`), queried directly against today's local instance — 51 real `/ask` traces from today's manual testing plus the `golden_set_eval.py` run. Not estimates.

## Current cost per query

Average total cost across all 51 traces: **$0.000862/query** (median $0.000973; range $0.000 – $0.00111). That's every LLM call the request makes: generation plus both judges. Breakdown by call:

| Call | Avg cost | % of total | Avg tokens |
|---|---|---|---|
| Generation (gpt-4o-mini) | $0.000436 | 50.5% | 2,330 |
| Groundedness judge | $0.000355 | 41.2% | 2,321 |
| Relevance judge | $0.000071 | 8.2% | 378 |

The two judges together are **49.5% of per-query cost** — almost exactly doubling what generation alone would cost. The groundedness judge specifically is nearly as expensive as generation itself, and the reason is visible in the token counts: it re-sends the full retrieved context (same ~2,300 tokens as generation) to check the answer against it, whereas the relevance judge only needs question+answer (~378 tokens) and costs 5x less. This isn't a guess — it's what the token counts show directly.

## Projected monthly cost (simple multiplication — not a load test)

| Volume | Monthly cost |
|---|---|
| 100 queries/day | ~$2.59 |
| 1,000 queries/day | ~$25.86 |
| 10,000 queries/day | ~$258.60 |

At 10,000/day, judges alone account for roughly $128/month of that — the single largest lever for cost control at scale (see optimization c).

## Latency and concurrency at scale

Average end-to-end latency: **10.5s/query** (median 10.2s). Breaking down where it goes: retrieval (embed + Qdrant query) ~3.7s, generation ~4.6s, then both judges concurrently via `asyncio.gather` (~1.6s, the slower of the two — this part is already parallelized correctly). Those three stages are sequential and together account for ~9.9s of the 10.5s observed.

FastAPI's async handler means concurrent *requests* don't block each other at the process level — the event loop can serve multiple users' `/ask` calls in parallel. The actual bottleneck at higher volume is external: **each user-visible query fires 3 separate OpenAI API calls** (generation + 2 judges), so 10,000 queries/day is really ~30,000 chat completion calls/day against OpenAI's per-key rate limits, and bursty traffic (not the daily average) is what would actually trip a rate limit, not the raw volume. There's no queueing, retry-with-backoff, or backpressure handling for that today — a burst simply produces failed requests.

## Three optimizations, ranked by effort-to-impact

**a) Response caching (high impact, low effort).** There is no caching layer today — confirmed by reading `retrieval.py`/`generation.py`; the only cache in the codebase is a one-time equipment-ID lookup, unrelated to answers. The UI's five example chips point users at the same fixed questions repeatedly, and those would be pure cache hits. An exact-match cache keyed on the normalized question string would eliminate the full $0.000862 and 10.5s for any repeat, for a few lines of code.

**b) Non-blocking judges (medium impact, medium effort).** Confirmed: `/ask` currently awaits `generate_answer()`, which awaits both judges before returning — the user's response is blocked on the ~1.6s judge step even though the frontend could show the answer first and the Grounded/Relevant badges a moment later. This saves latency (~15%), not cost (the judges still run either way), and requires a real UX change: the badges currently render synchronously with the answer, so making this async means a second round-trip or a loading state for those specific badges.

**c) Cheaper judge path (medium-high impact on cost, medium-high effort).** The groundedness judge's cost comes from re-sending the same ~2,300-token context as generation. Since `generate_answer` already knows which chunks got cited in the answer, passing the judge only the cited chunks instead of the full retrieved set would cut its input tokens substantially without changing what it's actually verifying.

## What's not handled

No rate limiting, no per-user quota, and no caching layer exist today. A single user (or a bug in a client) can currently fire unlimited concurrent `/ask` requests, each costing real money and consuming three OpenAI API calls, with nothing in front of it to throttle, deduplicate, or queue. These are known gaps, not hidden ones — acceptable for a hackathon demo at low volume, not for production traffic.
