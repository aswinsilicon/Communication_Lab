import numpy as np 
import matplotlib.pyplot as plt


x = np.random.randn(0, 2, 50000)


#PCM Encoding

def pcm_encode(x,b):
    L = 2**b
    delta = 1/L
    
    k = np.floor(x/delta)
    k = np.clip(k,0,L-1).astype(int)
    
    xcap = (k+0.5)*delta
    
    Ps = np.mean(x**2)
    Pn = np.mean((x-xcap)**2)
    
    SQNR = Ps/Pn
    SQNRdB = 10*np.log10(SQNR)
    
    bitstream = ""
    for v in k:
        bitstream+=np.binary_repr(v,width=b)
        
    b_tx = np.array(list(bitstream),dtype = np.uint8)
    
    return k,xcap,b_tx,SQNRdB    

b=8
b_tx = pcm_encode(x, b)[2]

def channel_bsc(b_tx,p,rng = None):
    
    if rng is None:
        rng=np.random.default_rng()
        
    z = (rng.random(b_tx.shape)<p).astype(np.uint8)
    b_rx = np.bitwise_xor(b_tx.astype(np.uint8),z)
    ber_measure = np.mean(b_rx!=b_tx)
    return b_rx,ber_measure

def bpsk_modulate(b):
    return 1-2*b.astype(np.uint8)

def bpsk_demodulate(y):
    return (y < 0).astype(np.uint8)

def channel_awgn(b_tx,ebn0dB):
    s = bpsk_modulate(b_tx)
    
    ebn0 = 10**(ebn0dB)/10
    N0 = 1/ebn0
    
    sigma = np.sqrt(N0/2)
    n = np.random.normal(0,sigma,size = s.shape)
    y = s + n
    
    b_rx = bpsk_demodulate(y)
    ber = np.mean(b_rx!=b_tx)
    
    return b_rx, ber

def pcm_decode(b_rx,b):
    L = 2**b
    delta = 1/L
    
    total_bits = (len(b_rx)//b)*b
    b_rx = b_rx[:total_bits]
    bits = b_rx.reshape(-1,b)
    
    k_hat = []
    for row in bits:
        binary_string =""
        for bit in row:
            binary_string +=str(bit)
        index = int(binary_string,2)
        k_hat.append(index)

    k_hat = np.array(k_hat)
    k_hat = np.clip(k_hat,0,L-1)
    
    xcap = (k_hat+0.5)**delta
    
    return xcap


# BPSK modulation constellation diagram
Eb = 1

bipolar = 1 - 2*b_tx.astype(int)   # 0 -> +1 , 1 -> -1
s = bipolar * np.sqrt(Eb)

plt.figure()
plt.scatter(s, np.zeros_like(s), s=10)
plt.xlabel("In-Phase")
plt.ylabel("Quadrature")
plt.title("BPSK Constellation without Noise")
plt.grid()

# AWGN channel simulation
list_y = []

EbN0_dB = np.arange(0, 11, 2)   # 0,2,4,6,8,10

for i in range(len(EbN0_dB)):

    EbN0_lin = 10**(EbN0_dB[i]/10)

    N0 = Eb / EbN0_lin

    noise_variance = N0 / 2

    nI = np.sqrt(noise_variance) * np.random.randn(len(s))
    nQ = np.sqrt(noise_variance) * np.random.randn(len(s))

    n = nI + 1j*nQ

    y = s + n

    list_y.append(y)

# Plot received constellation
for eachvalue in range(len(EbN0_dB)):

    plt.figure()

    plt.scatter(
        np.real(list_y[eachvalue][:5000]),
        np.imag(list_y[eachvalue][:5000]),
        s=5
    )

    plt.xlabel("In-Phase")
    plt.ylabel("Quadrature")
    plt.title(f"BPSK with AWGN at {EbN0_dB[eachvalue]} dB")
    plt.grid()

    plt.show()

# ML Detection
list_b_rx = []

for i in range(len(EbN0_dB)):

    y = list_y[i]

    b_rx = (np.real(y) < 0).astype(int)

    list_b_rx.append(b_rx)

# BER Calculation
sim_BER = []

for i in range(len(EbN0_dB)):

    bit_error = np.sum(b_tx != list_b_rx[i])

    BER = bit_error / len(b_tx)

    sim_BER.append(BER)

print("BER values:")
print(sim_BER)

# PCM Reconstruction
reconstructed_stream = []

for i in range(len(EbN0_dB)):

    decoded_signal = pcm_decode(list_b_rx[i], b)

    reconstructed_stream.append(decoded_signal)

# Plot reconstructed values
for i in range(len(EbN0_dB)):

    plt.figure()

    plt.scatter(
        reconstructed_stream[i][:5000],
        np.zeros_like(reconstructed_stream[i][:5000]),
        s=5
    )

    plt.title(f"Reconstructed Signal at {EbN0_dB[i]} dB")

    plt.grid()

    plt.show()

from scipy.special import erfc
    
theoritical_BER = 0.5 * erfc(np.sqrt(EbN0_lin))

#semilog plot
plt.figure()
plt.semilogy(EbN0_dB,sim_BER,'o',label = 'Simulated BER')
plt.semilogy(EbN0_dB,theoritical_BER,'-',label = 'Theoritical BER')
plt.xlabel("Eb/N0 (dB)")
plt.ylabel("BER")
plt.title("BER Performance of BPSK over AWGN")
plt.legend()
plt.grid()
plt.show()
    
    
    
    
    
    
