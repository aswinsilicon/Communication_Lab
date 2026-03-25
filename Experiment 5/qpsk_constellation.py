#Task 2 : QPSK Modulation and Constellation

#now from b_tx we map bits to QPSK Symbols
#generate QPSK Modulated signal
#plot constellation graph

Eb = 1
bit_reshaped = b_tx.reshape(-1,2)

#defining the mapping two bits to the corresponding symbols
mapping = {
    (0,0) : (1+1j),
    (0,1) : (-1+1j),
    (1,1) : (-1-1j),
    (1,0) : (1-1j)
}

s = np.array([mapping[tuple(b)] for b in bit_reshaped]) * np.sqrt(Eb)

plt.figure()
plt.scatter(np.real(s),np.imag(s),s=10)
plt.xlabel("In-Phase")
plt.ylabel("Quadrature-Phase")
plt.title("QPSK Constellation with no Noise Addition")
plt.axvline(0)
plt.axhline(0)
plt.grid()
plt.show()
