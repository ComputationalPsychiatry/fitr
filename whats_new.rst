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

- ``twostep`` module adds various models for the two-step task. Replaces ``tasks.twostep`` class
- Reinforcement learning parameters in module ``rlparams`` can now be initialized using desired mean and standard deviations. This should allow easier simulation of synthetic data from various tasks.
- Added ``rlparams.Param.plot_pdf`` function to plot the probability density function of synthetic parameters

Enhancements
------------

- The ``SyntheticData`` object was moved to a new module, ``fitrdata`` to account for the new task-specific model structures being introduced.
- Added more unit tests to catch up on code coverage

Bug Fixes
---------

Deprecations
------------

- The modules ``tasks``, ``loglik_functions``, and ``generative_models`` are deprecated and will be replaced by task specific modules, such as ``twostep``, wherein each model of the task will be represented as an object with the relevant likelihood functions and generative models contained within.

Removed Features
----------------

- ``tasks.twostep``
- ``rlparams.generate_groups``

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
