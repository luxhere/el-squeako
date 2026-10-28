# El Squeako

*tiny tragic concerto for a mechanism that should never have been installed*

A little stone. Sunglasses. A raincoat. A windscreen wiper nobody asked for.

Six slow rubber squeaks make an original miniature: a hesitant rising phrase,
an indignant silence, and an absurdly dignified return. The weather does not improve.

## Attend a performance

Open `index.html` directly in a modern browser. No install, build, or internet required.
If your browser restricts local audio, run `python3 -m http.server 8000` in this
folder and visit `http://localhost:8000`.

**Start with your device volume low.** Click **Begin the ordeal** to start one
16-second performance. Click **Stop the ordeal** to stop; **Mute sound** keeps
the little mechanism moving without audio. Click again for an encore.
Keyboard users can Tab to each control and use Enter or Space.
Reduced-motion preferences keep the wiper still. Leaving the tab stops the show.
Nothing plays until you ask. There is no telemetry, external dependency, or
network request initiated by the page (the recording download is a local file).

## A souvenir

`preview.wav` is an actual shareable 16-second mono PCM16 recording, not a link
to an audio service. It and the live Web Audio performance use the same original
six-gesture score, curved pitches, soft harmonic friction, and smooth envelopes.
The browser applies an additional conservative master gain; perceived loudness
still depends on your equipment. No outside recordings or copyrighted music used.

### Regenerate and verify

```sh
python3 render_squeako.py     # writes preview.wav (take one: the mournful ghost)
python3 render_squeako.py --v2 # writes preview-v2.wav (take two: rubber stick-slip)
python3 render_squeako.py --v3 # writes preview-v3.wav (take three: the long release)
python3 -m unittest -v         # eight tests: three each for takes one and two, two for take three
```

## Take two: preview-v2.wav

Take one sounded like a mournful ghost. Take two chases the actual rubber: short
uneven chirps in bursts (the blade catches, tension rises, it lets go), an
indignant silence, then single decisive strokes on the way back. Higher, dryer,
shorter than the ghost motif: friction, not lament.

Take one (`preview.wav`) is preserved as recorded, and take two
(`preview-v2.wav`) likewise. Take three won the second verdict: chitter,
chitter, long-swipe. It now plays in the browser page, and the download link
serves `preview-v3.wav`.

## Take three: preview-v3.wav

Take three keeps take two's chatter and pays the long stroke the piece owed:
the effortful drag mid-burst opens out, and the finale finally lets go. Same
engine, two gestures widened. The page plays it.

Tests check finite samples, conservative peak, silence, smooth sample changes,
duration/PCM format, deterministic rendering, and a self-contained static page.
The inline SVG illustration, composition, and code are original to this project.

MIT licensed. For the avoidance of doubt, the stone has not approved the invention.
