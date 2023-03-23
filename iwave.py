import matplotlib.pyplot as plt

fig = plt.figure(figsize=(9,4.5))

start = 1.31
end = 1.40

x_array = []
y_array = []
with open('iwave.dat', 'r') as data_file:
    for line in data_file.readlines():
        split_line = line.split()

        # convert from samples to seconds (FST4 uses 12000 samples/sec)
        x = int(split_line[0])/12000

        # this signal is complex, just look at the real part
        y = int(split_line[1])

        # only go from start to end
        if x >= start:
            #print(x, y)
            x_array.append(x)
            y_array.append(y)
        if x >= end:
            break

plt.plot(x_array, y_array)

plt.xlim([start, end])
plt.title("iwave")
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.savefig('iwave.png')
plt.close(fig)
