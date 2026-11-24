# /// script
# requires-python = ">=3.11"
# dependencies = ["genanki>=0.13", "markdown>=3.5"]
# ///
"""Build every generated artifact from the sources of truth.

questions/questions.json       -> questions/practice-questions.md, questions/quiz.html
anki/flashcards.csv            -> anki/ccar-f-flashcards.apkg
lessons/*.md + exercises/*.md  -> study-guide.html (with the question bank embedded)

Run: uv run build.py
"""
import csv
import html
import json
import re
from collections import Counter
from pathlib import Path

import genanki
import markdown

ROOT = Path(__file__).parent
# id: (name, weight %, practice questions)
DOMAINS = {
    "D1": ("Agentic Architecture & Orchestration", 27, 16),
    "D2": ("Tool Design & MCP Integration", 18, 11),
    "D3": ("Claude Code Configuration & Workflows", 20, 12),
    "D4": ("Prompt Engineering & Structured Output", 20, 12),
    "D5": ("Context Management & Reliability", 15, 9),
}
SCENARIOS = [
    "Customer Support Resolution Agent",
    "Code Generation with Claude Code",
    "Multi-Agent Research System",
    "Developer Productivity with Claude",
    "Claude Code for Continuous Integration",
    "Structured Data Extraction",
]


def check(qs):
    assert len(qs) == 60, f"expected 60 questions, got {len(qs)}"
    assert [q["id"] for q in qs] == list(range(1, 61)), "ids must run 1..60 in order"
    counts = Counter(q["domain"] for q in qs)
    for d, (_, _, n) in DOMAINS.items():
        assert counts[d] == n, f"{d}: expected {n} questions, got {counts[d]}"
    for q in qs:
        i = q["id"]
        assert q["domain"] in DOMAINS, i
        assert q["scenario"] in SCENARIOS, f"Q{i} scenario {q['scenario']!r}"
        assert q["objective"].startswith(q["domain"][1] + "."), f"Q{i} objective must start with its task statement number"
        assert set(q["answer"]) <= set(q["options"]), i
        assert len(q["answer"]) == q.get("select", 1), i
        assert set(q["wrong"]) == set(q["options"]) - set(q["answer"]), f"Q{i} wrong-option notes"


def build_markdown(qs):
    counts = Counter(q["domain"] for q in qs)
    out = [
        "# Practice Questions: CCAR-F",
        "",
        "Sixty original, scenario-based questions in the style of the Claude Certified Architect – Foundations exam. "
        "They are written for this course and are not drawn from the live exam, whose content is confidential. "
        "Each question sits in one of the six official exam scenarios and tests one task statement from the Exam Guide.",
        "",
        "**How to use this bank**",
        "",
        "- **Timed run:** 60 questions in 120 minutes (2 minutes each, the real exam's pace). Open an answer only after you commit.",
        "- **Interactive:** open `quiz.html` (or the Practice tab of `../study-guide.html`) for click-to-check practice with a score tracker and domain filter.",
        "- **Multiple-response items** say \"Choose TWO\". Score them all-or-nothing.",
        "- **Review every miss.** Write down which distractor pattern caught you (Lesson 06).",
        "",
        "| Domain | Weight | Questions |",
        "|---|---|---|",
    ]
    for d, (name, w, _) in DOMAINS.items():
        ids = [q["id"] for q in qs if q["domain"] == d]
        out.append(f"| {d} {name} | {w}% | {counts[d]} (Q{ids[0]}–Q{ids[-1]}) |")
    out += [
        "",
        "**Distractor patterns** named in the explanations: *prompt as policy*, *over-engineering*, *bigger model*, "
        "*unreliable proxy*, *invented feature*, *hide or kill the error*.",
        "",
        "**Readiness bands** (rough guide, not calibrated to the scaled score): 52–60 strong, 45–51 close, "
        "36–44 keep studying your weakest domains, below 36 restart with the lessons.",
    ]
    current = None
    for q in qs:
        if q["domain"] != current:
            current = q["domain"]
            out += ["", "---", "", f"## {current}: {DOMAINS[current][0]}"]
        select = q.get("select", 1)
        stem = q["stem"]
        if select > 1 and "Choose" not in stem:
            stem += f" **(Choose {['', 'ONE', 'TWO', 'THREE'][select]}.)**"
        out += ["", f"### Q{q['id']}", "", f"*Scenario: {q['scenario']}*", "", stem, ""]
        out += [f"- {k}. {v}" for k, v in q["options"].items()]
        ans = ", ".join(q["answer"])
        out += ["", "<details><summary>Answer</summary>", "", f"**Answer: {ans}**", "", f"**Why {ans} wins:** {q['why']}", ""]
        out += [f"- **{k} fails:** {v}" for k, v in q["wrong"].items()]
        out += ["", f"*Task statement:* {q['objective']}", "", "</details>"]
    (ROOT / "questions" / "practice-questions.md").write_text("\n".join(out) + "\n")


