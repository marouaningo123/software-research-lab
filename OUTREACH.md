# Launch copy

**Marouane Mouhajar · Expert AI Researcher**
marouane.mouhajar@gmail.com

Replace PUBLIC_REPO_URL with the live GitHub URL before posting. Each draft invites critique on a specific design choice.

## LinkedIn

I am opening a research portfolio with ten reproducible proposals in software engineering and computer systems.

The first question comes from a failure window familiar to teams running message queues. A worker commits to PostgreSQL, crashes before acknowledging RabbitMQ, and the same message arrives again. What happens if the deduplication record has already been compacted?

The repository also covers fault injection, flaky CI, authorization views, API caching, storage and PHP refactoring. Each protocol includes its sources, a baseline, a failure case and a decision criterion. The charts show model outputs. The next milestone is a real Symfony Messenger benchmark.

If you have worked on inbox/outbox retention or broker replay, I would welcome counterexamples to the proposed late-message policy.

PUBLIC_REPO_URL

## Systems and distributed software groups

I am looking for critique of a proposed comparison between an append-only SQL workflow ledger and a compacted one. Both versions use the same fault schedules and must preserve the same business invariants. Which broker or operator replay scenarios would invalidate a bounded deduplication horizon?

The repository includes the protocol, a small counterexample model, ten research proposals and reproducible curves. PUBLIC_REPO_URL

## PHP and Symfony groups

How do you test a Messenger handler when PostgreSQL commits but the worker crashes before the RabbitMQ acknowledgment? I have published an experimental design for that failure window and for late replay after compaction. I would like feedback on replay horizons and on practical scenarios for a public benchmark. PUBLIC_REPO_URL

## Short-form social post

Ten software research protocols, executable models and reproducible figures. First experiment: can you compact a Symfony Messenger retry ledger without letting an old replay duplicate a committed reservation? Counterexamples welcome. PUBLIC_REPO_URL
