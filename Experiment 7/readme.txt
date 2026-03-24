Problem: Band-limited channel → causes ISI (Inter-Symbol Interference)
Solution: Use pulse shaping (SRRC) + matched filtering

You send symbols like this:
+1 -1 +1 +1 ...
Without shaping → signals overlap randomly → errors
With SRRC → pulses are designed so that:

At sampling time, only one symbol is active

ISI occurs when pulses corresponding to different symbols overlap in time. 
In a band-limited channel, high-frequency components are removed,
which distorts the pulse shape. This causes spreading of pulses in time, 
leading to overlap at sampling instants and hence interference.

SRRC pulse shaping is used to limit bandwidth and reduce ISI.
It ensures that at the sampling instant, the contribution from all other symbols is zero, so only the desired symbol is detected.


