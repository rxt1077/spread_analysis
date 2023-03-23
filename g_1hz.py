import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,4.5))

df = 8.33333377E-03 # frequency per point of FFT
nfft = 1440000 # number of points in the FFT
smax = 677334.875 # pre-calculated max around 1Hz for this data
ia = int(4/df) # 4 Hz worth of points

g_fft = []
with open('g_fft.dat', 'r') as data_file:
    for line in data_file.readlines():
        split_line = line.split()

        # this signal is complex, get the magnitude and normalize by smax
        g_fft.append((float(split_line[1])**2 + float(split_line[2])**2)/smax)

x_array = []
y_array = []
for i in range(-ia, ia):
    x_array.append(i*df)
    # negative frequences are wrapped around to the other end of the FFT
    print(i+nfft)
    if i < 0:
        y = g_fft[i+nfft]
    else:
        y = g_fft[i]
    y_array.append(y)

plt.plot(x_array, y_array)

#plt.xlim([start, end])
plt.title("G FFT +/- 4Hz")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Normalized Magnitude")
plt.savefig('g_fft_4Hz.png')
plt.close(fig)
