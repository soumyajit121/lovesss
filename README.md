# For Sneha — an interactive romantic experience

A single scrolling page, built with Streamlit, ending in a marriage proposal. Everything —
code, photos, song, and docs — lives in **one flat folder**. No `assets` subfolder, no other
subfolder, nothing nested.

## Folder layout (this is exactly what your GitHub repo should look like)
```
app.py
requirements.txt
README.md
.gitignore
photo01.jpg
photo02.jpg
photo03.jpg
photo04.jpg
photo05.jpg
photo06.jpg
photo07.jpg
photo08.jpg
photo09.jpg
photo10.jpg
song_full.mp3
```
`app.py` looks for the photos and the song directly next to itself. If anything's missing, it
shows an on-screen error telling you exactly what's missing instead of failing silently.

## Deploy from GitHub (Streamlit Community Cloud)
1. Push every file above into the root of a GitHub repo (not inside a folder):
   ```
   git add -A
   git commit -m "add app and media"
   git push
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"**, pick your repo and branch, set the main file path to `app.py`, and
   click **Deploy**.
4. First load takes a little longer (it's base64-encoding the photos and song into the page) —
   every load after that is fast.
5. If you push more changes later, use the app's ⋮ menu → **Reboot app** so it pulls the latest
   commit.

## Run it locally instead
```
pip install -r requirements.txt
streamlit run app.py
```
Requires an internet connection once, to load two Google Fonts — everything else (all 10
photos, the full song) is bundled and works offline.

## The experience, in order
1. **Loading screen** with a memory-match puzzle (4 pairs of hearts) that unlocks the page.
2. **Love blast** — a burst of hearts and a glowing "I Love You" message.
3. **Music starts right with the blast**, at **1:46** into `song_full.mp3`, and loops back to
   that point instead of the very beginning.
4. **One continuous scrolling page**: a hero intro, a photo slideshow, "Why I Love You" cards, a
   love letter, a scrolling promise ticker, and an "Our Song" button that opens a full-screen
   synced visual experience.
5. **The finale — a marriage proposal.** An envelope you tap open, revealing a heartfelt message
   that ends in "Will You Marry Me?" with two ways to say yes, each triggering a big celebration.

## Configuration
Open `app.py` and edit the two lines near the top:
```python
HER_NAME = "Sneha"
SONG_START_SECONDS = 106   # 1:46 -- where the music picks up after the love blast
```

## Editing the words
- **Love letter** — the `<div class="letter">` block in the HTML body.
- **Proposal message** — the `<div class="finalCard">` block, right after the "Our Song" section.
- **Promise ticker / Why I Love You cards** — directly in their HTML sections.

## Note on the song
The app never bundles or hard-codes lyrics — it only plays the audio file you provide
(`song_full.mp3`), starting at whatever timestamp you set.

Made with love: Soumyajit + Sneha
