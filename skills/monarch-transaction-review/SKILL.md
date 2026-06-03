---
name: monarch-transaction-review
description: Prepare and review Monarch Money transactions with the Monarch MCP server while learning the user's merchant, category, tag, note, receipt, and recurring spending preferences. Use when the user asks Codex to prepare, review, categorize, tag, annotate, correct, or learn from Monarch transactions, especially unreviewed transactions or transactions tagged for AI preparation/human review.
---

# Monarch Transaction Review

## Core Rule

Never mark a transaction reviewed during AI preparation. Only mark a transaction reviewed during the human review stage after the user explicitly says to mark it reviewed.

Use the Monarch MCP server tools. Prefer exact tool names when available, such as:

- `transactions_list_transactions`
- `transactions_get_transaction`
- `transactions_update_transaction`
- `tags_list_tags`
- `tags_create_tag`

## Private Memory

Read the private memory file before reviewing transactions:

```text
~/.config/monarch/transaction-review-memory.md
```

If it does not exist, create it from `references/memory-template.md` or run:

```bash
python scripts/init_memory.py
```

Do not store personal transaction memory in this skill folder or in a public repo. The memory file should capture:

- merchant cleanup preferences
- category choices
- tag rules
- note-writing style
- receipt expectations
- recurring bills, obligations, subscriptions, and normal spending rhythms
- account-specific or household context
- corrections learned from the user
- open questions the agent should ask about

Only update memory from explicit user corrections, user-provided preferences, or strong repeated patterns. Mark uncertain inferences as tentative.

## Tags

Use these review workflow tags:

- `AI Prepared` (`#3B82F6`): AI prepared the transaction and it is waiting for human review.
- `AI Needs Context` (`#F59E0B`): AI could not confidently decide what to do.

Create missing tags when needed. Preserve unrelated user tags.

## Prepare Transactions

When the user asks to review or prepare transactions:

1. Load memory.
2. Find unreviewed transactions, usually with `filters.needs_review=true`.
3. Inspect enough context to decide safely. Use `output_mode="full"` when summary output lacks needed fields.
4. Apply high-confidence updates to merchant, category, tags, notes, or other editable fields.
5. Add `AI Prepared` when updated or confidently left unchanged for human review.
6. Add `AI Needs Context` when the transaction needs user clarification.
7. Do not set `review_status="reviewed"` in this phase.
8. Summarize actions as: transaction id, merchant/date/amount, changes made, confidence, and questions.

If confidence is low, prefer tagging `AI Needs Context` over guessing.

## Human Review Loop

When the user asks to review, audit, or manually review AI-prepared transactions:

1. Fetch transactions tagged `AI Prepared`, one at a time unless the user asks for a batch.
2. Show the transaction, the current proposed state, and why the agent thinks it is correct.
3. Ask for one of: mark reviewed, correct, needs context, skip.
4. On mark reviewed:
   - remove `AI Prepared`
   - set `review_status="reviewed"`
5. On correct:
   - apply the correction
   - update memory with the lesson
   - ask whether to mark reviewed now
6. On needs context:
   - replace `AI Prepared` with `AI Needs Context`
   - add the open question to memory
7. On skip:
   - leave the transaction unchanged

## Learning Rules

Update memory in concise, durable rules. Prefer rules that will help future transactions:

- Good: "If merchant is Shell and account is checking, categorize as Auto & Transport / Gas unless transaction notes indicate convenience-store purchase."
- Good: "Rent is expected monthly around the first week and usually does not have a receipt."
- Good: "For reimbursable work expenses, tag `Work Reimbursement` and write notes as `Reimbursable: <short reason>`."
- Weak: "Changed transaction abc123 to Gas." Put isolated facts in a correction log only if no general rule is clear.

Record spending habits as context, not as automatic proof. A recurring pattern can raise confidence, but it should not override a conflicting merchant, amount, date, note, or user correction.

## Output Controls

Use compact output by default. Request larger output only when needed:

- `output_mode="summary"` for queues and quick scans
- `output_mode="full"` for editing decisions
- `output_mode="raw"` only when raw API fields are necessary
- `fields=[...]` to limit large responses

## Safety

Treat all financial data as sensitive. Do not print raw payloads, tokens, full account details, or long transaction histories unless necessary. Never delete transactions or make destructive changes as part of review unless the user explicitly asks.
