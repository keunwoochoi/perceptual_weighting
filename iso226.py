# 04 Dec 2015, Keunwoo Choi (keunwoo.choi@qmul.ac.uk)
# It is an extended code of iso226.py written by Juan Carrano (https://github.com/jcarrano/rtfi/blob/master/iso226.py)
# Some part of this code is copied-and-pasted from Juan's code.

import numpy as np
from scipy.interpolate import interp1d, interp2d
import pdb
from constants import *

class ISO226Const:
	"""A class to store constants for iso226 - loudness_to_spl"""
	def __init__(self):
		self.f = np.array([20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500])
		self.af = np.array([0.532, 0.506, 0.480, 0.455, 0.432, 0.409, 0.387, 0.367, 0.349, 0.330, 0.315, 0.301, 0.288, 0.276, 0.267, 0.259, 0.253, 0.250, 0.246, 0.244, 0.243, 0.243, 0.243, 0.242, 0.242, 0.245, 0.254, 0.271, 0.301])
		self.Lu = np.array([-31.6, -27.2, -23.0, -19.1, -15.9, -13.0, -10.3, -8.1, -6.2, -4.5, -3.1, -2.0, -1.1, -0.4, 0.0, 0.3, 0.5, 0.0, -2.7, -4.1, -1.0, 1.7, 2.5, 1.2, -2.1, -7.1, -11.2, -10.7, -3.1])
		self.Tf = np.array([78.5, 68.7, 59.5, 51.1, 44.0, 37.5, 31.5, 26.5, 22.1, 17.9, 14.4, 11.4, 8.6, 6.2, 4.4, 3.0, 2.2, 2.4, 3.5, 1.7, -1.3, -4.2, -6.0, -5.4, -1.5, 6.0, 12.6, 13.9, 12.3])


class ISO226Const_Extended:
	"""It is a set of constants for extending ISO to be more robust.
	By adding heuristic values, we can get the result at f=0 or f>12500.
	"""
	def __init__(self):
		iso226const = ISO226Const()
		self.f = np.hstack((0, iso226const.f, 16000, 24000))
		self.af = np.hstack((iso226const.af[0], iso226const.af, iso226const.af[-2:]))
		self.Lu = np.hstack((iso226const.Lu[0], iso226const.Lu, iso226const.Lu[-2:]))
		self.Tf = np.hstack((iso226const.Tf[0], iso226const.Tf, iso226const.Tf[-2:]))


iso226const = ISO226Const()
iso226const_extended = ISO226Const_Extended()
prepared_spl_to_loudness_strict = None
prepared_spl_to_loudness_approx = None

prepared_loudness_to_spl = None



def get_interp2d_spl_to_loudness(isStrict=True):
	"""
	1d-interpolation is done by ISO generic function to get 2-d data,
	then the 2-d data is use for 2-d interpolation.
	This function returns this 2-d interpolator. 

	in 'strict' mode, the range of spl is [0, 90]
	in 'approx' mode, the range of spl is [-20, 110]

	"""
	global prepared_spl_to_loudness_strict
	global prepared_spl_to_loudness_approx

	if isStrict:
		spl_array = np.array(range(STRICT_MIN_SPL, STRICT_MAX_SPL+1, 5)) # [0,5,...85,90]
		freq_array= iso226const.f
		prepared_spl_to_loudness = prepared_spl_to_loudness_strict
	else:
		spl_array = np.array(range(APPROX_MIN_SPL, APPROX_MAX_SPL+1, 5)) # [0,5,...85,90]
		freq_array= iso226const_extended.f
		prepared_spl_to_loudness = prepared_spl_to_loudness_approx

	if prepared_spl_to_loudness is None:
		print 'datapoints was none.'
		# z-axis value for 2-d interpolator. 
		prepared_spl_to_loudness = np.zeros((len(spl_array), len(freq_array)))
				
		if isStrict:
			for spl_ind, spl_val in enumerate(spl_array):
				prepared_spl_to_loudness[spl_ind, :] = spl_to_loudness(spl_val, freqs=freq_array, iso_const=iso226const)
			prepared_spl_to_loudness_strict = prepared_spl_to_loudness
		else:
			for spl_ind, spl_val in enumerate(spl_array):
				prepared_spl_to_loudness[spl_ind, :] = spl_to_loudness(spl_val, freqs=freq_array, iso_const=iso226const_extended)
			prepared_spl_to_loudness_approx = prepared_spl_to_loudness
	else:
		print 'datapoints was NOT none.'
	
	"""
	ret = np.zeros(spls.shape)
	for row_ind, spl_list in enumerate(spls):
		for freq_ind, spl_val in enumerate(spl_list):
			print spl_val, freqs[freq_ind]
			ret[row_ind, freq_ind] = interp2d(spl_array, freq_array, prepared_spl_to_loudness, kind='cubic')(spl_val, freqs[freq_ind])
	"""
	return interp2d(x=spl_array, y=freq_array, z=prepared_spl_to_loudness.transpose(), kind='cubic')


'''
Insted of these two functions, create alternatives that can get multiple values of spls and corresponding freqs.
def spl_to_loudness_iso226(spl, freqs=None, iso_const=iso226const):
	"""It checks spl and frequency range according to the data in iso226"""
	if spl < 0 or spl > 90:
		raise ValueError('SPL value out of bounds!')
	return spl_to_loudness(spl=spl, freqs=freqs, iso_const=iso226const)

def loudness_to_spl_iso226(phon, freqs=None, iso_const=iso226const):
	"""It checks spl and frequency range according to the data in iso226"""
	if phon < 0 or phon > 90:
		raise ValueError('Phon value out of bounds!')
	return loudness_to_spl(phon=phon, freqs=freqs, iso_const=iso226const)
'''
# elementary functions.
def spl_to_loudness(spl, freqs, iso_const=iso226const):
	"""
	Compute loudness values at different frequencies, but given a single value of spl.
	spl: scalar. not list
	freqs: scalar or list. 
	By default, it use iso226const. It can be extended along frequency and spl by using iso226const_ext.
	"""
	Lp = spl
	Af = 10**((Lp - 94 + iso_const.Lu)*(iso_const.af/10))
	Ln = 40*np.log10((Af - (0.4*10**(((iso_const.Tf+iso_const.Lu)/10)-9 ))**iso_const.af )/(4.47E-3) + 1.15)
	try:
		ret = interp1d(iso_const.f, Ln, 'cubic')(freqs)
	except ValueError:
		pdb.set_trace()
	return ret 

def loudness_to_spl(phon, freqs, iso_const=iso226const):
	""" It gets loudness in a unit of phon according to ISO226 and returns the corresponding SPL value(s)
	Compute spl values at different frequencies, but given a single value of phon.
	phon: int or float, or list of any [phon]
	freqs: int or float, or list of any [Hz] 

	return: numpy array size of freqs.shape in SPL
	"""
	# Setup user-defined values for equation
	Ln = phon
	# Deriving sound pressure level from loudness level (iso226 sect 4.1)
	Af=4.47E-3 * (10**(0.025*Ln) - 1.15) + (0.4*10**(((iso_const.Tf+iso_const.Lu)/10)-9 ))**iso_const.af
	Lp=((10/iso_const.af)*np.log10(Af)) - iso_const.Lu + 94
	#Return 
	return interp1d(iso_const.f, Lp, 'cubic')(freqs)

if __name__=='__main__':
	# for debugging purpose
	spls = np.array([[60, 61, 62], [70, 71, 72]])
	freqs = np.array([500, 1000, 3000])
	print spls_to_loudnesses_iso226(spls, freqs)



