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
import fitr.utils as fu

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
    return fu.softmax(x)

def max(x):
    """ Gradient of a max reduction over a vector, with respect to that vector

    Arguments:

        x: `ndarray((n,))`

    Returns:

        `ndarray((n,))`

    """
    xmax = np.max(x)
    out = np.zeros(x.size)
    wheremax = np.equal(x, xmax)
    nmax = wheremax.astype(np.int).sum()
    out[wheremax] = 1/nmax
    return out

def softmax(x):
    """ Jacobian of the softmax function.

    Let

        - $x = (x_0, x_1, \ldots, x_n)^\\top
        - $v = (e^{x_0}, e^{x_1}, \ldots, e^{x_n})^\\top$
        - $z = \sum_{i=0}^n v_i
        - $\\mathbf{I}$ be the identity matrix of size $n \\times n$.

    Then the Jacobian of the softmax function $\\varsigma(x)$ is

    $$
    \\partial_x \\varsigma(x) = \\frac{zv \\mathbf I - vv^\\top}{z^2}
    $$

    Arguments:

        x: `ndarray((n,))`

    Returns:

        `ndarray((n,n))`

    """
    x = x - np.max(x)
    v = np.exp(x)
    z = np.sum(v)
    return (np.diag(z*v) - np.outer(v, v))/(z**2)
