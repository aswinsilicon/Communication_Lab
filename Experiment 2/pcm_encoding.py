#Part A: PCM Encoding (next task)
def pcm_encode(x, b):
    L = 2**b
    delta = 1/L
    k = np.floor(x/delta)
    k = np.clip(k, 0, L-1).astype(int)
    
    xcap = (k + 0.5)*delta
    Ps = np.mean(x**2)
    Pn = np.mean((x - xcap)**2)
    SQNRdB = 10*np.log10(Ps/Pn)
    
    
    bitstream="" #empty string to generate 0 or 1
    
    for v in k:
        bitstream+=np.binary_repr(v,width=b)  #representing the number in binary format
        
    b_tx = np.array(list(bitstream), dtype=np.uint8)  #numpy array of 0 and 1
    #separate each digit in the binary number and store as list contents
    
    return k, xcap, b_tx, SQNRdB

