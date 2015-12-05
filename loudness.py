# 04 Dec 2015, Keunwoo Choi (keunwoo.choi@qmul.ac.uk)
# This modules is designed to compute loudness of given time-frequency representation (which would be a numpy array)
# The standard ISO 226 computes SPL <-> Loudness, both of which are based on sound, the derivative of pressure, rather than signal.
# Therefore we need to assume how loud the signal would be played. In other word, the gain of DAC.

import numpy as np
from scipy.interpolate import interp1d
import iso226
import pdb
from constants import *

iso226const = iso226.ISO226Const()

class ISO226_Converter:
	def __init__(self, freqs, isStrict=True):
		"""It requires for which frequencies you need to convert.
		For example, if you want to use it with 512-point STFT at 44100 Hz,
		freqs should be range(0, 44100/2, 44100/(512/2))+[44100/2]

		if isStrict==True, mode follows the limitation of ISO226 strictly, i.e. 20<f<12000 and 0<SPL<90.
		else, ranges extends to 0<f<24k and -20<SPL<110
		"""
		#properties
		self.freqs = freqs
		self.isStrict = isStrict

		self.interp1d_s2l_functions = []
		# more init functions.
		self.get_interp1d_s2l_functions() # to fill functions
		
	def get_interp1d_s2l_functions(self):
		f_s2l_2d = iso226.get_interp2d_spl_to_loudness(isStrict=self.isStrict) # 2d interpolator.
		if self.isStrict:
			spl_array = np.array(range(STRICT_MIN_SPL, STRICT_MAX_SPL+1, 5)) # [0,5,...85,90]
		else:
			spl_array = np.array(range(APPROX_MIN_SPL, APPROX_MAX_SPL+1, 5)) # [0,5,...85,90]

		for i_freq, freq in enumerate(self.freqs):
			loudness_data = f_s2l_2d(spl_array, freq) # get loudness data given SINGLE frequency and SPL values
			self.interp1d_s2l_functions.append(interp1d(x=spl_array, y=loudness_data, kind='cubic'))

	def convert_s2l(self, spl_arrays):
		"""
		spl_arrays : N-by-M np array, where N == len(self.freqs) == number of frequency band.
											M == number of frame
		return: weighted spectrogram
		"""
		ret = np.zeros(spl_arrays.shape)
		for i_freq, spl_vals in enumerate(spl_arrays): # enumerate for each frequency band
			print "For spl values of", spl_vals, "at freq ind", i_freq, self.freqs[i_freq], 'hz.'
			ret[i_freq, :]=self.interp1d_s2l_functions[i_freq](spl_vals)
		return ret


#def perceptual_weighting(S, frequencies, type=None, ref_power=np.max):
	"""
	The interface mimics that of librosa.core.perceptual_weighting.

	S: 
		N-by-1 or N-by-M numpy array containing tf-bins. e.g. STFT. 
	frequencies: 
		N-by-1 numpy array, center frequency of S.
	type: 
		string, type of perceptual weighting. 
		'iso226', 'a-weighting'
	ref_power: function or scalar.
		<If scalar, log(abs(S)) is compared to log(ref_power)
		If a function, log(abs(S)) is compared to log(ref_power(abs(S))).
		This is primarily useful for comparing to the maximum value of S.> -- as written in librosa.
		However, it could mean more if 'iso226' is used. Since the SPL of iso226 is up to 90dB, this function will set the gain so that
		ref_power value is equal to 90 dB SPL.
	"""

if __name__=='__main__':
	S = np.array([[30, 40], [30,55], [40, 55]])
	freqs = np.array([500, 1000, 3000])
	
	cvt = ISO226_Converter(freqs)
	print cvt.convert_s2l(S)

	cvt = ISO226_Converter(freqs)
	print cvt.convert_s2l(S)

	S = np.array([[30, 40], [-5, 95], [40, 55]])
	freqs = np.array([0, 1000, 11000])
	cvt = ISO226_Converter(freqs, isStrict=False)
	print cvt.convert_s2l(S)
