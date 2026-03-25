#Task 2 : BPSK Modulation and Constellation

#now from b_tx we map bits to BPSK Symbols
#generate BPSK Modulated signal
#plot constellation graph

Eb = 1
bipolar = 1 - 2*b_tx.astype(int)  # 0 maps to +1, 1 maps to -1
s = bipolar * np.sqrt(Eb)  #symbols of BPSK Modulated signals

plt.figure()
plt.scatter(s,np.zeros_like(s),s=10)
plt.xlabel("In-Phase")
plt.ylabel("Quadrature-Phase")
plt.title("BPSK Constellation with no Noise Addition")
plt.grid()
plt.show()
