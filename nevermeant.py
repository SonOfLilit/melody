import melody
import play
import midi

pattern = play.pattern(tempo=65)
pattern.append([
    {'time': 0, 'duration': 800, 'pitch': midi.A_3},
    {'time': 0, 'duration': 200, 'pitch': midi.B_4},
    {'time': 0, 'duration': 200, 'pitch': midi.C_5},
    {'time': 0, 'duration': 200, 'pitch': midi.E_5},
    {'time': 200, 'duration': 200, 'pitch': midi.B_4},
    {'time': 200, 'duration': 200, 'pitch': midi.C_5},
    {'time': 200, 'duration': 200, 'pitch': midi.E_5},
    {'time': 400, 'duration': 200, 'pitch': midi.A_4},
    {'time': 400, 'duration': 200, 'pitch': midi.C_5},
    {'time': 400, 'duration': 200, 'pitch': midi.E_5},
    {'time': 600, 'duration': 200, 'pitch': midi.A_4},
    {'time': 600, 'duration': 200, 'pitch': midi.C_5},
    {'time': 600, 'duration': 200, 'pitch': midi.E_5},
    {'time': 800, 'duration': 800, 'pitch': midi.G_3},
    {'time': 800, 'duration': 200, 'pitch': midi.B_4},
    {'time': 800, 'duration': 200, 'pitch': midi.C_5},
    {'time': 800, 'duration': 200, 'pitch': midi.E_5},
    {'time': 1000, 'duration': 200, 'pitch': midi.B_4},
    {'time': 1000, 'duration': 200, 'pitch': midi.C_5},
    {'time': 1000, 'duration': 200, 'pitch': midi.E_5},
    {'time': 1200, 'duration': 200, 'pitch': midi.A_4},
    {'time': 1200, 'duration': 200, 'pitch': midi.C_5},
    {'time': 1200, 'duration': 200, 'pitch': midi.E_5},
    {'time': 1400, 'duration': 200, 'pitch': midi.A_4},
    {'time': 1400, 'duration': 200, 'pitch': midi.C_5},
    {'time': 1400, 'duration': 200, 'pitch': midi.E_5},
    {'time': 1600, 'duration': 800, 'pitch': midi.F_3},
    {'time': 1600, 'duration': 200, 'pitch': midi.B_4},
    {'time': 1600, 'duration': 200, 'pitch': midi.C_5},
    {'time': 1600, 'duration': 200, 'pitch': midi.E_5},
    {'time': 1800, 'duration': 200, 'pitch': midi.B_4},
    {'time': 1800, 'duration': 200, 'pitch': midi.C_5},
    {'time': 1800, 'duration': 200, 'pitch': midi.E_5},
    {'time': 2000, 'duration': 200, 'pitch': midi.A_4},
    {'time': 2000, 'duration': 200, 'pitch': midi.C_5},
    {'time': 2000, 'duration': 200, 'pitch': midi.E_5},
    {'time': 2200, 'duration': 200, 'pitch': midi.A_4},
    {'time': 2200, 'duration': 200, 'pitch': midi.C_5},
    {'time': 2200, 'duration': 200, 'pitch': midi.E_5},
    {'time': 2400, 'duration': 800, 'pitch': midi.E_3},
    {'time': 2400, 'duration': 200, 'pitch': midi.A_4},
    {'time': 2400, 'duration': 200, 'pitch': midi.B_4},
    {'time': 2400, 'duration': 200, 'pitch': midi.E_5},
    {'time': 2600, 'duration': 200, 'pitch': midi.A_4},
    {'time': 2600, 'duration': 200, 'pitch': midi.B_4},
    {'time': 2600, 'duration': 200, 'pitch': midi.E_5},
    {'time': 2800, 'duration': 200, 'pitch': midi.Gs_4},
    {'time': 2800, 'duration': 200, 'pitch': midi.B_4},
    {'time': 2800, 'duration': 200, 'pitch': midi.E_5},
    {'time': 3000, 'duration': 200, 'pitch': midi.Gs_4},
    {'time': 3000, 'duration': 200, 'pitch': midi.B_4},
    {'time': 3000, 'duration': 200, 'pitch': midi.E_5},

    {'time': 3200, 'duration': 800, 'pitch': midi.A_3},
    {'time': 3200, 'duration': 200, 'pitch': midi.B_4},
    {'time': 3200, 'duration': 200, 'pitch': midi.C_5},
    {'time': 3200, 'duration': 200, 'pitch': midi.E_5},
    {'time': 3400, 'duration': 200, 'pitch': midi.B_4},
    {'time': 3400, 'duration': 200, 'pitch': midi.C_5},
    {'time': 3400, 'duration': 200, 'pitch': midi.E_5},
])
pattern.append([
    {'time': 3100, 'duration': 25, 'pitch': midi.B_5},
    {'time': 3125, 'duration': 25, 'pitch': midi.C_6},
    {'time': 3150, 'duration': 25, 'pitch': midi.E_6},
    {'time': 3175, 'duration': 825, 'pitch': midi.D_6},
])
play.write(pattern, 'never-meant-to-belong.mid')