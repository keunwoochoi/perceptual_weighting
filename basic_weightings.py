# Keunwoo Choi
# All equations come from Wikipedia, https://en.wikipedia.org/wiki/A-weighting
import sys
import numpy as np
import pdb

EPS = np.float(sys.float_info.epsilon)

class Basic_Weighting_Converter:
	"""This class introduces a basic weighting converters A-, B-, C-, and D-weighting.
	Please see main body of this file to see an example.
	"""
	def __init__(self, freqs):

		self.freqs = np.array(freqs)
		self.A = None
		self.B = None
		self.C = None
		self.D = None
		
		self.init_A()
		self.init_B()
		self.init_C()
		self.init_D()

	def init_A(self):
		response = (12200**2 * self.freqs**4) /  ( (self.freqs**2+20.6**2) * (self.freqs**2+12200**2) * np.sqrt((self.freqs**2+107.7**2)*(self.freqs**2+737.9**2)) ) 
		self.A = 2.0 + 20*np.log10(response+EPS)

	def init_B(self):
		response = (12200**2 * self.freqs**3) / ((self.freqs**2+20.6**2) * (self.freqs**2+12200**2) * np.sqrt(self.freqs**2+158.5**2))
		self.B = 0.17 + 20*np.log10(response+EPS)

	def init_C(self):
		response = (12200**2 * self.freqs**2) / ((self.freqs**2 + 20.6**2) * (self.freqs**2 + 12200**2))
		self.C = 0.06 + 21*np.log10(response+EPS)

	def init_D(self):
		h_f = ((1037918.48-self.freqs**2)**2 + 1080768.16*self.freqs**2)/((9837328-self.freqs**2)**2 + 11723776*self.freqs**2)
		response = self.freqs / (6.8966888496476*10**(-5)) * np.sqrt( h_f/ ((self.freqs**2+79919.29) * (self.freqs**2+1345600)) )
		self.D = 20*np.log10(response+EPS)

if __name__=="__main__":
	sr = 44100
	n_fft = 1024
	bin_width = float(sr)/n_fft
	freqs = [0.0] + [(i+1)*bin_width for i in xrange(0,n_fft/2)]
	cvt = Basic_Weighting_Converter(freqs)

	# then add cvt.A - cvt.D to the log_amplitude(STFT), which is equivalent to 10*log(absolute(S)**2).
	import matplotlib.pyplot as plt
	plt.semilogx(freqs, cvt.A, color='#297885')
	plt.semilogx(freqs, cvt.B, color='#F68012')
	plt.semilogx(freqs, cvt.C, color='#31A12C')
	plt.semilogx(freqs, cvt.D, color='#D62727')
	plt.xlabel('Frequency (Hz)')
	plt.ylabel('Level (dB)')
	plt.grid()
	plt.xlim([0, sr/2])
	plt.ylim([-40, 20])
	plt.legend(['A-weighting', 'B-weighting', 'C-weighting', 'D-weighting'], loc='lower right')
	plt.show()
