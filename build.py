#!/usr/bin/env python3
"""Builds the landing page for Livia McGraw's teammate project.

Run: python3 build.py
Copy and facts live in this file. Every page is first person as Livia ("I");
her name appears only where she introduces herself. No external links:
research is cited in plain text.
"""
import json
import re

SITE_NAME = "The Teammate Effect"   # working name, Livia has not chosen one yet
AUTHOR = "Livia McGraw"
SITE = "https://odyssey-jotun.github.io/teammate-effect/"
TODAY = "2026-10-24"
HANDOUT = "downloads/teammate-handout.pdf"
CTA = "Download the Teammate Handout"

SOURCES = [
    "Benson, A. J., &amp; Bruner, M. W. (2018). How teammate behaviors relate to athlete affect, cognition, and behaviors: A daily diary approach within youth sport. <em>Psychology of Sport and Exercise, 34</em>, 119&ndash;127.",
    "Edmondson, A. (1999). Psychological safety and learning behavior in work teams. <em>Administrative Science Quarterly, 44</em>(2), 350&ndash;383.",
    "Fransen, K., Boen, F., Vansteenkiste, M., Mertens, N., &amp; Vande Broek, G. (2018). The power of competence support: The impact of coaches and athlete leaders on intrinsic motivation and performance. <em>Scandinavian Journal of Medicine &amp; Science in Sports, 28</em>(2), 725&ndash;745.",
    "Fransen, K., Steffens, N. K., Haslam, S. A., Vanbeselaere, N., Vande Broek, G., &amp; Boen, F. (2016). We will be champions: Leaders&rsquo; confidence in &lsquo;us&rsquo; inspires team members&rsquo; team confidence and performance. <em>Scandinavian Journal of Medicine &amp; Science in Sports, 26</em>(12), 1455&ndash;1469.",
    "Fransen, K., Vanbeselaere, N., De Cuyper, B., Vande Broek, G., &amp; Boen, F. (2014). The myth of the team captain as principal leader: Extending the athlete leadership classification within sport teams. <em>Journal of Sports Sciences, 32</em>(14), 1389&ndash;1397.",
    "Fransen, K., Vanbeselaere, N., De Cuyper, B., Vande Broek, G., &amp; Boen, F. (2015). Perceived sources of team confidence in soccer and basketball. <em>Medicine &amp; Science in Sports &amp; Exercise, 47</em>(7), 1470&ndash;1484.",
    "Furley, P., Moll, T., &amp; Memmert, D. (2015). &ldquo;Put your hands up in the air&rdquo;? The interpersonal effects of pride and shame expressions on opponents and teammates. <em>Frontiers in Psychology, 6</em>, Article 1361.",
]


def svg(body, sw="2.6"):
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


ICON_DOUBT = svg('<path d="M6 40h36"/><path d="M8 12l10 8 8-4 14 16"/><path d="M40 24v8h-8"/>')
ICON_HEAD = svg('<circle cx="24" cy="24" r="17"/><path d="M17 33c2-2.5 4.5-3.5 7-3.5s5 1 7 3.5"/><path d="M17 19l4 2M31 19l-4 2"/>')
ICON_ROSTER = svg('<circle cx="24" cy="15" r="5"/><circle cx="11" cy="20" r="4"/><circle cx="37" cy="20" r="4"/><path d="M15 38c0-6 4-10 9-10s9 4 9 10"/><path d="M4 36c0-4 3-7 7-7M44 36c0-4-3-7-7-7"/>')
ICON_VOICE = svg('<path d="M8 20v8h7l11 8V12l-11 8z"/><path d="M32 18c2 2 3 4 3 6s-1 4-3 6M37 13c4 3 6 7 6 11s-2 8-6 11"/>')
ICON_STAR = svg('<path d="M24 6l5.5 11.5 12.5 1.5-9.2 8.6 2.4 12.4L24 34l-11.2 6 2.4-12.4L6 19l12.5-1.5z"/>')
ICON_BODY = svg('<circle cx="24" cy="9" r="4.5"/><path d="M24 14v14M24 28l-7 13M24 28l7 13M13 20l11-3 11 3"/>')
ICON_HEART = svg('<path d="M24 40S7 30 7 18c0-5 4-9 9-9 3.5 0 6.4 2 8 5 1.6-3 4.5-5 8-5 5 0 9 4 9 9 0 12-17 22-17 22z"/>')
ICON_FLAG = svg('<path d="M12 42V7"/><path d="M12 8h22l-5 7 5 7H12"/>')
ICON_SHIELD = svg('<path d="M24 6l15 6v10c0 10-6.5 17-15 20-8.5-3-15-10-15-20V12z"/><path d="M17 24l5 5 9-10"/>')
CHECK = svg('<path d="M10 25l9 9 19-20"/>', sw="3.4")
CROSS = svg('<path d="M14 14l20 20M34 14L14 34"/>', sw="3.4")
MARK = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#1F3354"/>'
        '<circle cx="16" cy="16" r="9.5" fill="none" stroke="#C99A52" stroke-width="2"/>'
        '<path d="M6.5 16h19M16 6.5v19" stroke="#C99A52" stroke-width="1.6"/></svg>')
FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="9" fill="#1F3354"/>'
           '<circle cx="16" cy="16" r="9.5" fill="none" stroke="#C99A52" stroke-width="2"/>'
           '<path d="M6.5 16h19M16 6.5v19" stroke="#C99A52" stroke-width="1.6"/></svg>\n')

PROBLEMS = [
    (ICON_DOUBT, "23 sec", "Doubt spreads through a team",
     "In an experiment with 144 young soccer players, teams whose leader sounded confident finished a passing drill almost 23 seconds faster. Teams whose leader voiced doubt barely improved.",
     "faster with a confident teammate leading"),
    (ICON_HEAD, "72", "Players stop believing in themselves",
     "Players and coaches ranked 72 things that raise or lower a team's confidence. Among the worst were negative talk, slumped body language and anger at a teammate's mistake.",
     "sources of team confidence, ranked by players and coaches"),
    (ICON_ROSTER, "44%", "No player should have to wait for the captain to lead",
     "When researchers asked 4,451 players and coaches who led their teams, 44% said the captain was not the top leader in any of four leadership roles. Leaders came from all over the roster.",
     "said the captain was not the top leader in any role"),
]

HABITS = [
    (ICON_VOICE, "Believe in your team out loud",
     "Teams with a confident teammate leader finished a passing drill almost 23 seconds faster."),
    (ICON_STAR, "Tell teammates what they do well",
     "Players whose teammate cheered on their skills cut 13 seconds off a drill. Players without that teammate improved by 1."),
    (ICON_BODY, "Watch what your body says",
     "Players felt less sure about their own penalty kick after watching a teammate hang their head."),
    (ICON_HEART, "Pass kindness on",
     "Hockey players ages 11 to 17 were kinder to teammates on days their teammates were kind to them."),
    (ICON_FLAG, "Lead from wherever you are",
     "Leaders came from all over the roster. You don't need to be the captain or the best scorer."),
    (ICON_SHIELD, "Make it safe to make mistakes",
     "Teams that felt safe admitting mistakes and asking questions learned more, and the teams that learned more did better."),
]

STEPS = [
    ("Pick one habit", "Read the six habits in the free handout and choose the one your team needs first."),
    ("Fill out a goal card", "Write down one thing you'll do at practice this week, and keep the card in your bag."),
    ("Watch your team believe", "Enjoy playing on a team that trusts each other and plays better because of it."),
]


def css():
    t = open("styles.css").read()
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"\s*([{};:,>])\s*", r"\1", t).replace(";}", "}").strip()


def btn(cls="btn"):
    return f'<a href="{HANDOUT}" class="{cls}" download>{CTA}</a>'


def page():
    title = f"How to Be a Good Teammate: Six Habits From the Research | {SITE_NAME}"
    desc = ("My free handout of six teammate habits from peer-reviewed research, made for young athletes: "
            "what scientists found and what each habit looks like at practice, in a game and at school.")
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": SITE_NAME, "inLanguage": "en-US"},
        {"@type": "Person", "@id": SITE + "#livia", "name": AUTHOR},
        {"@type": "WebPage", "@id": SITE + "#page", "url": SITE, "name": title, "description": desc,
         "isPartOf": {"@id": SITE + "#site"}, "author": {"@id": SITE + "#livia"}, "datePublished": TODAY},
        {"@type": "CreativeWork", "name": "How One Teammate Changes a Team", "author": {"@id": SITE + "#livia"},
         "url": SITE + HANDOUT, "encodingFormat": "application/pdf", "isAccessibleForFree": True},
    ]}, separators=(",", ":"))
    problems = "\n".join(f"""      <div class="card">
        <div class="icon">{i}</div>
        <p class="num">{n}</p>
        <h3>{h}</h3>
        <p>{p}</p>
        <p class="of">{o}</p>
      </div>""" for i, n, h, p, o in PROBLEMS)
    habits = "\n".join(f"""      <div class="card">
        <div class="icon">{i}</div>
        <h3>{h}</h3>
        <p>{p}</p>
      </div>""" for i, h, p in HABITS)
    steps = "\n".join(f"""      <li>
        <h3>{h}</h3>
        <p>{p}</p>
      </li>""" for h, p in STEPS)
    refs = "\n".join(f"      <li>{s}</li>" for s in SOURCES)
    hero_set = "images/hero-team-480.webp 480w, images/hero-team-680.webp 680w, images/hero-team-800.webp 800w"
    hero_sizes = "(max-width: 860px) min(calc(100vw - 40px), 420px), 440px"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="{SITE}">
<meta name="author" content="{AUTHOR}">
<meta name="theme-color" content="#14223B">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The cover of Livia McGraw's handout, How One Teammate Changes a Team">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" as="image" type="image/webp" href="images/hero-team-800.webp" imagesrcset="{hero_set}" imagesizes="{hero_sizes}" fetchpriority="high">
<link rel="preload" href="fonts/barlow-condensed.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/source-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{css()}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>

