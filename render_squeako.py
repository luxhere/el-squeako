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


if __name__ == '__main__':
    render()
