# -*- coding: utf-8 -*-

import fitr
import numpy as np
import scipy

# Test softmax is returning numpy array
# Test softmax returns array with correct dimensional length
def test_softmax():
	_temp = fitr.utils.softmax([0.1, 0.2])
	assert(type(_temp) is np.ndarray)
	assert(np.shape(_temp)[0] == 2)

## Test action is returning an integer
def test_action():
	_temp = fitr.utils.action([0.5, 0.5])
	assert(type(_temp) is np.int64)

# Test logsumexp is of type numpy.float64
# Test that results are the same as the scipy method
def test_logsumexp():
	_temp = fitr.utils.logsumexp([0.1, 0.2, 100, 200, 500])
	assert(type(_temp) is np.float64)
	assert(round(_temp) == round(scipy.misc.logsumexp([0.1, 0.2, 100, 200, 500])))

# Test trans_UC
def test_trans_UC():
	y = fitr.utils.trans_UC(values_U = [-17, 10],
							rng = ['all_unc'])
	assert(y == [-17, 10])

	y = fitr.utils.trans_UC(values_U = [-17],
							rng = ['unit'])
	assert(0 < y[0] < 1)

	y = fitr.utils.trans_UC(values_U = [17],
							rng = ['pos'])
	assert(0 < y[0])

	y = fitr.utils.trans_UC(values_U = [-17],
							rng = ['half'])
	assert(0 < y[0] < 0.5)

	y = fitr.utils.trans_UC(values_U = [-17],
							rng = ['unc'])
	assert(y[0] == -17)
