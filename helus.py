# -*- coding: utf-8 -*-
"""
Created on Tue May 19 18:01:54 2026

@author: aswin
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.random.randn(20000)
print(x)

def pcm_encode(x,b):
    L = 2**b
    delta = 1/L
    
    k = np.floor(x/delta)
    k = np.clip(k,0,L-1).astype(int)
    
    xcap = (k+0.5)**delta
    
    Ps = np.mean(x**2)
    Pn = np.mean((x-xcap)**2)
    
    SQNR = Ps/Pn
    SQNRdB = 10*np.log10(SQNR)
    
    bitstream =""
    for v in k:
        bitstream+=np.binary_repr(v,width =b)
    
    b_tx = np.array(list(bitstream),dtype = np.uint8)
    
    return k,xcap,b_tx,SQNRdB, bitstream

b = 8
b_tx = pcm_encode(x,b)[2]
bitstream = pcm_encode(x,b) [4]

Eb=1
bipolar = 1 - 2*b_tx.astype(int)
s = bipolar * np.sqrt(Eb)

plt.figure()
plt.scatter(s,np.zeros_like(s),s=10)
plt.grid()
plt.show()
'''
bit_pairs = b_tx.reshape(-1,2)
s=[]
for b1,b2 in bit_pairs:
    if b1==0 and b2==0:
        s.append(1+1j)
    elif b1==0 and b2==1:
        s.append(-1+1j)
    elif b1==1 and b2==1:
        s.append(-1-1j)
    elif b1==1 and b2==0:
        s.append(1-1j)
        
s= np.array(s)

plt.figure()
plt.scatter(np.real(s[:1000]),np.imag(s[:1000]),s=10)
plt.grid()
plt.show()
'''

Eb = 1
EbN0 = np.arange(0,11,2)
for eachvalue in EbN0:
    
    EbN0_lin = 10**(eachvalue/10)
    N0 = Eb/EbN0_lin
    
    sigma = N0/2
    
    nI = np.random.normal(0,np.sqrt(sigma),len(s))
    nQ = np.random.normal(0,np.sqrt(sigma),len(s))
    noise = nI + 1j*nQ
    
    y= s+noise
    plt.figure()
    plt.scatter(np.real(y[:5000]),np.imag(y[:5000]),s=10)
    plt.grid()
    plt.show()

