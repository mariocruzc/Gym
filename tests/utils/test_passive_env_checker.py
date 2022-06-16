import re
from typing import Dict

import numpy as np
import pytest

import gym
from gym import spaces
from gym.utils.passive_env_checker import (
    check_action_space,
    check_obs,
    check_observation_space,
    passive_env_render_checker,
    passive_env_reset_checker,
    passive_env_step_checker,
)
from tests.testing_env import GenericTestEnv


def modified_space(space: spaces.Space, attribute: str, value):
    setattr(space, attribute, value)
    return space


@pytest.mark.parametrize(
    "test,space,message",
    [
        [
            AssertionError,
            "error",
            "Observation space does not inherit from `gym.spaces.Space`, actual type: <class 'str'>",
        ],
        # ===== Check box observation space ====
        [
            UserWarning,
            spaces.Box(np.zeros((5, 5, 1)), 255 * np.ones((5, 5, 1)), dtype=np.int32),
            "It seems that your observation space is an image but the `dtype` of your observation_space is not `np.uint8`, actual type: int32. If your observation is not an image, we recommend you to flatten the observation to have only a 1D vector",
        ],
        [
            UserWarning,
            spaces.Box(np.ones((2, 2, 1)), 255 * np.ones((2, 2, 1)), dtype=np.uint8),
            "It seems that your observation space is an image but the upper and lower bounds are not in [0, 255]. Generally, CNN policies assume observations are within that range, so you may encounter an issue if the observation values are not.",
        ],
        [
            UserWarning,
            spaces.Box(np.zeros((5, 5, 1)), np.ones((5, 5, 1)), dtype=np.uint8),
            "It seems that your observation space is an image but the upper and lower bounds are not in [0, 255]. Generally, CNN policies assume observations are within that range, so you may encounter an issue if the observation values are not.",
        ],
        [
            UserWarning,
            spaces.Box(np.zeros((5, 5)), np.ones((5, 5))),
            "Your observation space has an unconventional shape (neither an image, nor a 1D vector). We recommend you to flatten the observation to have only a 1D vector or use a custom policy to properly process the data. Actual observation shape: (5, 5)",
        ],
        [
            UserWarning,
            spaces.Box(np.zeros(5), np.zeros(5)),
            "Agent's maximum and minimum observation space values are equal",
        ],
        [
            AssertionError,
            spaces.Box(np.ones(5), np.zeros(5)),
            "Agent's minimum observation value is greater than it's maximum",
        ],
        [
            AssertionError,
            modified_space(spaces.Box(np.zeros(2), np.ones(2)), "low", np.zeros(3)),
            "Agent's observation_space.low and observation_space have different shapes, low shape: (3,), box shape: (2,)",
        ],
        [
            AssertionError,
            modified_space(spaces.Box(np.zeros(2), np.ones(2)), "high", np.ones(3)),
            "Agent's observation_space.high and observation_space have different shapes, high shape: (3,), box shape: (2,)",
        ],
        # ==== Other observation spaces (Discrete, MultiDiscrete, MultiBinary, Tuple, Dict)
        [
            AssertionError,
            modified_space(spaces.Discrete(5), "n", -1),
            "Discrete observation space's number of dimensions must be positive, actual dimensions: -1",
        ],
        [
            AssertionError,
            modified_space(spaces.MultiDiscrete([2, 2]), "_shape", (2, -1)),
            "All dimensions of multi-discrete observation space must be greater than 0, actual shape: (2, -1)",
        ],
        [
            AssertionError,
            modified_space(spaces.MultiBinary((2, 2)), "_shape", (2, -1)),
            "All dimensions of multi-binary observation space must be greater than 0, actual shape: (2, -1)",
        ],
        [
            AssertionError,
            spaces.Tuple([]),
            "An empty Tuple observation space is not allowed.",
        ],
        [
            AssertionError,
            spaces.Dict(),
            "An empty Dict observation space is not allowed.",
        ],
    ],
)
def test_check_observation_space(test, space, message: str):
    """Tests the check observation space."""
    if test is UserWarning:
        with pytest.warns(
            UserWarning, match=f"^\\x1b\\[33mWARN: {re.escape(message)}\\x1b\\[0m$"
        ):
            check_observation_space(space)
    else:
        with pytest.raises(test, match=f"^{re.escape(message)}$"):
            check_observation_space(space)


