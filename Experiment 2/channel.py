#Part B : Channels

#Channel A: Binary Symmetric Channel
            #(flips each bit independently with probability p: BER parameter)
            #rng: random number
def channel_bsc(b_tx, p, rng=None):
    if rng is None:
        rng = np.random.default_rng()
        
    z = (rng.random(b_tx.shape) < p).astype(np.uint8) #error mask
    b_rx = np.bitwise_xor(b_tx.astype(np.uint8), z)

    #measured BER
    ber_meas = np.mean(b_rx != b_tx)
    return b_rx, ber_meas

#Channel B: BPSK + AWGN : closer to physical link

def bpsk_modulate(b):
    b = b.astype(np.uint8)
    return 1 - 2*b # 0->1, 1->-1

def bpsk_demodulate(y):
    return (y > 0).astype(np.uint8)

def channel_awgn_bpsk(b_tx, ebn0_db):
    #signal to transmit symbols +1/-1
    s = bpsk_modulate(b_tx)
    ebn0 = 10**(ebn0_db/10) #log to linear
    Eb = 1
    N0 = Eb/ebn0    #noise spectral density
    sigma = np.sqrt(N0/2)
    
    #generating AWGN n
    n = np.random.normal(0,sigma,size=s.shape)
    y = s + n #received signal
    b_rx = bpsk_demodulate(y)
    #BER estimation
    ber = np.mean(b_rx != b_tx)
    return b_rx, ber
