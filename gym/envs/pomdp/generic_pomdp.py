from six import StringIO
import sys
import numpy as np
import gym
from gym import spaces
from gym import error
from gym.utils import seeding, colorize
import logging
logger = logging.getLogger(__name__)


class GenericPOMDPEnv(gym.Env):
    """
    A generic POMDP implementation. It supports an underlying MDP with additional clutter (random) state.
    The observables are then produced by multiplying the cluttered state with a confusion matrix
        Obs = (I - Rand(#State + #Clutter x #State + #Clutter)) * (State concat Clutter)
    It also includes a set of good states and a set of bad states.
    The reward signal is next computed using the following scheme:
        -1.0  if entering a bad state
        +1.0  if entering a good state
        -1.0  if reaching the maximum number of moves
        -1.0/max_num_moves  otherwise
    """
    metadata = {"render.modes": ["human", "ansi"]}

    def __init__(self, nb_states=None, nb_actions=None, confusion_dim=None, transition_table=None,
                 nb_unobservable=0, init_state=None, confusion_level=0.1, good_terminals=list(),
                 bad_terminals=list(), max_move=100, overwrite=False, pretty_printing=True):
        """
        Args:
            nb_states:  number of MDP states
            nb_actions: number of actions
            confusion_dim: number of clutter states
            transition_table: MDP transition table [s, a, s', p] --> p = transition probability
            nb_unobservable: number of unobservable states
            init_state: MDP init state
            confusion_level: in [0, 1], level of confusion --  0 == no confusion
            good_terminals: list of good terminal states resulting in reward +1
            bad_terminals: list of bad terminal states resulting in reward -1
            max_move: maximum allowable number of steps (terminal state if reached with reward -1)
            overwrite: boolean for overwriting saved confusion matrix
            pretty_printing: boolean for numpy output
        """
        assert None not in (nb_states, nb_actions, confusion_dim, transition_table, init_state) and \
            len(good_terminals) > 0, 'Bad one or more input arguments.'
        self.__dict__.update(locals())
        if pretty_printing:
            np.set_printoptions(precision=3, suppress=True)

    def _seed(self, seed=None):
        self.np_random, seed1 = seeding.np_random(seed)
        return seed1

    def _step(self, action):
        if self.done or self.move > self.max_move:
            self.done = True
            return self.obs, None, self.done, {'state': self.state, 'step': self.move}
        self.move += 1

        t_list = []
        for t in self.transition_table:
            if t[0] == self.state and t[1] == action:
                t_list.append(t)
        if t_list:  # otherwise self-loop (if not in the transition_table)
            t_probs = [item[-1] for item in t_list]
            t_idx = np.random.multinomial(n=1, pvals=np.array(t_probs)).argmax()
            self.state = t_list[t_idx][2]

        self.obs = self.state2obs(self.state)
        if self.state in self.good_terminals:
            self.done = True
            reward = 1.
        elif self.state in self.bad_terminals:
            self.done = True
            reward = -1.
        elif self.move == self.max_move:
            self.done = True
            reward = -1.
        else:
            self.done = False
            reward = -1. / self.max_move
        return self.obs, reward, self.done, {'state': self.state, 'step': self.move}

    def _reset(self):
        self.move = 0
        self.state = self.init_state
        self.obs = self.state2obs(self.init_state)
        self.action_space = spaces.Discrete(self.nb_actions)
        self.observation_space = spaces.Box(low=-np.inf,
                                            high=np.inf,
                                            shape=(self.nb_states - self.nb_unobservable + self.confusion_dim,))
        self.done = False
        return self.obs

    def _render(self, mode='human', close=False):
        if close:
            return
        output = StringIO() if mode == 'ansi' else sys.stdout
        output.write(colorize('base state: ', color='cyan', bold=True) + str(self.state) + '\n')
        output.write(colorize('observation: ', color='blue') + str(self.obs) + '\n')
        if mode == 'ansi':
            return output

    def state2obs(self, s_id):
        dim = self.confusion_dim + self.nb_states
        s = np.zeros(dim, dtype='float32')
        s[: self.confusion_dim] = np.random.uniform(-self.confusion_level, self.confusion_level,
                                                    size=self.confusion_dim)
        s[self.confusion_dim + s_id] = 1.

        # TODO: remove indices of unobservable states
        if self.nb_unobservable > 0:
            pass

        if not hasattr(self, "randproj"):
            # put confusion lazily
            self.randproj = np.eye(dim) - np.random.uniform(-self.confusion_level, self.confusion_level,
                                                            size=(dim, dim))
            self.invrandproj = np.linalg.inv(self.randproj)
            if self.overwrite:
                np.save('confusion.npy', (self.randproj, self.invrandproj))
            else:
                logger.warning('Confusion matrices exist! Set overwrite=True to let overwrite.')
        s = np.dot(self.randproj, s)
        return s

    def obs2state(self, s):
        s = np.dot(self.invrandproj, s)
        s1 = s[self.confusion_dim:]
        return np.argmax(s1)

    def write_mdp_to_dot(self, file='mdp.dot'):
        # after calling this method use the following for example:
        #    $ dot -T png -O mdp.dot
        import networkx as nx
        g = nx.DiGraph()
        g.add_nodes_from(np.arange(self.nb_states))
        edges = [(tr[0], tr[2], {'label': tr[1]}) for tr in self.transition_table]
        g.add_edges_from(edges)
        nx.drawing.nx_pydot.write_dot(g, file)
