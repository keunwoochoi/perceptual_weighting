import numpy as np
import loudness
import matplotlib
import matplotlib.pyplot as plt
import pdb

# setup 
S = np.load('data/spectrogram.npy')
sr = 44100
n_fft = 1024
bin_width = float(sr)/n_fft
freqs = [0.0] + [(i+1)*bin_width for i in xrange(0,n_fft/2)]
freqs = np.array(freqs)

# initiate a converter for given frequencies
converter = loudness.ISO226_Converter(freqs, isStrict=False)
# convert the spectrogram.
S_weighted = converter.convert_s2l(S)

# plot
bins = np.array(range(S.shape[1]))

try:
	import librosa
	plt.subplot(1,2,1)
	librosa.display.specshow(S, y_axis='log', cmap='coolwarm')
	plt.colorbar(format='%+2.0f dB')
	plt.title('Before')


	plt.subplot(1,2,2)
	librosa.display.specshow(S_weighted, y_axis='log', cmap='coolwarm')
	plt.colorbar(format='%+2.0f dB')
	plt.title('After perceptual weighting')

	plt.savefig('comparison_spectrogram_by_librosa.png')
	plt.close()


fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.pcolormesh(bins, freqs, S)
ax2.pcolormesh(bins, freqs, S_weighted)

ax1.set_yscale('symlog', linthreshy=0.1)
ax1.set_ylim([bin_width, sr/2])
ax1.set_title('Before')

ax2.set_yscale('symlog', linthreshy=0.1)
ax2.set_ylim([bin_width, sr/2])
ax2.set_title('After perceptual weighting')

plt.savefig('comparison_spectrogram_normal.png')
plt.close()





