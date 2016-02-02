# PsychoAcousticsToolbox
by Keunwoo Choi (keunwoo.choi@qmul.ac.uk)

# What does it do?
* loudness.py: You can get perceptually weighted time-frequency representation in a much more correct way than A-weighting.
* basic_weightings.py: You can add A-, B-, C-, and D-weighting to your TF-representation.

# Why do we need this?
* Because energy of tf-bin does not represent what we hear in terms of loudness.

You see the results in the included png files.

Please feel free to suggest me further upgrade!

# Usage
As in the example.py.
* preparation
```
# some constants
sr = 44100
n_fft = 1024
bin_width = float(sr)/n_fft
freqs = [0.0] + [(i+1)*bin_width for i in xrange(0,n_fft/2)] # important!
freqs = np.array(freqs)

S = np.load('data/spectrogram.npy')
```
* conversion
```
import loudness
converter = loudness.ISO226_Converter(freqs, isStrict=False) # initiate a converter object for the frequency bands
S_weighted = converter.convert_s2l(S) # convert the spectrogram.
```

# plan

- masking curve
- gammatone filterbank

