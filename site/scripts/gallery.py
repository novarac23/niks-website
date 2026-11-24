"""Shared markup for Dotted Line's original screenshot gallery."""

from html import escape


def dotted_screenshots():
    screenshots = (
        ("progress", "Time in dots", "Dotted Line’s progress screen showing the year, month, week, and day as rows of dots."),
        ("countdown", "Countdowns", "Dotted Line counting down 47 days to a trip to Lisbon."),
        ("intention", "Daily intentions", "Dotted Line’s daily intention screen with the words ‘Be brave.’"),
        ("widgets", "Home Screen widgets", "Dotted Line’s Home Screen widgets showing time progress, age, a countdown to Lisbon, and a daily intention."),
    )
    figures = ''.join(f'<figure><img src="../../assets/dotted/{name}.png" width="1206" height="2622" alt="{escape(alt, quote=True)}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure>' for name, caption, alt in screenshots)
    return f'<div class="screenshot-gallery" role="region" aria-label="Dotted Line screenshots, scroll horizontally for more" tabindex="0">{figures}</div>'
