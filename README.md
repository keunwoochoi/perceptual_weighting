# PsychoAcousticsToolbox
by Keunwoo Choi (keunwoo.choi@qmul.ac.uk)

pat, PsychoAcousticsToolbox for python, is my new project for a convenient computation of loudness given time-frequency representation. Basically, the goal is to bridge between psychoacoustics (based on sound) and signal processing (based on signal/data).

Further functionality would be computing masking curve and other (pseudo) perceptual weighting such as A-weighting. 

At some moment I'll wrap it into a form of python package to make it easier to install and manage.

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
then,
```
import loudness
converter = loudness.ISO226_Converter(freqs, isStrict=False) # initiate a converter object for the frequency bands
S_weighted = converter.convert_s2l(S) # convert the spectrogram.
```