@pytest.mark.parametrize(
    "test,space,message",
    [
        [
            AssertionError,
            "error",
            "Action space does not inherit from `gym.spaces.Space`, actual type: <class 'str'>",
        ],
        # ===== Check box observation space ====
        [
            UserWarning,
            spaces.Box(np.zeros(5), np.zeros(5)),
            "Agent's maximum and minimum action space values are equal",
        ],
        [
            AssertionError,
            spaces.Box(np.ones(5), np.zeros(5)),
            "Agent's minimum action value is greater than it's maximum",
        ],
        [
            AssertionError,
            modified_space(spaces.Box(np.zeros(2), np.ones(2)), "low", np.zeros(3)),
            "Agent's action_space.low and action_space have different shapes, low shape: (3,), box shape: (2,)",
        ],
        [
            AssertionError,
            modified_space(spaces.Box(np.zeros(2), np.ones(2)), "high", np.ones(3)),
            "Agent's action_space.high and action_space have different shapes, high shape: (3,), box shape: (2,)",
        ],
        # ==== Other observation spaces (Discrete, MultiDiscrete, MultiBinary, Tuple, Dict)
        [
            AssertionError,
            modified_space(spaces.Discrete(5), "n", -1),
            "Discrete action space's number of dimensions must be positive, actual dimensions: -1",
        ],
        [
            AssertionError,
            modified_space(spaces.MultiDiscrete([2, 2]), "_shape", (2, -1)),
            "All dimensions of multi-discrete action space must be greater than 0, actual shape: (2, -1)",
        ],
        [
            AssertionError,
            modified_space(spaces.MultiBinary((2, 2)), "_shape", (2, -1)),
            "All dimensions of multi-binary action space must be greater than 0, actual shape: (2, -1)",
        ],
        [
            AssertionError,
            spaces.Tuple([]),
            "An empty Tuple action space is not allowed.",
        ],
        [AssertionError, spaces.Dict(), "An empty Dict action space is not allowed."],
    ],
)
def test_check_action_space(test, space: spaces.Space, message: str):
    """Tests the check action space function."""
    if test is UserWarning:
        with pytest.warns(
            UserWarning, match=f"^\\x1b\\[33mWARN: {re.escape(message)}\\x1b\\[0m$"
        ):
            check_action_space(space)
    else:
        with pytest.raises(test, match=f"^{re.escape(message)}$"):
            check_action_space(space)


@pytest.mark.parametrize(
    "test,obs,obs_space,message",
    [
        [
            AssertionError,
            3,
            spaces.Discrete(2),
            "The obs returned by the `testing()` method is not within the observation space",
        ],
        [
            AssertionError,
            np.array([1], dtype=np.uint8)[0],
            spaces.Discrete(1),
            "The obs returned by the `testing()` method must be an int or np.int64, actually type: <class 'numpy.uint8'>",
        ],
        [
            AssertionError,
            1,
            spaces.Box(0, 1, ()),
            "The obs returned by the `testing()` method must be a numpy array, actually type: <class 'int'>",
        ],
        [
            AssertionError,
            [1, 2],
            spaces.Tuple([spaces.Discrete(1), spaces.Discrete(2)]),
            "The obs returned by the `testing()` method must be a tuple, actually type: <class 'list'>",
        ],
        [
            AssertionError,
            (1, 2, 3),
            spaces.Tuple([spaces.Discrete(1), spaces.Discrete(2)]),
            "The obs returned by the `testing()` method length is not same as the observation space length, obs length: 3, space length: 2",
        ],
        [
            AssertionError,
            {1, 2, 3},
            spaces.Dict(a=spaces.Discrete(1), b=spaces.Discrete(2)),
            "The obs returned by the `testing()` method must be a dict, actually <class 'set'>",
        ],
        [
            AssertionError,
            {"a": 1, "c": 2},
            spaces.Dict(a=spaces.Discrete(1), b=spaces.Discrete(2)),
            "The obs returned by the `testing()` method observation keys is not same as the observation space keys, obs keys: ['a', 'c'], space keys: ['a', 'b']",
        ],
    ],
)
def test_check_obs(test, obs, obs_space: spaces.Space, message: str):
    """Tests the check observations function."""
    if test is UserWarning:
        with pytest.warns(
            UserWarning, match=f"^\\x1b\\[33mWARN: {re.escape(message)}\\x1b\\[0m$"
        ):
            check_obs(obs, obs_space, "testing")
    else:
        with pytest.raises(test, match=f"^{re.escape(message)}$"):
            check_obs(obs, obs_space, "testing")


