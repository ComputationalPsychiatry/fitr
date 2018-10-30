import numpy as np
import matplotlib.pyplot as plt
from fitr import generate_behavioural_data
import fitr.gradients as grad
from fitr.agents import RWSoftmaxAgent
from fitr.environments import RandomContextualBandit
from fitr.criticism.plotting import actual_estimate
from fitr.inference import mlepar
from fitr.utils import sigmoid, stable_exp

class MyBanditTask(RandomContextualBandit):
    def __init__(self):
        super().__init__(nactions=4,
                         noutcomes=3,
                         nstates=4,
                         min_actions_per_context=None,
                         alpha=0.1,
                         alpha_start=1.,
                         shift_flip='shift',
                         reward_lb=-1,
                         reward_ub=1,
                         reward_drift='on',
                         drift_mu=np.zeros(3),
                         drift_sd=1.)

data = generate_behavioural_data(MyBanditTask, RWSoftmaxAgent, 20, 200)

def log_prob(w, D):
    agent = RWSoftmaxAgent(task=MyBanditTask(),
                           learning_rate=sigmoid(w[0]),
                           inverse_softmax_temp=stable_exp(w[1]))
    for t in range(D.shape[0]):
        x=D[t,:7]; u=D[t,7:11]; r=D[t,11]; x_=D[t,12:]
        agent.log_prob(x, u)
        agent.learning(x, u, r, x_, None)
    J = np.diag([grad.sigmoid(w[0]), grad.exp(w[1])])
    return -agent.logprob_, -J@agent.grad_


res = mlepar(log_prob, data.tensor, 2, maxstarts=5, jac=True, hess=True)
X = res.transform_xmin([sigmoid, stable_exp])

# Criticism: Actual vs. Estimate Plots
lr_fig  = actual_estimate(data.params[:,1], X[:,0]); plt.show()
ist_fig = actual_estimate(data.params[X[:,1]<20,2], X[X[:,1]<20,1]); plt.show()
