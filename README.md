# The World on Monday — 23 November 2026 in one image

![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/marwankickup/news-image-20261123-entry/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/marwankickup/news-image-20261123-entry/reward.svg)

Entry for the make.fun bounty [news-image-20261123](https://make.fun/bounty/news-image-20261123).

`entry.png` is a newspaper-style front page that sums up the world news of
**Monday 23 November 2026**: a masthead, the date in a banner, and six story
panels, each with a pictogram drawn in code, a headline and one factual line.
`main.ts` (Node, standard library only) copies `entry.png` to
`/output/entry.png`. The poster itself is drawn programmatically by
`draw_image.py` (Python + Pillow), which is kept here as the record of how
the image was made; the grader only runs `main.ts`.

## The six stories

1. **Huang is Nvidia CEO again** — Nvidia said on Monday it is reinstating
   Jensen Huang as CEO, effective immediately, 11 days after he resigned
   (12 Nov) over revelations of extramarital affairs including one with an
   alleged Chinese spy; the board is satisfied he poses no national-security
   risk, and Trump personally intervened. Shares rose about 33%.
   Sources: Reuters, "Nvidia reinstates Jensen Huang as CEO"
   (reuters.com, 23 Nov 2026).
2. **Iran vows to defy US blockade** — Iran's foreign ministry said it
   will use all available means to counter the US naval blockade; Iran's
   army said it shot down a US drone over the Persian Gulf, and explosions
   were reported in the Strait of Hormuz. Trump warned strikes could
   resume after the New Year if no deal is reached.
   Sources: OneTurn early edition, 23 Nov 2026; Just Security Early
   Edition, 23 Nov 2026.
3. **$1.62bn package for Nepal** — In New Delhi on Monday, Indian PM
   Narendra Modi announced with Nepali PM Balendra Shah a 240bn NPR
   ($1.62bn) development package for Nepal's rebuild after the 26 August
   glacier-collapse flood (~1,500 dead, ~5,200 missing; ~$4.7bn losses):
   $377m in grants plus a $1.24bn credit line for energy projects.
   Sources: AP, 23 Nov 2026; Reuters, 23 Nov 2026.
4. **EU proposes 22nd Russia package** — The European Commission on
   Monday proposed its 22nd package of sanctions against Russia, targeting
   financial institutions and crypto platforms: a transaction ban extended
   to some 60 Russian banks (all removed from SWIFT), energy services
   including electricity, 70+ more shadow-fleet ships, a visa ban for
   Russian ex-combatants, and a ban on Russian teams and athletes
   competing under the Russian flag in the EU.
   Sources: Reuters, "EU Commission proposes 22nd sanctions package on
   Russia" (23 Nov 2026); European Commission statement by President von
   der Leyen (23 Nov 2026).
5. **Armenia drops Karabakh claim** — Armenia published a draft proposal
   of a new constitution on Monday that rewrites the preamble and removes
   the reference to the 1990 Declaration of Independence calling for the
   reunification of Armenia and Nagorno-Karabakh — a central sticking point
   for Azerbaijan before a formal peace agreement. Baku welcomed the step.
   Sources: Reuters, "Armenia proposes new constitution in step towards
   peace with Azerbaijan" (Tbilisi, 23 Nov 2026); AP, 23 Nov 2026.
6. **Hasina to be jailed if she returns** — Bangladesh's State Minister
   for Foreign Affairs told Reuters on Monday that Bangladesh will arrest
   and jail former prime minister Sheikh Hasina if she returns to the
   country.
   Sources: Reuters via Just Security Early Edition, 23 Nov 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png, byte-identical to entry.png
```

## Regenerate the poster

```sh
python3 draw_image.py   # needs Pillow and the Liberation fonts
```
