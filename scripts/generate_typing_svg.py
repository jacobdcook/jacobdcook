#!/usr/bin/env python3
"""Generate assets/typing.svg — a self-hosted animated typing tagline.

Pure SMIL animation (no scripts, no external services), so it works when
GitHub serves it through camo as image/svg+xml. Each phrase types in
character by character, holds, then yields to the next phrase, looping
forever. Deterministic output: safe to re-run and diff.
"""
import html
import os

PHRASES = [
    "behavioral Sigma detections mapped to ATT&CK",
    "Wazuh SIEM deployment and tuning",
    "identity attack detection: Okta / Azure / AWS",
    "SOAR response automation in Python",
    "false positives documented before you ask",
]

WIDTH, HEIGHT = 720, 44
FONT = "'Cascadia Code', 'Fira Code', Consolas, 'Courier New', monospace"
COLOR = "#2f80ed"
PROMPT_COLOR = "#8b949e"
TYPE_TIME = 1.4    # seconds spent typing each phrase
HOLD_TIME = 1.8    # seconds each phrase stays on screen after typing
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "typing.svg")


def fmt(t):
    return f"{t:.3f}".rstrip("0").rstrip(".")


def main():
    cycle = len(PHRASES) * (TYPE_TIME + HOLD_TIME)
    parts = [
        f'<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape("; ".join(PHRASES))}">',
    ]
    for i, phrase in enumerate(PHRASES):
        start = i * (TYPE_TIME + HOLD_TIME)
        end = start + TYPE_TIME + HOLD_TIME
        # Visibility gate for the whole phrase (discrete: on at start, off at end).
        gate_times = f"0;{fmt(start / cycle)};{fmt(end / cycle)}"
        gate_values = "0;1;0" if start > 0 else "1;1;0"
        parts.append(
            f'<text x="{WIDTH // 2}" y="29" text-anchor="middle" opacity="0" '
            f'font-family="{FONT}" font-size="24" font-weight="600" fill="{COLOR}">'
            f'<animate attributeName="opacity" values="{gate_values}" '
            f'keyTimes="{gate_times}" calcMode="discrete" '
            f'dur="{fmt(cycle)}s" repeatCount="indefinite"/>'
        )
        # Everything inside <text> must be one whitespace-free run: newlines or
        # raw spaces between tspans render as extra glyph gaps.
        run = [f'<tspan fill="{PROMPT_COLOR}">&gt;&#160;</tspan>']
        per_char = TYPE_TIME / max(len(phrase), 1)
        for j, ch in enumerate(phrase):
            t_on = (start + (j + 1) * per_char) / cycle
            glyph = "&#160;" if ch == " " else html.escape(ch)
            run.append(
                f'<tspan opacity="0">{glyph}'
                f'<animate attributeName="opacity" values="0;1" '
                f'keyTimes="0;{fmt(t_on)}" calcMode="discrete" '
                f'dur="{fmt(cycle)}s" repeatCount="indefinite"/></tspan>'
            )
        # Blinking cursor, alive only while this phrase is visible (parent gates it).
        run.append(
            '<tspan>_<animate attributeName="opacity" values="1;0" keyTimes="0;0.5" '
            'calcMode="discrete" dur="1.06s" repeatCount="indefinite"/></tspan>'
        )
        parts.append("".join(run) + "</text>")
    parts.append("</svg>")
    svg = "\n".join(parts) + "\n"
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {os.path.normpath(OUT)} ({len(svg)} bytes, {fmt(cycle)}s cycle)")


if __name__ == "__main__":
    main()
