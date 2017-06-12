import pytest
import numpy as np
import fitr
from fitr.rlparams import *
from fitr.models import twostep as task
from fitr.metrics import parameter_distance
from fitr.metrics import likelihood_distance
from fitr.plotting import heatmap
from fitr.plotting import distance_scatter
from fitr.plotting import distance_hist

def test_param_plot_pdf():
    LearningRate(mean=0.5, sd=0.2).plot_pdf()
    ChoiceRandomness(mean=4.5, sd=2).plot_pdf()
    Perseveration().plot_pdf()

    with pytest.raises(Exception):
        LearningRate().plot_pdf(xlim=[1, 0])
        LearningRate().plot_pdf(xlim=[-1, 1])
        LearningRate().plot_pdf(xlim=[0, 2])
        ChoiceRandomness().plot_pdf(xlim=[-1, 20])
        ChoiceRandomness().plot_pdf(xlim=[1, -20])

def test_synthetic_data_plots():
    group = task.lr_cr_mf().simulate(ntrials=20, nsubjects=5)
    group.plot_cumreward()
    group.cumreward_param_plot()

def test_distance_plots(tmpdir):
    nsubjects = 20
    res = task.lr_cr_mf().simulate(ntrials=20, nsubjects=nsubjects)
    param_dist = parameter_distance(params=res.params)
    ll_dist = likelihood_distance(loglik_func=task.lr_cr_mf().loglikelihood,
                                  params=res.params,
                                  data=res.data)

    group_labels = np.zeros(nsubjects)
    group_labels[10:] = 1

    _file = tmpdir.join('output.pdf')
    heatmap(param_dist,
            title='Heatmap',
            xlab='X',
            ylab='Y',
            interpolation='none',
            save_figure=True,
            figname=_file.strpath)

    _file = tmpdir.join('output.pdf')
    distance_scatter(param_dist,
                     ll_dist,
                     group_labels=group_labels,
                     alpha=0.5,
                     save_figure=True,
                     figname=_file.strpath)

    _file = tmpdir.join('output.pdf')
    distance_hist(param_dist,
                  group_labels=group_labels,
                  alpha=0.5,
                  save_figure=True,
                  figname=_file.strpath)
