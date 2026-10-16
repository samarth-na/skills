# Excalidraw as a communication canvas

An Excalidraw board is a more extensible canvas than markdown: it holds diagrams, screenshots, links, and notes in one persistent surface. When a board session is active, prefer the board for durable content and keep chat for short coordination.

This is an opt-in default, not a mandate. If there is no active board, reply in chat as normal. Never create a board just to deliver a reply. If a reply is growing board-shaped (several links, screenshots, or a long summary) and no board exists, offer once in one line — "want me to put this on a board?" — and create it only on yes.

## When a board session is active

A session is active when the user opened a board, asked for a diagram, or is iterating on one with you. While active, treat the board as the primary surface:

- **Screenshots and images** go on the board as `image` elements (see [scene-format.md](./scene-format.md), images section), not as a flood of chat attachments.
- **Links** go on the element itself (`link` field) plus a short visible label. A clickable shape with no visible text is not communication.
- **End-of-session summaries, decisions, and open questions** go into the board's notes frame instead of a long chat reply.
- Anything the user will need next session goes on the board. The file persists in `~/.opencode/excalidraw/`; chat scrolls away.

## What stays in chat

- One or two lines after a board update: what changed, which file.
- Direct answers to direct questions.
- Errors, blockers, anything needed right now. Never let a board update delay a needed answer.
- Anything that fits in a few lines stays in chat, even with an active board.

## Board notes, kept simple

1. Keep **one** notes frame per board (id `notes`, name it "Session notes"). Place it below or beside the main content, never overlapping it.
2. Append timestamped entries, newest at bottom. A few short lines each.
3. Use short lines and enough space. Inspect the changed area in the preview when layout changes.
4. Save the canonical file, rebuild the preview, then send one chat line: what you added and where.
5. Batch updates at natural breakpoints (task done, session end), not after every micro-step.

## Don'ts

- Don't narrate chain-of-thought on the board. Notes are conclusions, decisions, links — not process.
- Don't create a board uninvited. Offer first; create only on yes.
- Don't move an ongoing conversation onto the board mid-stream. If the user is talking, talk back.
- Don't let layout fuss inflate the work. Rough and readable beats pixel-perfect.
