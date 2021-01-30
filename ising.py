import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

'''
This program creates an animation of electron spins in order to discover
a temperature Tc (Curie temperature). It then caclulates the average magnetic
moment of the whole system for a range of temperatures and plots magnetic
moment vs temperature.
'''

# Create grid of random values -1 and 1
a = [-1, 1]
x = np.random.choice(a, (50, 50))

# Temperature value
T = [0.01, 0.1, 1, 2, 3, 4, 5, 10, 100]


# Calculate energy of lattice
def H(x):
    one = np.roll(x, -1, axis=0)
    two = np.roll(x, 1, axis=0)
    sum1 = one + two
    sum2 = np.sum(sum1)
    return -1*sum2


# Change energy configuration
def flip_H(x, t):
    n = np.random.randint(0, 50)
    m = np.random.randint(0, 50)
    right = x[n, (m+1) % 50]  # right side
    left = x[n, (m-1) % 50]  # left side
    top = x[(n+1) % 50, m]  # top
    b = x[(n-1) % 50, m]  # bottom
    mid = x[n, m]  # middle point
    e = mid*right + mid*left + mid*top + mid*b  # energy
    x[n, m] = -1*x[n, m]
    flip = -1*mid  # create new configuration
    enew = flip*right + flip*left + flip*top + flip*b
    if e < enew:
        prob = np.exp(-1*(enew-e)/t)
        r = np.random.random()
        if r > prob:
            x[n, m] = -1*x[n, m]
    return x


# Calculate magnetic moment of system
fin = []
for n in range(5):
    moment = []
    for i in T:
        for r in range(600000):
            m = flip_H(x, i)
            mom = np.sum(m)
        moment.append(mom)
    fin.append(moment)
list = np.abs(np.array(fin))
end = list.max(axis=0)


# Animations
# Movie 1: temp = 0.1
fig = plt.figure()
ims = []
for i in range(600000):
    m = np.copy(x)
    k = flip_H(m, 0.1)
    if i % 1000 == 0:
        ims.append((plt.pcolormesh(k), ))
imani = animation.ArtistAnimation(fig, ims, interval=75,  repeat=False)
imani.save('temp_0.1.mp4')
plt.clf()  # clear before next movie

# Movie 2: temp = 2.5
fig = plt.figure()
ims = []
for i in range(600000):
    m2 = np.copy(x)
    k = flip_H(m2, 2.5)
    if i % 1000 == 0:
        ims.append((plt.pcolormesh(k), ))
imani = animation.ArtistAnimation(fig, ims, interval=75,  repeat=False)
imani.save('temp_2.5.mp4')
plt.clf()  # clear before next movie


# Movie 3: temp = 100
fig = plt.figure()
ims = []
for i in range(600000):
    m3 = np.copy(x)
    k = flip_H(m3, 100)
    if i % 1000 == 0:
        ims.append((plt.pcolormesh(k), ))
imani = animation.ArtistAnimation(fig, ims, interval=75,  repeat=False)
imani.save('temp_100.mp4')
plt.clf()

# Plot max M values vs T, put T on log scale
plt.plot(T, end)
plt.xscale('log')
plt.title('M vs T')
plt.xlabel('Temperature (degrees)')
plt.ylabel('Magnetic moment (M)')
plt.savefig('Tcurie.pdf')
