# -*- coding: utf-8 -*-

import fitr
from fitr.inference import EM
from fitr.model_selection import BIC
from fitr.model_selection import AIC
from fitr.model_selection import BMS

from fitr import tasks
from fitr import generative_models as gm
from fitr import loglik_functions as ll
import numpy as np
import scipy

def test_model_selections():
	nsubjects = 5
	ntrials = 10

	lr = fitr.rlparams.LearningRate()
	cr = fitr.rlparams.ChoiceRandomness()
	params = [lr, cr]

	group = np.zeros([nsubjects, 2])
	group[:, 0] = lr.sample(size=nsubjects)
	group[:, 1] = cr.sample(size=nsubjects)

	res = tasks.bandit(narms=2).simulate(params=group, ntrials=ntrials)

	m1 = EM(loglik_func=ll.bandit_ll().lr_cr,
			params=params)

	m2 = EM(loglik_func=ll.bandit_ll().lr_cr_rs,
			params=[fitr.rlparams.LearningRate(),
		  		    fitr.rlparams.ChoiceRandomness(),
				    fitr.rlparams.RewardSensitivity()])

	fit1 = m1.fit(data=res.data)
	fit2 = m2.fit(data=res.data)

	models = [fit1, fit2]
	bms_results = BMS(model_fits=models, c_limit=1e-10).run()
	bms_results.plot(statistic='pxp')
	bms_results.plot(statistic='xp')

	bic_results = BIC(model_fits=models).run()
	bic_results.plot(statistic='BIC')

	aic_results = AIC(model_fits=models).run()
	aic_results.plot(statistic='AIC')

	assert(len(bms_results.modelnames) == 2)
	assert(len(bms_results.xp) == 2)
	assert(len(bms_results.pxp) == 2)

	assert(len(bic_results.modelnames) == 2)
	assert(len(bic_results.BIC) == 2)

	assert(len(aic_results.modelnames) == 2)
	assert(len(aic_results.AIC) == 2)
