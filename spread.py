import math
from numpy.fft import fft
import numpy as np
import matplotlib.pyplot as plt

RF_DATA_FILE = 'iwave.dat'
IDEAL_FILE = 'cwave.dat'
TIME = 60
SAMPLE_RATE = 12000
samples = TIME * SAMPLE_RATE
g_fft_size = samples * 2
index_per_freq = g_fft_size / SAMPLE_RATE
freq_per_index = 1 / index_per_freq
FOCUS_REGION = 4 # we really only care about frequencies +/- 4 Hz
POWER_REGION = 1 # we look for the maximum power to normalize in +/- 1 Hz
NOISE_REGION = 2 # we look for the noise 2 Hz in from outsides of the FOCUS region

# theoretically our RF data is between -32768 and 32768
# this scale factor makes it a float between -1 and 1
rf_scale_factor = 1.0 / 32768

# Read RF data
rf_data = np.empty(samples, dtype=float)
with open(RF_DATA_FILE, 'r') as data_file:
    i = 0
    for line in data_file.readlines():
        split_line = line.split()
        rf_data[i] = int(split_line[1])
        i += 1
        if i > samples:
            break
print(f"Read {rf_data.size} samples of RF data from {RF_DATA_FILE}")

# Read ideal waveform
ideal = np.empty(samples, dtype=complex)
with open(IDEAL_FILE, 'r') as data_file:
    i = 0
    for line in data_file.readlines():
        split_line = line.split()
        ideal[i] = complex(float(split_line[1]), float(split_line[2]))
        i += 1
        if i > samples:
            break
print(f"Read {ideal.size} samples of the ideal waveform from {IDEAL_FILE}")

g = rf_scale_factor * rf_data * np.conj(ideal)
g_fft = fft(g, g_fft_size)

# grab the focus region, don't forget negative values wrap around
# we center the focus region in our array and from complex to just magnitude
di = int(index_per_freq * FOCUS_REGION)
g_fft_focus = np.empty(di * 2, dtype=float)
j = 0
for i in range(-1 * di, di):
    if i < 0:
        i += g_fft_size
    g_fft_focus[j] = g_fft[i].real**2 + g_fft[i].imag**2
    j += 1

# find the maximum power in the +/- POWER_REGION Hz region
# don't forget that the frequency has now shifted to start at -FOCUS_REGION Hz
power_start = int(index_per_freq * (FOCUS_REGION - POWER_REGION))
power_end = int(power_start + index_per_freq * (POWER_REGION * 2))
smax = g_fft_focus[power_start:power_end].max()
print(f"smax: {smax}")

# using smax, scale the FFT to be between 0 and 1
g_fft_focus /= smax

# calculate the noise average
left_noise = np.average(g_fft_focus[0:int(index_per_freq * NOISE_REGION)])
right_noise = np.average(g_fft_focus[:-int(index_per_freq*NOISE_REGION)])
noise = min(left_noise, right_noise)

# subtract out the noise
g_fft_focus -= noise

# calculate the power around POWER_REGION
total_power = np.sum(g_fft_focus[power_start:power_end])

# find the indexes around the power region where we hit 25% and 75% of the power
current_power = 0.0
p25_index = None
p75_index = None
for i in range(power_start, power_end):
    current_power += g_fft_focus[i]
    power_percent = current_power / total_power
    if (power_percent >= 0.25) and p25_index == None:
        p25_index = i
    if power_percent >= 0.75:
        p75_index = i
        break
    prev_power = current_power

xdiff = math.sqrt(1 + (p75_index - p25_index)**2)
w50 = xdiff * freq_per_index
print(f"Doppler Spread (w50): {w50}")
