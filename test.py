import melody
import midi

midi = melody.to_midi([{'duration': 100, 'pitch': midi.C_3}, {'duration': 100, 'pitch': midi.C_4}] * 10)
print midi
melody.write(midi, 'test.mid')