QUIZ = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CCAR-F Practice Quiz</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{--cream:#f5f0e6;--paper:#fff;--ink:#1a1a1a;--muted:#6b6559;--line:#ddd5c0;--accent:#b85c1f;--ok:#4d8a3a;--bad:#c0392b;--okbg:#f2f7ef;--badbg:#fbefe4}
@media (prefers-color-scheme:dark){:root{--cream:#1c1c1c;--paper:#262626;--ink:#f5f0e6;--muted:#b8b2a4;--line:#3a3a3a;--okbg:#1f2e1b;--badbg:#3a2418}}
*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:16px/1.45 Inter,-apple-system,sans-serif}
header{position:sticky;top:0;background:var(--ink);color:var(--cream);padding:12px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:2}
header h1{font-size:18px;margin:0;font-weight:800}header .score{margin-left:auto;font-weight:700;color:#e7c548}
header select,header button{font:inherit;padding:4px 8px;border-radius:4px;border:0}
main{max-width:860px;margin:0 auto;padding:16px}
.q{background:var(--paper);border:2px solid var(--ink);padding:16px;margin:16px 0;border-radius:4px}
.meta{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700}
.stem{margin:8px 0 12px}
label{display:block;border:1px solid var(--line);padding:8px 10px;margin:6px 0;border-radius:4px;cursor:pointer}
label.right{background:var(--okbg);border-color:var(--ok)}label.wrong{background:var(--badbg);border-color:var(--bad)}
button.check{background:var(--ink);color:var(--cream);border:0;padding:8px 14px;font-weight:700;border-radius:4px;cursor:pointer}
.exp{display:none;margin-top:12px;border-top:2px solid var(--ok);padding-top:8px;font-size:15px}.exp.show{display:block}
.exp ul{padding-left:18px}.verdict{font-weight:800}
</style></head><body>
<header><h1>CCAR-F Practice Quiz</h1>
<select id="dom" aria-label="Filter by domain"><option value="">All domains</option>__DOMOPTS__</select>
<button id="reset">Reset</button><span class="score" id="score">0 / 0</span></header>
<main id="list"></main>
<script>
const QS = __DATA__;
const list = document.getElementById('list'), scoreEl = document.getElementById('score');
let done = {};
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML}
function render(){
  const dom = document.getElementById('dom').value;
  list.innerHTML = '';
  QS.filter(q => !dom || q.domain === dom).forEach(q => {
    const multi = q.answer.length > 1, type = multi ? 'checkbox' : 'radio';
    const el = document.createElement('section'); el.className = 'q';
    el.innerHTML = `<div class="meta">Q${q.id} · ${q.domain} · ${esc(q.scenario)}${multi ? ' · choose ' + q.answer.length : ''}</div>
      <div class="stem">${esc(q.stem)}</div>
      ${Object.entries(q.options).map(([k,v]) => `<label data-k="${k}"><input type="${type}" name="q${q.id}" value="${k}"> <b>${k}.</b> ${esc(v)}</label>`).join('')}
      <button class="check">Check</button>
      <div class="exp"><p class="verdict"></p><p><b>Why ${q.answer.join(', ')}:</b> ${esc(q.why)}</p>
      <ul>${Object.entries(q.wrong).map(([k,v]) => `<li><b>${k}:</b> ${esc(v)}</li>`).join('')}</ul>
      <p><i>Task statement ${esc(q.objective)}</i></p></div>`;
    el.querySelector('.check').onclick = () => {
      const picked = [...el.querySelectorAll('input:checked')].map(i => i.value).sort();
      if (!picked.length) return;
      const ok = picked.join() === [...q.answer].sort().join();
      el.querySelectorAll('label').forEach(l => {
        const k = l.dataset.k;
        l.classList.toggle('right', q.answer.includes(k));
        l.classList.toggle('wrong', picked.includes(k) && !q.answer.includes(k));
      });
      const v = el.querySelector('.verdict'); v.textContent = ok ? 'Correct' : 'Not quite'; v.style.color = ok ? 'var(--ok)' : 'var(--bad)';
      el.querySelector('.exp').classList.add('show');
      done[q.id] = ok; tally();
    };
    list.appendChild(el);
  });
}
function tally(){const v=Object.values(done);scoreEl.textContent=v.filter(Boolean).length+' / '+v.length}
document.getElementById('dom').onchange = render;
document.getElementById('reset').onclick = () => { done = {}; tally(); render(); };
render();
</script></body></html>
"""


def build_quiz(qs):
    opts = "".join(f'<option value="{d}">{d} · {html.escape(n)}</option>' for d, (n, _, _) in DOMAINS.items())
    data = json.dumps(qs).replace("</", "<\\/")
    (ROOT / "questions" / "quiz.html").write_text(QUIZ.replace("__DOMOPTS__", opts).replace("__DATA__", data))


def build_anki():
    rows = list(csv.DictReader((ROOT / "anki" / "flashcards.csv").open()))
    assert len(rows) == 60, f"expected 60 flashcards, got {len(rows)}"
    assert all(r["domain"] in DOMAINS for r in rows), "flashcard domain must be D1..D5"
    model = genanki.Model(
        1607392321,
        "CCAR-F Flashcard",
        fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Domain"}],
        templates=[{
            "name": "Card",
            "qfmt": '<div class="dom">{{Domain}}</div><div class="front">{{Front}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="back">{{Back}}</div>',
        }],
        css=".card{font-family:Inter,-apple-system,sans-serif;font-size:19px;text-align:left;color:#1a1a1a;background:#f5f0e6;padding:12px}"
            ".nightMode.card{color:#f5f0e6;background:#1c1c1c}"
            ".dom{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#b85c1f;font-weight:700;margin-bottom:8px}"
            ".front{font-weight:700}.back{line-height:1.45}",
    )
    deck = genanki.Deck(2059400112, "Claude Certified Architect – Foundations (CCAR-F)")
    for i, r in enumerate(rows, 1):
        name = DOMAINS[r["domain"]][0]
        deck.add_note(genanki.Note(
            model=model,
            fields=[html.escape(r["front"]), html.escape(r["back"]).replace("\n", "<br>"), f"{r['domain']} · {html.escape(name)}"],
            tags=[f"CCAR-F::{r['domain']}"] + r["tags"].split(),
            guid=genanki.guid_for("ccar-f", i),
        ))
    genanki.Package(deck).write_to_file(ROOT / "anki" / "ccar-f-flashcards.apkg")


# ---------- study guide: markdown -> HTML ----------

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def md(text, src_dir="."):
    """Render markdown and fix it up for the study-guide page at the repo root."""
    h = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    h = h.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")

    def link(m):
        url = m.group(1)
        if url.startswith(("http://", "https://")):
            return f'href="{url}" target="_blank" rel="noopener"'
        if url.startswith(("#", "mailto:")):
            return m.group(0)
        # repo-relative links: resolve against the source file's folder
        return f'href="{(Path(src_dir) / url).as_posix().replace("lessons/../", "").replace("exercises/../", "")}"'

    return re.sub(r'href="([^"]*)"', link, h)


def inline(text):
    return re.sub(r"^<p>(.*)</p>$", r"\1", md(text).strip(), flags=re.S)


def split_on(text, marker):
    """Split markdown on a heading marker ('## ' or '### '), skipping fenced code. Returns (preamble, [(title, body)])."""
    pre, parts, cur, fence = [], [], None, False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith(marker):
            cur = [line[len(marker):].strip(), []]
            parts.append(cur)
        elif cur is None:
            pre.append(line)
        else:
            cur[1].append(line)
    return "\n".join(pre), [(t, "\n".join(b)) for t, b in parts]


def folds(body, src_dir, prefix):
    intro, subs = split_on(body, "### ")
    out = md(intro, src_dir) if intro.strip() else ""
    if not subs:
        return out
    out += '\n<div class="folds">'
    for title, text in subs:
        lines = text.strip().splitlines()
        sub = ""
        if lines and re.fullmatch(r"\*[^*].*\*", lines[0].strip()):
            sub = f'<span class="fs">{inline(lines[0].strip()[1:-1])}</span>'
            lines = lines[1:]
        out += (f'\n<details class="fold" id="{prefix}-{slug(title)}"><summary><span class="ft">{inline(title)}</span>{sub}</summary>'
                f'<div class="fb">{md(chr(10).join(lines), src_dir)}</div></details>')
    return out + "\n</div>"


def title_and_rest(path):
    text = path.read_text()
    first, _, rest = text.partition("\n")
    assert first.startswith("# "), f"{path} must start with '# Title'"
    return first[2:].strip(), rest


def page_section(path, prefix):
    """Overview / Strategy tab: # -> h2, ## -> h3, ### -> folds."""
    title, rest = title_and_rest(path)
    pre, secs = split_on(rest, "## ")
    out = f"<h2>{inline(title)}</h2>\n" + md(pre, "lessons").replace("<p>", '<p class="prose">')
    for t, body in secs:
        out += f'\n<h3 id="{prefix}-{slug(t)}">{inline(t)}</h3>\n' + folds(body, "lessons", f"{prefix}-{slug(t)}")
    return out


def domain_article(path, did):
    title, rest = title_and_rest(path)
    name = title.split("·", 1)[-1].strip()
    pre, secs = split_on(rest, "## ")
    paras = [p for p in pre.strip().split("\n\n") if p.strip()]
    meta = inline(paras.pop(0)) if paras and paras[0].startswith("**") else ""
    out = (f'<article class="domain stack" id="{did.lower()}">\n'
           f'  <header class="dhead"><span class="dnum">{did}</span><div><h2>{html.escape(name)}</h2><p class="fs">{meta}</p></div></header>\n')
    out += md("\n\n".join(paras), "lessons").replace("<p>", '<p class="prose">')
    for t, body in secs:
        block = folds(body, "lessons", f"{did.lower()}-{slug(t)}")
        if t.lower().startswith("task statements"):
            block = block.replace("<ol>", '<ol class="objlist">', 1)
        out += f"\n<h3>{inline(t)}</h3>\n{block}"
    return out + "\n</article>"


def exercise_fold(path):
    title, rest = title_and_rest(path)
    num = path.name[:2]
    pre, secs = split_on(rest, "## ")
    paras = [p for p in pre.strip().split("\n\n") if p.strip()]
    meta = inline(paras.pop(0)) if paras and paras[0].startswith("**") else ""
    body = md("\n\n".join(paras), "exercises")
    for t, text in secs:
        inner = re.sub(r"^### ", "##### ", text, flags=re.M)  # ### inside an exercise -> small heading
        rendered = f"<h4>{inline(t)}</h4>\n" + md(inner, "exercises")
        if t.lower().startswith(("reference answer", "answer")):
            rendered = f'<details class="reveal"><summary>Show {inline(t).lower()}</summary>{rendered}</details>'
        body += "\n" + rendered
    return (f'<details class="fold" id="ex-{num}"><summary><span class="ft">{inline(title)}</span>'
            f'<span class="fs">{meta} · <a href="exercises/{path.name}">{path.name}</a></span></summary><div class="fb">{body}</div></details>'), title, meta


def build_study_guide(qs):
    lessons = sorted((ROOT / "lessons").glob("[0-9][0-9]-*.md"))
    by_num = {p.name[:2]: p for p in lessons}
    domains = "\n".join(domain_article(by_num[f"0{i}"], d) for i, d in enumerate(DOMAINS, 1))
    ex = [exercise_fold(p) for p in sorted((ROOT / "exercises").glob("[0-9][0-9]-*.md"))]
    table = ('<div class="table-scroll"><table><thead><tr><th>Exercise</th><th>Details</th></tr></thead><tbody>'
             + "".join(f'<tr><td><a href="#ex-{f.split(chr(34))[3][3:]}">{t}</a></td><td>{m}</td></tr>' for f, t, m in ex)
             + "</tbody></table></div>")
    exercises = table + '\n<div class="folds">\n' + "\n".join(f for f, _, _ in ex) + "\n</div>"
    domains_js = json.dumps([{"id": d.lower(), "label": d, "w": w, "name": n} for d, (n, w, _) in DOMAINS.items()])
    page = (ROOT / "templates" / "study-guide.html").read_text()
    for key, val in {
        "__OVERVIEW__": page_section(by_num["00"], "ov"),
        "__DOMAINS__": domains,
        "__EXERCISES__": exercises,
        "__STRATEGY__": page_section(by_num["06"], "plan"),
        "__DOMAINS_JS__": domains_js,
        "__QDATA__": json.dumps(qs).replace("</", "<\\/"),
    }.items():
        assert key in page, key
        page = page.replace(key, val)
    (ROOT / "study-guide.html").write_text(page)


if __name__ == "__main__":
    qs = json.loads((ROOT / "questions" / "questions.json").read_text())
    check(qs)
    build_markdown(qs)
    build_quiz(qs)
    build_anki()
    build_study_guide(qs)
    print("built: questions/practice-questions.md, questions/quiz.html, anki/ccar-f-flashcards.apkg, study-guide.html")
