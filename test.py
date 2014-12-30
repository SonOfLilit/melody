import melody
import midi

arpeggio = list(
    melody.melody([
        {'duration': 100, 'pitch': midi.C_4},
        {'duration': 100, 'pitch': midi.E_4},
        {'duration': 100, 'pitch': midi.G_4},
        {'duration': 100, 'pitch': midi.C_6},
        {'duration': 100, 'pitch': midi.G_4},
        {'duration': 100, 'pitch': midi.E_4},
    ])) + [{'time': 700, 'duration': 400, 'pitch': midi.C_4}]
midi = melody.to_midi(arpeggio)
print midi
melody.write(midi, 'test.mid')
