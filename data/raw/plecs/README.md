# Raw PLECS Frequency-Response Exports

Each CSV contains one header row followed by 41 numeric samples:

```text
column 1: frequency in Hz
column 2: magnitude in dB
column 3: phase in degrees
```

The repeated PLECS measurement heading in columns two and three is part of the
original export format. The Python reader therefore uses column position rather
than heading text.

