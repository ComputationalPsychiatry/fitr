import autograd.numpy as np
from fitr.utils import logsumexp
import fitr.gradients as grad

class SoftmaxPolicy(object):
    """ Action selection by sampling from a multinomial whose parameters are given by a softmax.

    Action sampling is

    $$
    \mathbf u \sim \mathrm{Multinomial}(1, \mathbf p=\\varsigma(\mathbf v)).
    $$

    Parameters of that distribution are

    $$
    p(\mathbf u|\mathbf v) = \\varsigma(\mathbf v) = \\frac{e^{\\beta \mathbf v}}{\sum_{i}^{|\mathbf v|} e^{\\beta v_i}}.
    $$

    Arguments:

        inverse_softmax_temp: Inverse softmax temperature $\\beta$
        rng: `np.random.RandomState` object

    """
    def __init__(self, inverse_softmax_temp=1., rng=np.random.RandomState()):
        self.inverse_softmax_temp = inverse_softmax_temp
        self.rng  = rng

    def log_prob(self, x):
        """ Computes the log-probability of an action $\mathbf u$

        $$
        \log p(\mathbf u|\mathbf v) = \\beta \mathbf v - \log \sum_{v_i} e^{\\beta \mathbf v_i}
        $$

        Arguments:

            x: State vector of type `ndarray((nstates,))`

        Returns:

            Scalar log-probability
        """
        xcor = x - np.max(x) # For stability
        Bx  = self.inverse_softmax_temp*xcor
        LSE = logsumexp(Bx)
        if not np.isfinite(LSE): LSE = 0.
        return Bx - LSE

    def grad_log_prob(self, x):
        """ Computes the gradients for the softmax policy

        - [ ] TODO: Insert gradient definitions

        Arguments:

            x: State vector of type `ndarray((nstates,))`

        Returns:

            dict: Gradients indexed by `inverse_softmax_temp` or `x`
        """
        gradients = {}

        #x = x - np.max(x)
        Bx = self.inverse_softmax_temp*x
        Dlogsumexp = grad.logsumexp(Bx)

        # Partial derivative with respect to inverse softmax temp
        gradients['inverse_softmax_temp'] = x - np.dot(Dlogsumexp, x)

        # Gradient with respect to x
        Bdiag = np.eye(x.size)*self.inverse_softmax_temp
        Dlsetile = np.tile(self.inverse_softmax_temp*Dlogsumexp, [x.size, 1])
        gradients['x'] = Bdiag - Dlsetile

        return gradients

    def action_prob(self, x):
        """ Computes the softmax """
        exp_x  = np.exp(self.inverse_softmax_temp*x)
        return exp_x/np.sum(exp_x)

    def sample(self, x):
        """ Samples from the action distribution """
        return self.rng.multinomial(1, pvals=self.action_prob(x))