def _reset_no_seed(self, return_info=False, options=None):
    return self.observation_space.sample()


def _reset_seed_default(self, seed="error", return_info=False, options=None):
    return self.observation_space.sample()


def _reset_no_return_info(self, seed=None, options=None):
    return self.observation_space.sample()


def _reset_no_option(self, seed=None, return_info=False):
    return self.observation_space.sample()


def _make_reset_results(results):
    def _reset_result(self, seed=None, return_info=False, options=None):
        return results

    return _reset_result


@pytest.mark.parametrize(
    "test,func,message,kwargs",
    [
        [
            UserWarning,
            _reset_no_seed,
            "Future gym versions will require that `Env.reset` can be passed a `seed` instead of using `Env.seed` for resetting the environment random number generator.",
            {},
        ],
        [
            UserWarning,
            _reset_seed_default,
            "The default seed argument in `Env.reset` should be `None`, otherwise the environment will by default always be deterministic. Actual default: seed='error'",
            {},
        ],
        [
            UserWarning,
            _reset_no_return_info,
            "Future gym versions will require that `Env.reset` can be passed `return_info` to return information from the environment resetting.",
            {},
        ],
        [
            UserWarning,
            _reset_no_option,
            "Future gym versions will require that `Env.reset` can be passed `options` to allow the environment initialisation to be passed additional information.",
            {},
        ],
        [
            AssertionError,
            _make_reset_results([0, {}]),
            "The result returned by `env.reset(return_info=True)` was not a tuple, actually type: <class 'list'>",
            {"return_info": True},
        ],
        [
            AssertionError,
            _make_reset_results((0, {1, 2})),
            "The second element returned by `env.reset(return_info=True)` was not a dictionary, actually type: <class 'set'>",
            {"return_info": True},
        ],
        [
            AssertionError,
            _make_reset_results(2),
            "The obs returned by the `reset()` method must be a numpy array, actually type: <class 'int'>",
            {"return_info": False},
        ],
        [
            AssertionError,
            _make_reset_results((2, {})),
            "The obs returned by the `reset()` method must be a numpy array, actually type: <class 'int'>",
            {"return_info": True},
        ],
    ],
)
def test_passive_env_reset_checker(test, func: callable, message: str, kwargs: Dict):
    """Tests the passive env reset check"""
    if test is UserWarning:
        with pytest.warns(
            UserWarning, match=f"^\\x1b\\[33mWARN: {re.escape(message)}\\x1b\\[0m$"
        ):
            passive_env_reset_checker(GenericTestEnv(reset_fn=func), **kwargs)
    else:
        with pytest.raises(test, match=f"^{re.escape(message)}$"):
            passive_env_reset_checker(GenericTestEnv(reset_fn=func), **kwargs)


def modified_step(
    self, obs=None, reward=0, terminated=False, truncated=None, info=None
):
    if obs is None:
        obs = self.observation_space.sample()
    if info is None:
        info = {}

    if truncated is None:
        return obs, reward, terminated, info
    else:
        return obs, reward, terminated, truncated, info


