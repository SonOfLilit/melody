import midi

def to_ticks(duration):
    return duration

def to_events(notes):
    time = 0
    for note in notes:
        duration = to_ticks(note['duration'])
        yield midi.NoteOnEvent(tick=0, pitch=note['pitch'], velocity=100)
        yield midi.NoteOffEvent(tick=duration, pitch=note['pitch'])
        time += duration

def to_midi(notes, tempo=140):
    pattern = midi.Pattern()
    pattern.append([
        midi.TimeSignatureEvent(tick=0, data=[4, 2, 24, 8]),
                midi.KeySignatureEvent(tick=0, data=[0, 0]),
                midi.EndOfTrackEvent(tick=1, data=[])])
    track = midi.Track()
    pattern.append(track)
    track.extend([
        midi.ControlChangeEvent(tick=0, channel=0, data=[91, 58]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[10, 69]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[0, 0]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[32, 0]),
        midi.ProgramChangeEvent(tick=0, channel=0, data=[24])])
    for event in to_events(notes):
        track.append(event)
    track.append(midi.EndOfTrackEvent(tick=1, data=[]))
    return pattern

def write(pattern, path):
    midi.write_midifile(path, pattern)
