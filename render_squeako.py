#!/usr/bin/env python3
"""An original, deterministic miniature for rubber and injured dignity."""
import math
import struct
import wave
from pathlib import Path

RATE = 24000
DURATION = 16
# time, duration, starting pitch, ending pitch: a hesitant minor motif, then reply.
SCORE = [(0.8, 1.65, 293.66, 349.23), (2.65, 1.25, 349.23, 329.63),
         (4.15, 1.85, 329.63, 220.0), (9.0, 2.0, 220.0, 293.66),
         (11.3, 1.5, 261.63, 246.94), (13.0, 2.2, 246.94, 220.0)]


def synthesize():
    samples = [0.0] * (RATE * DURATION)
    for start, duration, low, high in SCORE:
        phase = 0.0
        for j in range(round(duration * RATE)):
            t = j / RATE
            u = t / duration
            # Curved pitch, rubbery friction flutter, soft harmonic rasp.
            frequency = (low + (high - low) * (0.5 - 0.5 * math.cos(math.pi * u)))
            frequency *= 1 + 0.018 * math.sin(2 * math.pi * 5.3 * t)
            phase += 2 * math.pi * frequency / RATE
            envelope = math.sin(math.pi * u) ** 1.6
            friction = 0.74 + 0.26 * math.sin(2 * math.pi * 13 * t) ** 2
            value = 0.115 * envelope * friction * (math.sin(phase) +
                      0.24 * math.sin(2 * phase + 0.7) + 0.09 * math.sin(3 * phase))
            samples[round(start * RATE) + j] += value
    assert all(math.isfinite(x) for x in samples)
    assert max(map(abs, samples)) < 0.17
    return samples


def render(destination=Path(__file__).with_name('preview.wav')):
    samples = synthesize()
    pcm = struct.pack('<' + 'h' * len(samples), *(round(x * 32767) for x in samples))
    with wave.open(str(destination), 'wb') as output:
        output.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        output.writeframes(pcm)
    print(f'{Path(destination).name}: {DURATION}s, mono PCM16, peak {max(map(abs, samples)):.3f}')


# --- Take two: stick-slip chatter, uneven catches, dignified return. ---
# time, duration, starting pitch, ending pitch: short rubbery chirps in bursts,
# an indignant silence, then single decisive strokes. Higher, dryer, shorter
# than the ghost motif: friction, not lament.
SCORE_V2 = [
    (0.60, 0.09, 620, 1150), (0.72, 0.06, 700, 1280), (0.84, 0.12, 580, 1050),
    (1.60, 0.07, 760, 1340), (1.71, 0.05, 900, 1480),
    (2.45, 0.14, 540, 980),
    (3.10, 0.06, 820, 1390), (3.20, 0.05, 700, 1210),
    (4.05, 0.10, 640, 1170),
    (4.70, 0.06, 880, 1420), (4.80, 0.08, 750, 1250),
    (5.55, 0.13, 560, 990),
    (9.60, 0.10, 700, 1300),
    (10.45, 0.07, 850, 1450),
    (11.60, 0.09, 660, 1240),
    (12.90, 0.06, 940, 1490),
    (14.10, 0.11, 600, 1120),
]


def _deterministic_noise(size):
    """Fixed-seed chatter, one-pole smoothed so it rasps instead of clicks."""
    state = 12345
    smoothed = []
    y = 0.0
    for _ in range(size):
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        n = (state / 0x3FFFFFFF) - 1.0
        y += 0.18 * (n - y)
        smoothed.append(y)
    return smoothed


def synthesize_v2():
    samples = [0.0] * (RATE * DURATION)
    rasp = _deterministic_noise(len(samples))
    for start, duration, low, high in SCORE_V2:
        offset = round(start * RATE)
        phase = 0.0
        for j in range(round(duration * RATE)):
            t = j / RATE
            u = t / duration
            # Fast glide: the blade catches, tension rises, it lets go.
            frequency = low + (high - low) * (u ** 0.7)
            frequency *= 1 + 0.03 * math.sin(2 * math.pi * 17 * t)
            phase += 2 * math.pi * frequency / RATE
            attack = min(t / 0.004, 1.0)
            release = (1.0 - u) ** 1.5
            envelope = attack * release
            friction = 0.65 + 0.35 * abs(math.sin(2 * math.pi * 28 * t))
            voice = (math.sin(phase) +
                     0.18 * math.sin(2 * phase) + 0.05 * math.sin(3 * phase))
            value = (0.12 * envelope * friction * voice +
                     0.10 * envelope * rasp[offset + j])
            samples[offset + j] += value
    assert all(math.isfinite(x) for x in samples)
    assert max(map(abs, samples)) < 0.17
    return samples


def render_v2(destination=Path(__file__).with_name('preview-v2.wav')):
    samples = synthesize_v2()
    pcm = struct.pack('<' + 'h' * len(samples), *(round(x * 32767) for x in samples))
    with wave.open(str(destination), 'wb') as output:
        output.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        output.writeframes(pcm)
    print(f'{Path(destination).name}: {DURATION}s, mono PCM16, peak {max(map(abs, samples)):.3f}')


if __name__ == '__main__':
    import sys
    render_v2() if '--v2' in sys.argv else render()
