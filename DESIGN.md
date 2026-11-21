---
name: Nik’s Website
description: A restrained personal website for apps and writing.
colors:
  paper: "#fcfcfe"
  ink: "#1b2238"
  muted: "#586176"
  blue: "#2459d3"
  line: "#dfe3eb"
  prose: "#424c61"
  code-bg: "#172033"
  code-header: "#202b42"
  code-text: "#e6edf7"
typography:
  body:
    fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "17px"
    lineHeight: 1.7
  display:
    fontFamily: "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(2rem, 5.4vw, 3.5rem)"
    lineHeight: 1.2
    letterSpacing: "-.025em"
  section:
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-.02em"
rounded:
  button: "6px"
  portrait: "12px"
  app-icon: "14px"
  screenshot: "16px"
spacing:
  small: "12px"
  medium: "24px"
  large: "40px"
  section: "48px"
  page: "56px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "white"
    rounded: "{rounded.button}"
    padding: "10px 18px"
  button-primary-hover:
    backgroundColor: "{colors.blue}"
---

# Design System: Nik’s Website

## Overview

A personal maker website with a near-white surface, navy text, blue links, and generous whitespace. Its character comes from readable content, personal copy, and real assets. Preserve the current system when making scoped refinements. Impeccable informed the cleanup; this document records the approved result rather than a new redesign proposal.

The reference was the directness of Sindre Sorhus's personal app site, expanded with a fuller introduction and writing. It is not a copy of that site or of the old Jekyll theme. No decorative astronomical identity remains.

## Colors

Use the frontmatter colors and corresponding custom properties in `site/src/styles.css`. Blue is for links, active navigation, and focus. Ink supports headings and primary actions; muted text supports dates and descriptions. Dark code panels provide a distinct reading surface for examples. Do not introduce extra accent colors or change the approved palette as a side effect of another task.

## Typography

The approved system uses the platform sans stack with no external fonts. Body text is 17px/1.7, changing to 16px on phones; article prose uses 1.85 line height and a maximum measure of 70ch. Monospace is reserved for code. Normal h1 sizing is `clamp(2rem, 5vw, 3rem)`; the homepage uses the display token above. Titles are balanced and tightly tracked without exaggerated scale.

Keep headings plain: Apps, Recent posts, Blog, About me, Screenshots. No eyebrow labels, invented slogans, or numbered sections. Preserve ordinary sentence case and first-person copy. “Hi, I’m Nikola.” is one continuous heading with no forced line break.

## Layout

The shared shell is at most 1000px wide with 40px side margins; at 700px and below, side margins become 20px. The header is a wordmark plus navigation. Its phone layout uses a native hamburger disclosure. There is no fixed overlay or JavaScript menu dependency.

Section spacing is generally 40–64px, with smaller gaps inside related content. About uses explicit `photo copy` grid areas: the original portrait, up to 340px, sits on the left and the complete biography/contact article on the right, with a 48px gap. At 700px and below, it stacks photo above copy. Avoid stretching, cropping, or upscaling the original portrait beyond its useful resolution.

Dotted screenshots form four columns on wide screens. At 1000px and below, the gallery scrolls horizontally with columns `min(78vw, 300px)`. Maintain natural image aspect ratios, intrinsic dimensions, alt text, keyboard focus, and native scrolling.
Blog posts can embed this same gallery within the article’s reading width, preserving its captions and responsive behavior.

Divider ownership is deliberate: header bottom and footer top; app/post lists own a top rule and separators between rows. Use `--divider: 1px solid var(--line)`. No extra rule beneath the introduction, around article headings/navigation, or around screenshot content. Author-written article rules and code borders serve their own purpose.

## Elevation & Depth

The system is flat. Use whitespace, typography, and the limited divider pattern for grouping. There are no decorative shadows, glass panels, gradient surfaces, or nested marketing cards.

## Shapes

Buttons use 6px corners; portrait and code blocks use 12px; app icons use 14px in lists and 16px in the product title; screenshots use 16px. Preserve actual raster imagery. SVG is appropriate for consistent functional hamburger/close and external-link icons, not ornamental illustrations.

## Components

- **Navigation:** Home, Apps, Blog, About, Contact Me. Default links are muted; hover becomes ink; current desktop route gets a blue underline. The phone disclosure has a 44px hit target, visible focus, and hamburger/close states. Contact Me is a mail link after About.
- **Homepage:** title, role, approved introduction, Apps, Recent posts. No hero actions or “how I work” section.
- **App row:** actual icon, title, factual description, platforms. The whole row links to the local detail page; no separate “View app” label.
- **Recent post row:** date left and title right, including on phones. The full Blog page keeps descriptions, dates, and reading times. Post categories are omitted throughout the site.
- **Dotted detail:** real icon, personal story, website and App Store links beside each other when space permits, four original screenshots with concise captions. No feature table.
- **Links and buttons:** underlines and visible keyboard focus; minimum 44px for navigation/action controls. Primary product action uses ink with white text; secondary action uses a restrained border. Actions wrap naturally.
- **Code:** labeled, selectable, horizontally scrollable blocks; Python highlighting at build time and `text` fences for output. Preserve keyboard access to scrolling.
- **Footer and browser icon:** site name left, literal `@` plus current year right. No email or company line. Keep the explicit empty icon declaration on canonical and redirect pages.

## Do's and Don'ts

- Do preserve the user's approved copy, portrait, app icon, screenshot sources, and original blog content.
- Do check desktop and phone behavior, contrast, long text, focus, image dimensions, and links when changing affected components.
- Do use Impeccable's relevant playbook and craft floor when available; follow this approved system rather than starting a new aesthetic workshop for a small change.
- Don't restore the star, nova artwork/caption, company branding, favicon, hero buttons, redundant app links, or removed sections.
- Don't add generic card grids, ornamental statistics, gradient text, external fonts, or animations to make the site seem more designed.
- Don't claim visual review when only source/build checks were possible. Browser preview was unavailable in the original workspace; the current environment should be assessed afresh.
