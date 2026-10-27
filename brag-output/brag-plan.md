# /brag-slim — Ashruta the Band

## What it is
A one-page official site for **Ashruta the Band** — a five-piece that plays Bollywood
fusion in rock metal. Dark/crimson, Oswald + Montserrat, parallax and diagonal section
cuts, with a real backend: tRPC + MySQL behind the newsletter, contact and booking forms,
plus an admin dashboard to read the inquiries.

## Angle
The site's own thesis is the collision: *"WHERE TWO WORLDS COLLIDE."* The non-obvious,
specific, true detail that no generic metal-band video could claim is the lineup —
an electric guitarist and a **bansuri flautist** in the same band. That is the hook.
Not "we built a website": the band, the lineup, the set, the tour.

## Hook (first 2s)
The real hero tagline split in half and slammed together: **BOLLYWOOD** in from the left,
**ROCK METAL** in from the right, impact on the downbeat → wordmark. The video *is* the
collision before it says the word.

## Highlights
1. **THE CULT** — all five members, real names and real roles, dealt in one per beat;
   Rachita / **Flute** lands last and holds. The lineup is the proof.
2. **THE SET** — real track titles from the code: *Agni Raag (Fire Melody)*,
   *Tandav Metal*, *Raga of the Fallen*, *Bollywood Inferno*. Debut album coming soon.
3. **ON TOUR** — the three real dates: Mumbai, Delhi, Bangalore.

## Punchline
Wordmark + the real CTAs (**LISTEN NOW** / **TOUR DATES**) and the real handle
`@ashruta_theband`.

## Tone
`cinematic` — trailer-scale, big type, hard impacts, restrained. Inferred from the source:
the site is already cinematic (full-bleed parallax, fixed backgrounds, 5xl Oswald caps,
crimson on black). Nothing is played for a joke; the band isn't a joke.

## Visual identity (taken from the source, not invented)
- Black `#000` ground; crimson `#dc2626` (red-600), `#ef4444` (red-500), `#f87171` (red-400)
- Logo glow reproduced exactly: `drop-shadow(0 0 30px rgba(239, 68, 68, 0.8))`
- Type: **Oswald** 300–700 (headings, tracking-wider caps), **Montserrat** 400–800 (body)
  — the same two families the site loads, self-hosted from Google Fonts into `work/fonts/`
- Member-card geometry copied from `MemberCard.tsx`: `h-80`, rounded-lg, gray-900 body,
  `from-black via-black/50 to-transparent` overlay, red-600/50 border on reveal
- Diagonal section cuts (`clip-path: polygon(0 3%, 100% 0, …)`) reused as transitions

## Asset substitution (stated plainly)
The site's photography is served from a CloudFront host this session's egress proxy blocks,
and the `/manus-storage` uploads (logo, Rachita's portrait, the four performance clips) are
not in the repo. **No real band photo or video was reachable.** Rather than fake a photo of
real people, the member cards use the real card geometry and the real names/roles with a
generated stage-haze texture where the portrait goes, and the wordmark is set in type
instead of using the logo image. Everything *said* on screen is the band's own copy.

## Sound
One piece at **120 BPM** (0.5s/beat, 2s/bar — 20.0s is exactly 10 bars), A minor.
Drone + bansuri-style lead (sine with breath noise and vibrato) over palm-muted saw guitar,
kick/snare on the grid. Transition impacts are tuned to A and sit *under* the music, not on
top of it. Every element is counted from frame 0 off one grid, so nothing drifts.

## Storyboard — 1920×1080, 30fps, 600 frames, 20.0s
| # | Scene | In→Out | Bars/beats | What happens |
|---|---|---|---|---|
| 1 | Collision hook | 0.0–3.0 | b1–b6 | Black. "BOLLYWOOD" in from left (amber), "ROCK METAL" in from right (crimson), impact flash on beat 5 |
| 2 | Wordmark reveal | 3.0–6.0 | b7–b12 | ASHRUTA, letterspaced, red glow; real tagline "BOLLYWOOD FUSION IN ROCK METAL" settles and holds |
| 3 | THE CULT | 6.0–10.5 | b13–b21 | Five real member cards dealt one per beat; Rachita / Flute lifts and holds on the last beat |
| 4 | THE SET | 10.5–14.0 | b22–b28 | Real track titles stack in on beats; "DEBUT ALBUM — COMING SOON" |
| 5 | ON TOUR | 14.0–17.0 | b29–b34 | Three real dates snap in, diagonal cut wipe |
| 6 | Outro | 17.0–20.0 | b35–b40 | Wordmark, real CTAs, @ashruta_theband; settles for the poster frame |

Readability: every line the viewer is meant to read holds ≥0.3s/word *after* it has fully
settled. Transitions dip through black rather than crossfading two busy layouts.

## Share caption
See `share-copy.txt`.
