# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Gognilr/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Gognilr/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up Monday 23 November 2026 in a
single image: COP31 collapsing in Antalya without a climate deal, the
Democrats clinching a 258-seat House majority, suspected Ukrainian sea
drones hitting a Russian warship in Libya, the deadly candy factory fire
in Indonesia, and strikes across Yemen — plus the day's other briefs.
The masthead names the day, and every story is drawn from events that
happened, or were first reported, on 23 November 2026.

![The World Today — Monday 23 November 2026](entry.png)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22+) validates `entry.png` — PNG/JPEG magic bytes, at most
1 MiB, at most 1024×1024 — then copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `./out`). The page itself is
composed at build time by `compose.py` (Pillow): masthead, generated hero
photograph of the COP31 plenary hall, headline, five tagged stories
and a briefs footer.

## The day's stories

- **COP31 collapses with no deal.** After nearly 48 hours of overtime in
  Antalya, the talks end without an overarching agreement; the EU and
  Pacific island states reject a draft that drops any mention of fossil
  fuels.
- **Democrats clinch a 258-seat House majority.** The largest since 1992,
  reached after Chuck Hubbard beats Virginia Foxx in a North Carolina
  recount; Hakeem Jeffries is set to become Speaker.
- **Sea drones hit Russian warship in Libya.** A suspected Ukrainian drone
  strike on the corvette Merkury at Benghazi naval base; the ship capsizes
  and 10 people are injured. Neither Kyiv nor Moscow confirms responsibility.
- **24 body bags pulled from candy factory fire.** A fire at a candy factory
  in Cikande, Banten, Indonesia, leaves about 30 people unaccounted for.
- **Strikes and Houthi drone attack kill 5, injure 18 in Yemen.**
  Saudi-led coalition airstrikes and a Houthi drone attack strike across
  the country.
- **Also today:** Delta delays 1,000+ flights at Atlanta after a systems
  fault; South Korea's education minister quits over the college-exam
  cheating row; Russian strikes kill 6 near Kyiv; drones hit a UN building
  in Khartoum; North Korea's Kim says his country seeks security, not
  supremacy; Paolo Bulgari dies at 89.

Sources: Xinhua, AP, Reuters, SCMP, The Japan Times, Manila Times,
The Economic Times, Gulf News (23 November 2026 editions).

Deliberately left out: the Houthi strikes on Riyadh, the Sparta II fire
and the Nigeria boat capsize — all 22 November stories, covered in the
previous day's entry.

## Licence

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=c5nt5ce8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
