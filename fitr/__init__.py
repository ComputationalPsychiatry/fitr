# -*- coding: utf-8 -*-
# Fitr. A package for fitting reinforcement learning models to behavioural data
# Copyright (C) 2017 Abraham Nunes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# CONTACT INFO:
#   Abraham Nunes
#    Email: nunes@dal.ca
#
# ============================================================================

from .fitr import fitrmodel
from .fitr import EM
from .fitr import EmpiricalPriors
from .fitr import MCMC
from .fitr import fitrfit

from .rlparams import *

from .loglik_functions import *
from .generative_models import *
from .model_selection import *
from .tasks import *
from .utils import *


__all__ = ['fitrmodel',
           'EM',
           'EmpiricalPriors',
           'MCMC',
           'fitrfit',
           'rlparams',
           'loglik_functions',
           'generative_models',
           'model_selection',
           'tasks',
           'utils']
