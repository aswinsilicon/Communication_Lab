# -*- coding: utf-8 -*-
"""
Created on Wed May 20 07:51:14 2026

@author: aswin
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.random.randn(20000)

def pcm_encode(x,b):
    L = 2**b
    delta= 1/L
    
    k = np.floor(x/delta)
    k= np.clip(k,0,L-1).astype(int)
    
    xcap = (k+0.5)**delta
    
    Ps = np.mean(x**2)
    Pn = np.mean((x-xcap)**2)
    SQNR =Ps/Pn
    SQNRdB = 10 * np.log10(SQNR)
    
    bitstream = ""
    for v in k:
        bitstream+=np.binary_repr(v,width=b)
    b_tx = np.array(list(bitstream),dtype = np.uint8)
    
    return xcap,k,b_tx,SQNRdB,bitstream


b=8 
b_tx = pcm_encode(x,b)[2]


Eb = 1
bipolar = 1-2*b_tx.astype(int)
s = bipolar * np.sqrt(Eb)
'''
plt.figure()
plt.scatter(s,np.zeros_like(s),s=10)
plt.show()
'''
s=[]
bit_pairs = b_tx.reshape(-1,2)
for b1,b2 in bit_pairs:
    if b1==0 and b2==0:
        s.append(1+1j)
    elif b1==0 and b2==1:
        s.append(-1+1j)
    elif b1==1 and b2==1:
        s.append(-1-1j)
    elif b1==1 and b2==0:
        s.append(1-1j)
        
s = np.array(s)
plt.figure()
plt.scatter(np.real(s[:5000]),np.imag(s[:5000]),s=10)
plt.show()

BER_sim=[]

EbN0dB = np.arange(0,11,2)
for eachvalue in EbN0dB:
    EbN0_lin = 10 **(eachvalue/10)
    N0 = Eb/EbN0_lin
    
    sigma = N0/2
    
    nI= np.random.normal(0,np.sqrt(sigma),len(s))
    nQ= np.random.normal(0,np.sqrt(sigma),len(s))
    noise = nI +1j*nQ
    
    y = s+noise
    
    plt.figure()
    plt.scatter(np.real(y[:5000]),np.imag(y[:5000]),s=10)
    plt.grid()
    plt.show()
    
    bI = np.where(np.real(y)>0,0,1)
    bQ = np.where(np.imag(y)>0,0,1)
    
    b_rx =[]
    
    for bi,bq in zip(bI,bQ):
        if bi==0 and bq==0:
            b_rx.extend([0,0])
        elif bi==0 and bq==1:
            b_rx.extend([1,0])
        elif bi==1 and bq==1:
            b_rx.extend([1,1])
        elif bi==1 and bq==0:
            b_rx.extend([0,1])
            
    b_rx = np.array(b_rx)
    
    bit_error = np.sum(b_tx != b_rx[:len(b_tx)])
    BER = bit_error/len(b_tx)

    BER_sim.append(BER)
    
BER_theory = []

from scipy.special import erfc

for eachvalue in EbN0dB:
    EbN0_lin = 10 **(eachvalue/10)
    ber_theory = 0.5 * erfc(EbN0_lin)
    BER_theory.append(ber_theory)
    
    
    
plt.semilogy(EbN0dB, BER_theory,'o-')
plt.semilogy(EbN0dB, BER_sim,'--')
    















