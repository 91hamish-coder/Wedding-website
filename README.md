# Message site

One page per message, generated from a spreadsheet.

## Use it
1. Edit `messages.csv` (columns: `slug`, `message`).
   - `slug` is the URL path: slug `7` gives `yoursite.com/7`. Leave it blank to use the row number.
   - A blank line inside a message starts a new paragraph.
2. Run `python build.py` (Python 3, no installs needed).
3. Upload the `dist/` folder to a static host.

## Host it
- Netlify: drag the `dist` folder onto app.netlify.com/drop
- Cloudflare Pages, GitHub Pages, Vercel: point them at `dist` (or your repo)

## Change the look
Edit `templates/page.html` and `templates/style.css`, then re-run `python build.py`.
