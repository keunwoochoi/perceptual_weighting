# PsychoAcousticsToolbox
by Keunwoo Choi (keunwoo.choi@qmul.ac.uk)

pat, PsychoAcousticsToolbox for python, is my new project for a convenient computation of loudness given time-frequency representation. Basically, the goal is to bridge between psychoacoustics (based on sound) and signal processing (based on signal/data).

Further functionality would be computing masking curve and other (pseudo) perceptual weighting such as A-weighting. 

At some moment I'll wrap it into a form of python package to make it easier to install and manage.

Please feel free to suggest me further upgrade!

# Usage
As in the example.py,
` import loudness
converter = loudness.ISO226_Converter(freqs, isStrict=False)
S_weighted = converter.convert_s2l(S)


