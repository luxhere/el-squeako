import math
import re
import struct
import unittest
import wave
from pathlib import Path
import render_squeako as music

ROOT = Path(__file__).parent


class SqueakoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.samples = music.synthesize()

    def test_safe_samples_and_silence(self):
        samples = self.samples
        self.assertTrue(all(math.isfinite(x) for x in samples))
        self.assertGreater(max(map(abs, samples)), .05)
        self.assertLess(max(map(abs, samples)), .17)
        self.assertLess(max(abs(b-a) for a, b in zip(samples, samples[1:])), .03)
        self.assertTrue(all(x == 0 for x in samples[int(6.1*music.RATE):9*music.RATE]))

    def test_actual_preview_matches_deterministic_synthesis(self):
        with wave.open(str(ROOT / 'preview.wav'), 'rb') as audio:
            self.assertEqual((audio.getnchannels(), audio.getsampwidth(), audio.getframerate()), (1, 2, music.RATE))
            self.assertEqual(audio.getcomptype(), 'NONE')
            self.assertEqual(audio.getnframes()/audio.getframerate(), 16)
            actual = audio.readframes(audio.getnframes())
        expected = struct.pack('<'+'h'*len(self.samples), *(round(x*32767) for x in self.samples))
        self.assertEqual(actual, expected)

    def test_static_private_page(self):
        html = (ROOT / 'index.html').read_text()
        self.assertNotRegex(html, r'(?i)(https?://|fetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|autoplay|@import)')
        self.assertNotRegex(html, r'(?i)<(?:script|img|iframe|audio)[^>]+src=')
        self.assertIn('prefers-reduced-motion', html)
        self.assertIn('aria-pressed', html)
        self.assertIn('aria-live="polite"', html)
        for start, duration, low, high in music.SCORE:
            self.assertLessEqual(start+duration, music.DURATION)
        # Both renderers retain the exact same six-gesture score.
        js_score = re.search(r'const score = (\[.*?\]);', html).group(1)
        import json
        self.assertEqual(json.loads(js_score), [list(note) for note in music.SCORE])


if __name__ == '__main__':
    unittest.main()
