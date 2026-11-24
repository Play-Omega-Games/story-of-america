# Story of America

Reading plans for the 📜 Story of America Grok Bot template by Omega Games, part of the Omega Home Library (Story Shelf, ages 6 to 12). A family reads one piece of American history aloud at bedtime, word for word from This Country of Ours by H. E. Marshall (1917), with Fifty Famous Stories Retold by James Baldwin (1896) as a warm-up. Both are in the public domain in the United States.

## Quick start

```
curl -sO https://raw.githubusercontent.com/Play-Omega-Games/story-of-america/main/plans/story-of-america.json
python3 scripts/build.py --fetch
python3 tests/test_plan.py
python3 scripts/check_links.py
python3 scripts/check_standards.py
```

A bot loads `plans/story-of-america.json` (about 10 minutes a reading), `plans/story-of-america-5min.json` (about 5 minutes) and `plans/standards.json` from `https://raw.githubusercontent.com/Play-Omega-Games/story-of-america/main/plans/`. If that fails, it downloads `scripts/build.py`, `scripts/curation.py` and `scripts/scan.py` and rebuilds all three files from the public sources.

## Plan format

Each plan has `meta`, `chapters`, `readings`, `famous_stories` and `famous_nights`.

- `readings` (This Country of Ours, 99 chapters in 7 parts): `id`, `chapter`, `title`, `part_of_book`, `reading` and `of` (part of the chapter), `words`, `minutes` (at 150 words a minute), `word_offset` (within the chapter), `starts_with`, `ends_with`, `timeline` (`when`, `event`), `content`, `standards`, `text`. In the 5-minute plan, `parent` names the 10-minute reading each part comes from.
- `famous_stories`: the same fields without chapter and timeline; `famous_nights` groups them into nights in book order.
- `content`: `severity` (none, low, medium, high), `topics`, `note` (a short note for grown-ups, shown before medium and high readings) and, for high readings, `skip_summary` (one line in our own words for families who skip it).
- `standards`: the activity in the bot that supports practice toward each code (`framework`, `code`, `band`, `activity`, `wording`, `source`, `verified`). Code text is in `plans/standards.json`. Not accredited, and not a replacement for any state requirement.

Reading text is copied word for word. The build only joins hard-wrapped lines, keeps verse line breaks, drops picture markers and italic underscores, and splits chapters at paragraph breaks. Original spellings, including the 1896 book's syllable hyphens, are kept.

## Files

- `plans/`: the two plans and `standards.json`.
- `scripts/build.py`: `python3 scripts/build.py --fetch` downloads the sources into `./src` and rebuilds `plans/` (standard library only). `scripts/curation.py`: timeline labels, reviewed content notes, skip summaries, Next shelf and standards. `scripts/scan.py`: the content scan used by the build.
- `scripts/check_links.py`: downloads the sources live and checks every reading against them; `--raw` also checks the files served from this repo.
- `scripts/check_standards.py`: downloads the official standards documents and checks every code's text word for word (needs `pdftotext`).
- `tests/test_plan.py`: offline checks: word for word against the source, nothing added or dropped, paragraph-only splits, caps, notes and tags.
- `MANIFEST.txt`: every file with its size and SHA-256, for loading by raw URL.

## License

The plans are CC0 1.0. Code is MIT. See `LICENSE`.

Questions or ideas? Contact Omega Games at john@playomega.games.
