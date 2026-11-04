"""Generate an original, royalty-free soft background track (pad + arpeggio + light beat).
Usage: python3 music.py seconds out.wav [seed]"""
import sys, wave, numpy as np

secs = float(sys.argv[1]); out = sys.argv[2]; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
sr = 44100; n = int(secs * sr); t = np.arange(n) / sr
rng = np.random.default_rng(seed)
bpm = 96; beat = 60 / bpm; bar = beat * 4
progs = [[60, 57, 53, 55], [57, 53, 60, 55], [62, 58, 53, 60]]  # root notes (MIDI)
prog = progs[seed % len(progs)]
f = lambda m: 440 * 2 ** ((m - 69) / 12)
mix = np.zeros(n)

for i in range(int(secs / bar) + 1):
    root = prog[i % 4]; s0 = int(i * bar * sr); s1 = min(n, int((i + 1) * bar * sr))
    if s0 >= n: break
    tt = t[s0:s1] - t[s0]
    third = 3 if root in (57, 62) else 4
    env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.4)
    for m in (root - 12, root, root + third, root + 7):  # warm pad
        mix[s0:s1] += 0.07 * env * (np.sin(2 * np.pi * f(m) * tt) + 0.3 * np.sin(2 * np.pi * f(m) * 2.003 * tt))
    arp = [root + 12, root + 12 + third, root + 19, root + 12 + third]
    for k in range(8):  # eighth-note pluck arpeggio
        a0 = s0 + int(k * beat / 2 * sr); a1 = min(n, a0 + int(0.45 * sr))
        if a0 >= n: break
        ta = t[a0:a1] - t[a0]
        mix[a0:a1] += 0.05 * np.exp(-ta * 7) * np.sin(2 * np.pi * f(arp[k % 4]) * ta)
    for k in range(4):  # soft kick on each beat, hat on off-beats
        k0 = s0 + int(k * beat * sr); k1 = min(n, k0 + int(0.25 * sr))
        if k0 >= n: break
        tk = t[k0:k1] - t[k0]
        mix[k0:k1] += 0.18 * np.exp(-tk * 18) * np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk)
        h0 = k0 + int(beat / 2 * sr); h1 = min(n, h0 + int(0.05 * sr))
        if h0 < n:
            mix[h0:h1] += 0.03 * np.exp(-(t[h0:h1] - t[h0]) * 80) * rng.standard_normal(h1 - h0)

fade = int(1.5 * sr); mix[:fade] *= np.linspace(0, 1, fade); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.8
st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes())
print(out)
