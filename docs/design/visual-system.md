# Visual System v0.1

## Direction

Calm, technical, and evidence-first. The interface should feel like an operator console rather than a speculative trading screen: dark navy surfaces, restrained cyan accent, green only for confirmed states, and amber for caveats.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | `#07111F` | page background |
| `--panel` | `#0D1A2B` | cards and panels |
| `--line` | `#203650` | borders and table rules |
| `--text` | `#EDF4FF` | primary text |
| `--muted` | `#8DA3BD` | secondary text |
| `--cyan` | `#54D6E5` | primary action and focus |
| `--green` | `#63E6A5` | confirmed / selected |
| `--amber` | `#F4C66A` | warning / stale |
| `--red` | `#FF7D8F` | failure or destructive state |

## Components

- **Metric card**: one label, one large value, one short interpretation.
- **State flow**: completed nodes use green; active node uses cyan; unavailable nodes remain muted.
- **Quote table**: show raw price and all-in price side by side; never hide cost assumptions.
- **Route card**: the selected decision gets the strongest visual contrast.
- **Audit trail**: chronological, compact, and reason-oriented.

## Responsive rules

- Desktop: two-column content, evidence on the left and selected route on the right.
- Tablet: stack content while keeping the route card above the table.
- Mobile: preserve horizontal scrolling for state flow and quote table; do not squeeze numeric columns.

## Accessibility

Color is never the only state signal: every state has a label or icon. Body text targets readable contrast, controls are keyboard-focusable, and tables retain semantic headers.
