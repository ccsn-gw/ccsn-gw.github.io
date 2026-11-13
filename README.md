# CCSN Waveform Archive

Website of the supernova gravitational-wave group at the Energetic Cosmos Laboratory,
Nazarbayev University: <https://ccsn-gw.github.io/>

The site is a single static page. There is no build step: GitHub Pages serves the files as they are.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole page: layout, styles, text and scripts |
| `data/signals.txt` | Strain series for the waveform explorer (from `6EOS_4M.csv`) |
| `photos/` | Team portraits, 320 x 320 px JPEG, lowercase file names |
| `favicon.svg`, `og.png` | Browser-tab icon and the preview image shown when the link is shared |
| `404.html`, `robots.txt`, `sitemap.xml` | Not-found page and search-engine files |
| `tools/build_explorer_data.py` | Rebuilds the explorer data from a CSV |

## Updating content

Everything editable sits in a few lists near the top of the `<script>` block in `index.html`:

- `DATASETS` - the Zenodo cards (title, DOI, summary, specification rows, linked paper)
- `PUBS` - the publication list, newest first
- `TEAM` - people, roles, emails and photo paths
- `SITES` - institutions on the collaboration map, with coordinates and number of joint papers

When a dataset is added or its details change, also update the matching entry in the
`application/ld+json` block at the top of the file. Search engines read that block.

File names are case-sensitive on GitHub Pages: `photos/Name.jpg` and `photos/name.jpg` are different files.

## Updating the waveform explorer

```
pip install numpy pandas
python tools/build_explorer_data.py path/to/6EOS_4M.csv
```

This rewrites `data/signals.txt` and the `const DATA=...;` line in `index.html`.

## Previewing locally

```
python -m http.server 8000
```

Then open <http://localhost:8000/>. Opening `index.html` directly from disk shows the page
but not the strain plot, because browsers block loading `data/signals.txt` from a `file://` page.

## Licence

The datasets linked from the site are released under CC BY 4.0 on Zenodo.
