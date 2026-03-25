#Part C: PCM Decoder 
def pcm_decode(b_rx, b, M, N):
    L = 2**b
    delta = 1 / L
    total_bits = (len(b_rx) // b) * b
    b_rx = b_rx[:total_bits] #drops extra bits caused by channel truncation
    bits = b_rx.reshape(-1, b) #each row is one symbol

    #converting binary number into a digit in decimal rep
    k_hat = []
    for row in bits:
        binary_string = ""
        for bit in row:
            binary_string += str(bit)
        index = int(binary_string, 2)
        k_hat.append(index)

    #mid-rise reconstruction    
    k_hat = np.array(k_hat)
    k_hat = np.clip(k_hat, 0, L-1)
    xcap = (k_hat + 0.5) * delta
    xcap_img = xcap.reshape(M, N)
    
    return xcap_img

def compute(x, x_hat):

    #mean squared error
    mse = np.mean((x - x_hat)**2)
    Ps = np.mean(x**2)
    snr_db = 10*np.log10(Ps/mse)
    maximum = 1 #max pixel value = 1
    psnr_db = 10*np.log10(maximum**2/mse)
    
    return mse, snr_db, psnr_db
