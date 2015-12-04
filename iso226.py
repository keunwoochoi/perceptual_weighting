# 04 Dec 2015, Keunwoo Choi (keunwoo.choi@qmul.ac.uk)
# It is an extended code of iso226.py written by Juan Carrano (https://github.com/jcarrano/rtfi/blob/master/iso226.py)
# Some part of this code is copied-and-pasted from Juan's code.

import numpy as np

from scipy.interpolate import interp1d

class ISO226Const:
	"""A class to store constants for iso226 - loudness_to_spl"""
	def __init__(self):
		self.f = np.array([20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500])
		self.af = np.array([0.532, 0.506, 0.480, 0.455, 0.432, 0.409, 0.387, 0.367, 0.349, 0.330, 0.315, 0.301, 0.288, 0.276, 0.267, 0.259, 0.253, 0.250, 0.246, 0.244, 0.243, 0.243, 0.243, 0.242, 0.242, 0.245, 0.254, 0.271, 0.301])
		self.Lu = np.array([-31.6, -27.2, -23.0, -19.1, -15.9, -13.0, -10.3, -8.1, -6.2, -4.5, -3.1, -2.0, -1.1, -0.4, 0.0, 0.3, 0.5, 0.0, -2.7, -4.1, -1.0, 1.7, 2.5, 1.2, -2.1, -7.1, -11.2, -10.7, -3.1])
		self.Tf = np.array([78.5, 68.7, 59.5, 51.1, 44.0, 37.5, 31.5, 26.5, 22.1, 17.9, 14.4, 11.4, 8.6, 6.2, 4.4, 3.0, 2.2, 2.4, 3.5, 1.7, -1.3, -4.2, -6.0, -5.4, -1.5, 6.0, 12.6, 13.9, 12.3])

iso226const = ISO226Const()

class Spectrogram_Loudness_Converter:
	"""A converter class of """

def spl_to_loudness(spl, freqs=None):
	if freqs==None:
		raise ValueError('Invalid frequency input')
	if spl < 0 or spl > 90:
		raise ValueError('SPL value out of bounds!')
	Lp = spl
	Af = 10**((Lp - 94 + iso226const.Lu)*(iso226const.af/10))
	Ln = 40*np.log10((Af - (0.4*10**(((iso226const.Tf+iso226const.Lu)/10)-9 ))**iso226const.af )/(4.47E-3) + 1.15)
	
	return interp1d(iso226const.f, Ln, 'cubic')(freqs)

def loudness_to_spl(phon, freqs=None):
	""" It gets loudness in a unit of phon according to ISO226 and returns the corresponding SPL value(s)
	phon: int or float, or list of any [phon]
	freqs: int or float, or list of any [Hz] 

	return: numpy array size of freqs.shape in SPL
	"""
	if freqs==None:
		raise ValueError('Invalid frequency input')
	if phon < 0 or phon > 90:
		raise ValueError('Phon value out of bounds!')
	else:
	# Setup user-defined values for equation
		Ln = phon
	# Deriving sound pressure level from loudness level (iso226 sect 4.1)
		Af=4.47E-3 * (10**(0.025*Ln) - 1.15) + (0.4*10**(((iso226const.Tf+iso226const.Lu)/10)-9 ))**iso226const.af
		Lp=((10/iso226const.af)*np.log10(Af)) - iso226const.Lu + 94
	#Return 
	return interp1d(iso226const.f, Lp, 'cubic')(freqs)


