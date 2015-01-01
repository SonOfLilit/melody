from constants import *
import midi

from heapq import heappush, heappop

TEMPO_SETTINGS = [
        midi.TimeSignatureEvent(tick=0, data=[4, 2, 24, 8]),
        midi.KeySignatureEvent(tick=0, data=[0, 0])]

BASIC_SETTINGS = [
        midi.ControlChangeEvent(tick=0, channel=0, data=[91, 58]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[10, 69]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[0, 0]),
        midi.ControlChangeEvent(tick=0, channel=0, data=[32, 0]),
        midi.ProgramChangeEvent(tick=0, channel=0, data=[24])]

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

def pattern():
    pattern = midi.Pattern()
    pattern.append(TEMPO_SETTINGS)
    pattern.append(BASIC_SETTINGS)
    return pattern

def write(pattern, path):
    for i, track in enumerate(pattern):
        if not is_midi_track(track):
            pattern[i] = list(to_events(track))
        pattern[i].append(midi.EndOfTrackEvent(tick=1, data=[]))
    print pattern
    midi.write_midifile(path, pattern)

def is_midi_track(track):
    return isinstance(track, list) and track and isinstance(track[0], midi.AbstractEvent)
