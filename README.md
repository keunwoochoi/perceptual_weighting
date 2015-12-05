# PsychoAcousticsToolbox
by Keunwoo Choi (keunwoo.choi@qmul.ac.uk)

What does it do?
You can get perceptually weighted time-frequency representation in a much more correct way than A-weighting.
(At the moment, the toolbox is very small. This is it!)

Further functionality would be computing masking curve and other (pseudo) perceptual weighting such as A-weighting. 

At some moment I'll wrap it into a form of python package to make it easier to install and manage.... or I'll change the name to more humble one. 

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


