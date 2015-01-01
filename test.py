import melody
import midi

arpeggio = melody.repeat(4, 600,
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
)
pattern = melody.to_midi(arpeggio)
#print pattern
melody.write(pattern, 'test.mid')
