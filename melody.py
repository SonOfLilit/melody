import midi

for name in 'pitch time duration'.split():
    globals()[name.upper()] = name

TEMPO_SETTINGS = [
        midi.TimeSignatureEvent(tick=0, data=[4, 2, 24, 8]),
                midi.KeySignatureEvent(tick=0, data=[0, 0]),
                midi.EndOfTrackEvent(tick=1, data=[])]

BASIC_SETTINGS = [
        midi.ControlChangeEvent(tick=0, channel=0, data=[91, 58]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[10, 69]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[0, 0]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[32, 0]),
        midi.ProgramChangeEvent(tick=0, channel=0, data=[24])]

def melody(notes, duration=None, pitch=None):
    time = 0
    for note in notes:
        note = dict(note)
        if duration is not None:
            note[DURATION] = duration
        if pitch is not None:
            note[PITCH] = pitch
        note[TIME] = time
        yield note
        time += note[DURATION]
assert list(melody([])) == []
assert list(melody([{DURATION: 100}])) == [{DURATION: 100, TIME: 0}]
assert list(melody([{DURATION: 100}] * 2)) == [{TIME: 0, DURATION: 100}, {TIME: 100, DURATION: 100}]
assert list(melody([{}], duration=200)) == [{TIME: 0, DURATION: 200}]

def idxmin(items, key=None):
    if key is not None:
        k = lambda x: key(x[1])
    else:
        k = lambda x: x[1]
    return min(enumerate(items), key=k)
assert idxmin([3]) == (0, 3)
assert idxmin([3, 1, 0, 2]) == (2, 0)
assert idxmin([3, 1, 5, 2], key=lambda x: x % 3) == (0, 3)
try:
    idxmin([])
except ValueError:
    pass
else:
    assert False

def merge(melodies):
    melodies = map(iter, melodies)
    firsts = []
    i = 0
    while i < len(melodies):
        try:
            firsts.append(melodies[i].next())
        except StopIteration:
            del melodies[i]
        else:
            i += 1
    time = 0
    while melodies:
        index, note = idxmin(firsts, key=lambda m: m[TIME])
        if note[TIME] < time:
            raise ValueError('Melodies must be time-sorted')
        yield note
        time = note[TIME]
        try:
            firsts[index] = melodies[index].next()
        except StopIteration:
            del firsts[index]
            del melodies[index]
assert list(merge([])) == []
assert list(merge([[{TIME: 100}, {TIME: 200}]])) == [
    {TIME: 100}, {TIME: 200}]
assert list(merge([iter([{TIME: 100}, {TIME: 200}])])) == [
    {TIME: 100}, {TIME: 200}]
assert list(merge([[{TIME: 100}, {TIME: 200}], [{TIME: 50}]])) == [
    {TIME: 50}, {TIME: 100}, {TIME: 200}]
assert list(merge([[{TIME: 100}, {TIME: 200}], [{TIME: 100}]])) == [
    {TIME: 100}, {TIME: 100}, {TIME: 200}]
assert list(merge([[{TIME: 100}, {TIME: 200}], [{TIME: 150}]])) == [
    {TIME: 100}, {TIME: 150}, {TIME: 200}]
assert list(merge([[{TIME: 100}, {TIME: 200}], [{TIME: 200}]])) == [
    {TIME: 100}, {TIME: 200}, {TIME: 200}]
assert list(merge([[{TIME: 100}, {TIME: 200}], [{TIME: 250}]])) == [
    {TIME: 100}, {TIME: 200}, {TIME: 250}]
assert list(merge([[{TIME: 200}], [{TIME: 100}, {TIME: 300}]])) == [
    {TIME: 100}, {TIME: 200}, {TIME: 300}]
try:
    list(merge([[{TIME: 200}, {TIME: 100}]]))
except ValueError:
    pass
else:
    assert False

def to_ticks(duration):
    return duration

def to_events(notes):
    time = 0
    for note in notes:
        assert note[TIME] >= time
        duration = to_ticks(note[DURATION])
        yield midi.NoteOnEvent(tick=note[TIME] - time, pitch=note[PITCH], velocity=100)
        time = note[TIME]
        yield midi.NoteOffEvent(tick=duration, pitch=note[PITCH])
        time += duration
assert list(to_events([])) == []
assert list(to_events([
    {TIME: 0, DURATION: 100, PITCH: midi.C_3},
    {TIME: 100, DURATION: 100, PITCH: midi.D_3}])) == [
        midi.NoteOnEvent(tick=0, pitch=midi.C_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.C_3, velocity=100),
        midi.NoteOnEvent(tick=0, pitch=midi.D_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.D_3, velocity=100)]
print list(to_events([
    {TIME: 0, DURATION: 50, PITCH: midi.C_3},
    {TIME: 100, DURATION: 100, PITCH: midi.D_3}]))
assert list(to_events([
    {TIME: 0, DURATION: 50, PITCH: midi.C_3},
    {TIME: 100, DURATION: 100, PITCH: midi.D_3}])) == [
        midi.NoteOnEvent(tick=0, pitch=midi.C_3, velocity=100),
        midi.NoteOffEvent(tick=50, pitch=midi.C_3, velocity=100),
        midi.NoteOnEvent(tick=50, pitch=midi.D_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.D_3, velocity=100)]

def to_midi(notes, tempo=140):
    pattern = midi.Pattern()
    pattern.append(TEMPO_SETTINGS)
    track = midi.Track()
    pattern.append(track)
    track.extend(BASIC_SETTINGS)
    for event in to_events(notes):
        track.append(event)
    track.append(midi.EndOfTrackEvent(tick=1, data=[]))
    return pattern

def write(pattern, path):
    midi.write_midifile(path, pattern)
