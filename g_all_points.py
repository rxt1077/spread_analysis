import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,4.5))

df = 8.33333377E-03

x_array = []
y_array = []
with open('g_fft.dat', 'r') as data_file:
    for line in data_file.readlines():
        split_line = line.split()

        x = int(split_line[0])

        # this signal is complex, get the magnitude
        y = float(split_line[1])**2 + float(split_line[2])**2

        x_array.append(x)
        y_array.append(y)

plt.plot(x_array, y_array)

#plt.xlim([start, end])
plt.title("G FFT (All Points)")
plt.xlabel("Index")
plt.ylabel("Magnitude")
plt.savefig('g_fft_all.png')
plt.close(fig)
