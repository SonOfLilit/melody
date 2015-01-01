import melody
import play
import midi

def transpose(halftones, notes):
    for note in notes:
        note = dict(note)
        note['pitch'] += halftones
        yield note

arpeggio = list(melody.repeat(1, 600,
    melody.merge([
        melody.melody([
            {'duration': 600, 'pitch': midi.C_3}
        ]), melody.melody([
            {'duration': 100, 'pitch': midi.C_4},
            {'duration': 100, 'pitch': midi.E_4},
            {'duration': 100, 'pitch': midi.G_4},
            {'duration': 100, 'pitch': midi.C_6},
            {'duration': 100, 'pitch': midi.G_4},
            {'duration': 100, 'pitch': midi.E_4},
        ])
    ])
))
pattern = play.pattern()
pattern.append(arpeggio)
pattern.append(transpose(12, arpeggio))
play.write(pattern, 'test.mid')
