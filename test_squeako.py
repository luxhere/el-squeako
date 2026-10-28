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
        for start, duration, low, high in music.SCORE_V2:
            self.assertLessEqual(start+duration, music.DURATION)
        # Both renderers retain the exact same take-two score (seventeen gestures).
        js_score = re.search(r'const score = (\[.*?\]);', html).group(1)
        import json
        self.assertEqual(json.loads(js_score), [list(note) for note in music.SCORE_V2])


class TakeTwoTests(unittest.TestCase):
    """preview.wav (the ghost) stays untouched; v2 is its own artifact."""
    @classmethod
    def setUpClass(cls):
        cls.samples = music.synthesize_v2()

    def test_v2_safe_uneven_and_smooth(self):
        samples = self.samples
        self.assertTrue(all(math.isfinite(x) for x in samples))
        self.assertGreater(max(map(abs, samples)), .05)
        self.assertLess(max(map(abs, samples)), .17)
        # Loosest sane bound: 1.5 kHz glides move more per sample than the
        # ghost's 300 Hz moan. A click would jump near 0.4; this must not.
        self.assertLess(max(abs(b-a) for a, b in zip(samples, samples[1:])), .15)
        # Indignant silence intact between the bursts and the dignified return.
        self.assertTrue(all(x == 0 for x in samples[int(6.2*music.RATE):int(9.2*music.RATE)]))

    def test_v2_score_fits_the_night(self):
        self.assertTrue(music.SCORE_V2)
        for start, duration, low, high in music.SCORE_V2:
            self.assertLessEqual(start + duration, music.DURATION)
            self.assertLess(low, high)
            self.assertLess(duration, 0.2)  # chirps, not moans

    def test_v2_preview_file_matches_synthesis(self):
        with wave.open(str(ROOT / 'preview-v2.wav'), 'rb') as audio:
            self.assertEqual((audio.getnchannels(), audio.getsampwidth(), audio.getframerate()), (1, 2, music.RATE))
            self.assertEqual(audio.getnframes()/audio.getframerate(), 16)
            actual = audio.readframes(audio.getnframes())
        expected = struct.pack('<'+'h'*len(self.samples), *(round(x*32767) for x in self.samples))
        self.assertEqual(actual, expected)


class TakeThreeTests(unittest.TestCase):
    """Take three: take two's chatter plus the long release it owed us."""
    @classmethod
    def setUpClass(cls):
        cls.samples = music.synthesize_v2(music.SCORE_V3)

    def test_v3_keeps_the_chatter_and_pays_the_release(self):
        samples = self.samples
        self.assertTrue(all(math.isfinite(x) for x in samples))
        self.assertGreater(max(map(abs, samples)), .05)
        self.assertLess(max(map(abs, samples)), .17)
        self.assertLess(max(abs(b-a) for a, b in zip(samples, samples[1:])), .15)
        self.assertTrue(all(x == 0 for x in samples[int(6.2*music.RATE):int(9.2*music.RATE)]))
        # The two widened gestures exist; the chirps survive around them.
        self.assertGreaterEqual(sum(1 for n in music.SCORE_V3 if n[1] >= .4), 2)
        self.assertGreaterEqual(sum(1 for n in music.SCORE_V3 if n[1] < .2), 14)
        # No gesture overlaps another, and all fit the 16 seconds.
        ordered = sorted(music.SCORE_V3)
        for (start, duration, _, _), (next_start, _, _, _) in zip(ordered, ordered[1:]):
            self.assertLessEqual(start + duration, next_start)
        for start, duration, _, _ in ordered:
            self.assertLessEqual(start + duration, music.DURATION)

    def test_v3_preview_file_matches_synthesis(self):
        with wave.open(str(ROOT / 'preview-v3.wav'), 'rb') as audio:
            self.assertEqual((audio.getnchannels(), audio.getsampwidth(), audio.getframerate()), (1, 2, music.RATE))
            self.assertEqual(audio.getnframes()/audio.getframerate(), 16)
            actual = audio.readframes(audio.getnframes())
        expected = struct.pack('<'+'h'*len(self.samples), *(round(x*32767) for x in self.samples))
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