@pytest.mark.parametrize(
    "test,func,message",
    [
        [
            AssertionError,
            lambda self, _: "error",
            "Expects step result to be a tuple, actual type: <class 'str'>",
        ],
        [
            AssertionError,
            lambda self, _: modified_step(self, terminated="error"),
            "The `done` signal must be a boolean, actual type: <class 'str'>",
        ],
        [
            AssertionError,
            lambda self, _: modified_step(self, terminated="error", truncated=False),
            "The `terminated` signal must be a boolean, actual type: <class 'str'>",
        ],
        [
            AssertionError,
            lambda self, _: modified_step(self, truncated="error"),
            "The `truncated` signal must be a boolean, actual type: <class 'str'>",
        ],
        [
            AssertionError,
            lambda self, _: modified_step(self, terminated=True, truncated=True),
            "Only `terminated` or `truncated` can be true, not both.",
        ],
        [
            gym.error.Error,
            lambda self, _: (1, 2, 3),
            "Expected `Env.step` to return a four or five elements, actually number of elements returned: 3.",
        ],
        [
            AssertionError,
            lambda self, _: modified_step(self, reward="error"),
            "The reward returned by `step()` must be a float, int, np.integer or np.floating, actual type: <class 'str'>",
        ],
        [
            UserWarning,
            lambda self, _: modified_step(self, reward=np.nan),
            "The reward is a NaN value.",
        ],
        [
            UserWarning,
            lambda self, _: modified_step(self, reward=np.inf),
            "The reward is an inf value.",
        ],
        [
            AssertionError,
            lambda self, _: modified_step(self, info="error"),
            "The `info` returned by `step()` must be a python dictionary, actual type: <class 'str'>",
        ],
    ],
)
def test_passive_env_step_checker(test, func, message):
    """Tests the passive env step checker."""
    if test is UserWarning:
        with pytest.warns(
            UserWarning, match=f"^\\x1b\\[33mWARN: {re.escape(message)}\\x1b\\[0m$"
        ):
            passive_env_step_checker(GenericTestEnv(step_fn=func), 0)
    else:
        with pytest.raises(test, match=f"^{re.escape(message)}$"):
            passive_env_step_checker(GenericTestEnv(step_fn=func), 0)


@pytest.mark.parametrize(
    "test,env,message",
    [
        [
            gym.error.Error,
            GenericTestEnv(render_modes=None),
            "No render modes was declared in the environment (env.metadata['render_modes'] is None or not defined), you may have trouble when calling `.render()`.",
        ],
        [
            AssertionError,
            GenericTestEnv(render_modes="Testing mode"),
            "Expects the render_modes to be a sequence (i.e. list, tuple), actual type: <class 'str'>",
        ],
        [
            AssertionError,
            GenericTestEnv(render_modes=["Testing mode", 1]),
            "Expects all render modes to be strings, actual types: [<class 'str'>, <class 'int'>].",
        ],
        [
            UserWarning,
            GenericTestEnv(
                render_modes=["Testing mode"],
                render_fps=None,
                render_mode="Testing mode",
                render_fn=lambda self: 0,
            ),
            "No render fps was declared in the environment (env.metadata['render_fps'] is None or not defined), rendering may occur at inconsistent fps.",
        ],
        [
            AssertionError,
            GenericTestEnv(render_modes=["Testing mode"], render_fps="fps"),
            "Expects the `env.metadata['render_fps']` to be an integer, actual type: <class 'str'>.",
        ],
        [
            AssertionError,
            GenericTestEnv(render_modes=[], render_fps=30, render_mode="Test"),
            "With no render_modes, expects the render_mode to be None",
        ],
        [
            AssertionError,
            GenericTestEnv(
                render_modes=["Testing mode"], render_fps=30, render_mode="Non mode"
            ),
            "The environment was initialized successfully however with an unsupported render mode.",
        ],
    ],
)
def test_passive_render_checker(test, env: GenericTestEnv, message: str):
    """Tests the passive render checker."""
    if test is UserWarning:
        with pytest.warns(
            UserWarning, match=f"^\\x1b\\[33mWARN: {re.escape(message)}\\x1b\\[0m$"
        ):
            passive_env_render_checker(env)
    else:
        with pytest.raises(test, match=f"^{re.escape(message)}$"):
            passive_env_render_checker(env)