class StickySoftmaxPolicy(object):
    """ Action selection by sampling from a multinomial whose parameters are given by a softmax, but with accounting for the tendency to perseverate (i.e. choosing the previously used action without considering its value).

    Let $\mathbf u_{t-1} = (u_{t-1}^{(i)})_{i=1}^{|\mathcal U|}$ be a one hot vector representing the action taken at the last step, and $\\beta^\\rho$ be an inverse softmax temperature for the influence of this last action.

    Action sampling is thus:

    $$
    \mathbf u \sim \mathrm{Multinomial}(1, \mathbf p=\\varsigma(\mathbf v, \mathbf u_{t-1})).
    $$

    Parameters of that distribution are

    $$
    p(\mathbf u|\mathbf v, \mathbf u_{t-1}) = \\varsigma(\mathbf v, \mathbf u_{t-1}) = \\frac{e^{\\beta \mathbf v + \\beta^\\rho \mathbf u_{t-1}}}{\sum_{i}^{|\mathbf v|} e^{\\beta v_i + \\beta^\\rho u_{t-1}^{(i)}}}.
    $$

    Arguments:

        inverse_softmax_temp: Inverse softmax temperature $\\beta$
        perseveration: Inverse softmax temperature $\\beta^\\rho$ capturing the tendency to repeat the last action taken.
        rng: `np.random.RandomState` object

    """
    def __init__(self, inverse_softmax_temp=1., perseveration=0.01, rng=np.random.RandomState()):
        self.inverse_softmax_temp = inverse_softmax_temp
        self.perseveration        = perseveration
        self.rng  = rng
        self.a_last = [0]

    def log_prob(self, x):
        """ Computes the log-probability of an action $\mathbf u$

        $$
        \log p(\mathbf u|\mathbf v, \mathbf u_{t-1}) = \\big(\\beta \mathbf v + \\beta^\\rho \mathbf u_{t-1}) - \log \sum_{v_i} e^{\\beta \mathbf v_i + \\beta^\\rho u_{t-1}^{(i)}}
        $$

        Arguments:

            x: State vector of type `ndarray((nactions,))`

        Returns:

            Scalar log-probability
        """
        Bx = self.inverse_softmax_temp*x
        stickiness = self.perseveration*self.a_last
        x  = Bx + stickiness
        x  = x - np.max(x)
        LSE = logsumexp(x)
        if not np.isfinite(LSE): LSE = 0.
        return x - LSE

    def grad_log_prob(self, x):
        """ Computes the gradients of the log probability of the sticky softmax observation function

        - [ ] TODO: Insert gradient definitions

        Arguments:

            x: State vector of type `ndarray((nactions,))`

        Returns:

            dict
        """
        gradients = {}

        #x = x - np.max(x)
        logits = self.inverse_softmax_temp*x + self.perseveration*self.a_last
        Dlogsumexp = grad.logsumexp(logits)

        # Partial derivative with respect to inverse softmax temp
        gradients['inverse_softmax_temp'] = x - np.dot(Dlogsumexp, x)
        gradients['perseveration'] = self.a_last - np.dot(Dlogsumexp, self.a_last)

        # Gradient with respect to x
        Bdiag = np.eye(x.size)*self.inverse_softmax_temp
        Dlsetile = np.tile(self.inverse_softmax_temp*Dlogsumexp, [x.size, 1])
        gradients['x'] = Bdiag - Dlsetile

        return gradients

    def action_prob(self, x):
        """ Computes the softmax

        Arguments:

            x: `ndarray((nactions,))` one-hot state vector

        Returns:

            `ndarray((nactions,))` vector of action probabilities
        """
        stickiness = self.perseveration*self.a_last
        exp_x  = np.exp(self.inverse_softmax_temp*x + stickiness)
        return exp_x/np.sum(exp_x)

    def sample(self, x):
        """ Samples from the action distribution

        Arguments:

            x: `ndarray((nactions,))` one-hot state vector

        Returns:

            `ndarray((nactions,))` one-hot action vector
        """
        a_new = self.rng.multinomial(1, pvals=self.action_prob(x))
        self.a_last = a_new
        return a_new

class EpsilonGreedyPolicy(object):
    """ A policy that takes the maximally valued action with probability $1-\\epsilon$, otherwise chooses randomlyself.

    Arguments:

        epsilon: Probability of not taking the action with highest value
        rng: `numpy.random.RandomState` object
    """
    def __init__(self, epsilon=0.1, rng=np.random.RandomState()):
        self.epsilon = epsilon
        self.rng  = rng

    def action_prob(self, x):
        """ Creates vector of action probabilities for e-greedy policy

        Arguments:

            x: `ndarray((nstates,))` one-hot state vector

        Returns:

            `ndarray((nstates,))` vector of action probabilities
        """
        p = np.zeros(x.size)
        p[np.argmax(x)] = 1 - self.epsilon
        p[p == 0.] = np.epsilon/(x.size-1)
        return p

    def sample(self, x):
        """ Samples from the action distribution

        Arguments:

            x: `ndarray((nstates,))` one-hot state vector

        Returns:

            `ndarray((nstates,))` one-hot action vector
        """
        return self.rng.multinomial(1, pvals=self.action_prob(x))
