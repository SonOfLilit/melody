from constants import *

import midi

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
assert len(list(repeat(2, 100, m()))) == 2 * 2
assert len(list(repeat(4, 100, m()))) == 4 * 2
