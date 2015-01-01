import midi
from heapq import heappush, heappop

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

def delay(delta, notes):
    for note in notes:
        note = dict(note)
        note[TIME] += delta
        yield note
assert list(delay(100, [])) == []
assert list(delay(100, [{TIME: 5}])) == [{TIME: 105}]
assert list(delay(100, [{TIME: 5}, {TIME: 15}])) == [{TIME: 105}, {TIME: 115}]
assert list(delay(0, [{TIME: 5}, {TIME: 15}])) == [{TIME: 5}, {TIME: 15}]

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

class StreamCloner(object):
    def __init__(self, stream):
        self.stream = stream
        self.past = []

    def read(self):
        """
        Appends next item to self.past, raises StopIteration if no more items.
        """
        self.past.append(self.stream.next())

    def clone(self):
        i = 0
        while True:
            while i >= len(self.past):
                self.read()
            yield self.past[i]
            i += 1
stream = StreamCloner(iter([1, 2, 3]))
assert list(stream.clone()) == list(stream.clone()) == [1, 2, 3]
stream = StreamCloner(iter([1, 2, 3]))
assert zip(stream.clone(), stream.clone()) == [(1, 1), (2, 2), (3, 3)]

def repeat(n, period, notes):
    cloner = StreamCloner(iter(notes))
    clones = (cloner.clone() for i in xrange(n))
    return merge(delay(i * period, notes_tee) for i, notes_tee in enumerate(clones))
assert list(repeat(3, 100, [])) == []
assert list(repeat(3, 100, [{TIME: 0, DURATION: 100}])) == [
    {TIME: 0, DURATION: 100},
    {TIME: 100, DURATION: 100},
    {TIME: 200, DURATION: 100},
]
assert list(repeat(3, 100, [{TIME: 0, DURATION: 50}])) == [
    {TIME: 0, DURATION: 50},
    {TIME: 100, DURATION: 50},
    {TIME: 200, DURATION: 50},
]
assert list(repeat(3, 75, [{TIME: 0, DURATION: 50}, {TIME: 100, DURATION: 100}])) == [
    {TIME: 0, DURATION: 50},
    {TIME: 75, DURATION: 50},
                             {TIME: 100, DURATION: 100},
    {TIME: 150, DURATION: 50},
                             {TIME: 175, DURATION: 100},
                             {TIME: 250, DURATION: 100},
]
m = lambda: melody([
            {'duration': 100, 'pitch': midi.C_4},
            {'duration': 100, 'pitch': midi.E_4}])
print list(m())
print list(repeat(1, 100, m()))
print list(repeat(2, 100, m()))
assert len(list(repeat(2, 100, m()))) == 2 * 2
assert len(list(repeat(4, 100, m()))) == 4 * 2

def to_ticks(duration):
    return duration

def counter(i=0):
    while True:
        yield i
        i += 1

def to_events(notes):
    time = 0
    queue = []
    # makes the queue sorting stable
    count = counter()
    for note in notes:
        note_time = to_ticks(note[TIME])
        duration = to_ticks(note[DURATION])
        heappush(queue, (note_time, count.next(), (midi.NoteOnEvent, note[PITCH])))
        heappush(queue, (note_time + duration, count.next(), (midi.NoteOffEvent, note[PITCH])))
        while True:
            if not queue:
                # no more pending events, next note!
                break
            event_data = heappop(queue)
            event_time, _, (event_type, pitch) = event_data
            if event_time > note_time:
                # we can't know which is the next event
                # until we see when the next note starts
                # (until now we could because we knew the
                # next note starts at note_time)

                # put it back
                heappush(queue, event_data)
                break
            assert event_time >= time
            yield event_type(tick=event_time - time, pitch=pitch, velocity=100)
            time = event_time
    # drain all remaining events
    while queue:
        event_time, _, (event_type, pitch) = heappop(queue)
        assert event_time >= time
        yield event_type(tick=event_time - time)
        time = event_time
assert list(to_events([])) == []
assert list(to_events([
    {TIME: 0, DURATION: 100, PITCH: midi.C_3},
    {TIME: 100, DURATION: 100, PITCH: midi.D_3}])) == [
        midi.NoteOnEvent(tick=0, pitch=midi.C_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.C_3, velocity=100),
        midi.NoteOnEvent(tick=0, pitch=midi.D_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.D_3, velocity=100)]
assert list(to_events([
    {TIME: 0, DURATION: 50, PITCH: midi.C_3},
    {TIME: 100, DURATION: 100, PITCH: midi.D_3}])) == [
        midi.NoteOnEvent(tick=0, pitch=midi.C_3, velocity=100),
        midi.NoteOffEvent(tick=50, pitch=midi.C_3, velocity=100),
        midi.NoteOnEvent(tick=50, pitch=midi.D_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.D_3, velocity=100)]
assert list(to_events([
    {TIME: 0, DURATION: 400, PITCH: midi.C_3},
    {TIME: 100, DURATION: 100, PITCH: midi.D_3}])) == [
        midi.NoteOnEvent(tick=0, pitch=midi.C_3, velocity=100),
        midi.NoteOnEvent(tick=100, pitch=midi.D_3, velocity=100),
        midi.NoteOffEvent(tick=100, pitch=midi.D_3, velocity=100),
        midi.NoteOffEvent(tick=200, pitch=midi.C_3, velocity=100)]

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