<a class="skip" href="#main">Skip to content</a>

<nav class="site" aria-label="Primary">
  <div class="wrap">
    <a class="wordmark" href="#main">{MARK}<span>{SITE_NAME}</span></a>
    <ul>
      <li><a href="#habits">The habits</a></li>
      <li><a href="#sources">Research</a></li>
      <li><a href="{HANDOUT}" download>Handout</a></li>
    </ul>
  </div>
</nav>

<main id="main">

<header class="hero">
  <div class="wrap hero-grid">
    <div class="hero-text">
      <h1>Every player can lead</h1>
      <p class="lede">A free handout of six teammate habits from real research, made for young athletes.</p>
      <div class="btn-row">{btn("btn light")}</div>
    </div>
    <figure class="hero-photo"><img src="images/hero-team-800.webp" srcset="{hero_set}" sizes="{hero_sizes}" width="800" height="1000" alt="Young girls in navy team jerseys sitting together on a bench, seen from behind" fetchpriority="high" decoding="async"></figure>
  </div>
</header>

<section id="problem" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>Being a good teammate is harder than it looks</h2>
      <p>Young players hear &ldquo;be a good teammate&rdquo; all the time, and few are ever shown what it takes.</p>
    </div>
    <div class="cards">
{problems}
    </div>
  </div>
</section>

<section id="about">
  <div class="wrap split">
    <div class="about-text">
      <h2>What 14 studies taught me about teammates</h2>
      <p>I'm {AUTHOR}, and I play tennis. I've had bad teammates, and I know how much one person's attitude can change the way a whole team plays.</p>
      <p>So I went looking for what the research says. I read 14 peer-reviewed studies on how teammates affect each other's confidence and performance. My favorite followed high school teams, because I could relate to it. The biggest thing I took away is that a teammate's encouragement can matter as much as the coach's, because players listen to people who are more like them.</p>
      <p>I turned what I learned into six habits a third grader can use, and Coach Young invited me to share them with his teams at the basketball academy. Before this, I coached Pee Wee basketball for two years.</p>
    </div>
    <figure class="handout"><img src="images/handout-cover-760.webp" srcset="images/handout-cover-480.webp 480w, images/handout-cover-760.webp 760w" sizes="(max-width: 860px) min(calc(100vw - 40px), 380px), 380px" width="760" height="984" alt="The cover of my handout, How One Teammate Changes a Team, with a youth team cheering above the title" loading="lazy" decoding="async"></figure>
  </div>
</section>

<section id="plan" class="band">
  <div class="wrap">
    <div class="section-head center">
      <h2>Three steps to becoming the teammate everyone wants</h2>
      <p>It starts at your next practice.</p>
    </div>
    <ol class="steps">
{steps}
    </ol>
    <div class="btn-row">{btn()}</div>
  </div>
</section>

<section id="habits">
  <div class="wrap">
    <div class="section-head center">
      <h2>Six habits from the research</h2>
      <p>Each one in the handout shows what scientists found and what it looks like at practice, in a game and at school.</p>
    </div>
    <div class="cards">
{habits}
    </div>
  </div>
</section>

<section id="stakes" class="dark">
  <div class="wrap">
    <div class="section-head center">
      <h2>What one teammate can change</h2>
    </div>
    <div class="stakes">
      <div class="stake">
        <h3>When nobody steps up</h3>
        <ul class="outcomes">
          <li>{CROSS}<span>One player's frustration spreads, and the whole team starts doubting itself.</span></li>
          <li>{CROSS}<span>Everyone waits for the captain or the coach to fix things.</span></li>
          <li>{CROSS}<span>Close games and losing streaks fall apart under pressure.</span></li>
        </ul>
      </div>
      <div class="stake good">
        <h3>When every player leads</h3>
        <ul class="outcomes">
          <li>{CHECK}<span>Your team believes it can win, and plays like it.</span></li>
          <li>{CHECK}<span>You know your own actions help decide how your team plays.</span></li>
          <li>{CHECK}<span>Practice is more fun, because sports are more fun when you like your teammates.</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="closing">
  <div class="wrap">
    <h2>Start with one habit at your next practice</h2>
    <p>The handout is free, with goal cards on the last page.</p>
    <div class="btn-row">{btn()}</div>
  </div>
</section>

<section class="refs" id="sources">
  <div class="wrap">
    <h2>Research behind the handout</h2>
    <ol>
{refs}
    </ol>
    <p class="cite-line">Photos: Unsplash.</p>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <p>I'm {AUTHOR}, and {SITE_NAME} is my project on being a good teammate. Every figure on this page comes from the peer-reviewed research listed above.</p>
  </div>
</footer>

</body>
</html>
"""


if __name__ == "__main__":
    open("index.html", "w").write(page())
    open("robots.txt", "w").write("User-agent: *\nDisallow: /\n")
    open("favicon.svg", "w").write(FAVICON)
    open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{SITE}</loc><lastmod>{TODAY}</lastmod></url>\n</urlset>\n')
    print("wrote index.html, robots.txt, favicon.svg, sitemap.xml")
