.. -*- mode: rst -*-

====================
Fitr Release History
====================

Version 0.0.2
=============

**In Development**

As of this version, development and testing will be done exclusively in Python 3.5+.

New Features
------------

Summary
.......

- ``inference``, ``metrics``, ``models``, ``model_selection``, ``plotting``, ``unsupervised`` subpackages
- ``twostep`` module adds various models for the two-step task. Replaces ``tasks.twostep`` class
- Reinforcement learning parameters in module ``rlparams`` can now be initialized using desired mean and standard deviations. This should allow easier simulation of synthetic data from various tasks.
- Added ``rlparams.Param.plot_pdf`` function to plot the probability density function of synthetic parameters

Inference Subpackage
........................

- The former ``fitr`` module has been turned into the subpackage ``inference``, with all constituent functions therein. Should make development a bit easier with shorter files. Also importing ``fitr.inference`` makes a bit more sense than ``fitr.fitr``, as it was before.
- Implemented ``fitr.inference.MLE()`` class for maximum-likelihood estimation
- Split ``ModelFitResult`` into ``OptimizationFitResult`` (for ``EM``, ``EmpiricalPriors``, and ``MLE``) and ``MCMCFitResult`` (for ``MCMC``) to reduce complexity of the code

Metrics Subpackage
..................

- Model evaluation functions like ``BIC``, ``AIC``, and ``LME`` are now here
- A new ``distance`` module which contains distance metrics
    - ``parameter_distance``
    - ``likelihood_distance``

Models Subpackage
.................

- A new place to keep all of the paradigm model modules
- ``twostep`` module containing models of the two-step task
- ``driftbandit`` module containing models of an N-armed bandit task with drifting reward probabilities
- ``synthetic_data`` module containing object for synthetic behavioural data
- ``stancode`` folder with Stan code for fitting various models. Currently have code for various ``driftbandit`` and ``twostep`` models

Model Selection Subpackage
..........................

- The former ``model_selection`` module is now the ``fitr.model_selection`` subpackage, with constituent functions as individual modules. Should make development easier with shorter files.

Plotting Subpackage
...................

- A new place to write the plotting functions to be used across Fitr
- ``heatmap`` function
- ``confusion_matrix`` function
- ``distance_hist`` and ``distance_scatter`` functions

Unsupervised Subpackage
.......................

- ``cluster`` module including ``AffinityPropagation`` algorithm
- ``embedding`` module including ``TSNE`` algorithm

Enhancements
------------

- Added more unit tests to catch up on code coverage
- Stancode folder to include native ``.stan`` files

Bug Fixes
---------

- Fixed problem with automatic sizing of ``fitrfit.plot_ae()``

Deprecations
------------

Removed Features
----------------

- ``tasks`` module
- ``loglik_functions`` module
- ``generative_models`` module
- ``rlparams.generate_groups``
- 'MAP0' option in the ``fitr.inference.fitmodel`` function ``FitModel.fit()``

Version 0.0.1
=============

**April 8, 2017**

New Features
------------

- Model fitting with Markov-Chain Monte Carlo (via Stan)

List of Contributors
====================

- Abraham Nunes (Dalhousie University. Halifax, NS, Canada)
- Alexander Rudiuk (Dalhousie University. Halifax, NS, Canada)
