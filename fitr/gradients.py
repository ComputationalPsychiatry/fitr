# -*- coding: utf-8 -*-
# Fitr. A package for fitting reinforcement learning models to behavioural data
# Copyright (C) 2018 Abraham Nunes
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
import numpy as np

def logsumexp(x):
    """ Gradient for the logsumexp function taken at point $x$:
    
    $$
    \\frac{\\partial}{\\partial x} \\log \\sum_i e^{x_i} = \Big( \\frac{e^{x_0}}{\\sum_i e^{x_i}}, \ldots, \\frac{e^{x_j}}{\\sum_i e^{x_i}}, \ldots, \\frac{e^{x_n}}{\\sum_i e^{x_i}} \Big)^\\top
    $$
    
    Arguments: 

        x: `ndarray((n,))`

    Returns: 
        
        `ndarray((n,))`

    """
    n = x.size
    expx = np.exp(x)
    sumexpx = np.sum(expx)
    return expx/sumexpx
