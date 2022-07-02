"""A set of functions for checking an environment details.

This file is originally from the Stable Baselines3 repository hosted on GitHub
(https://github.com/DLR-RM/stable-baselines3/)
Original Author: Antonin Raffin

It also uses some warnings/assertions from the PettingZoo repository hosted on GitHub
(https://github.com/PettingZoo-Team/PettingZoo)
Original Author: J K Terry

This was rewritten and split into "env_checker.py" and "passive_env_checker.py" for invasive and passive environment checking
Original Author: Mark Towers

These projects are covered by the MIT License.
"""

import inspect
from copy import deepcopy

import numpy as np

import gym
from gym import logger, spaces
from gym.utils.passive_env_checker import (
    check_action_space,
    check_observation_space,
    env_render_passive_checker,
    env_reset_passive_checker,
    env_step_passive_checker,
)


def data_equivalence(data_1, data_2) -> bool:
    """Assert equality between data 1 and 2, i.e observations, actions, info.

    Args:
        data_1: data structure 1
        data_2: data structure 2

    Returns:
        If observation 1 and 2 are equivalent
    """
    if type(data_1) == type(data_2):
        if isinstance(data_1, dict):
            return data_1.keys() == data_2.keys() and all(
                data_equivalence(data_1[k], data_2[k]) for k in data_1.keys()
            )
        elif isinstance(data_1, tuple):
            return len(data_1) == len(data_2) and all(
                data_equivalence(o_1, o_2) for o_1, o_2 in zip(data_1, data_2)
            )
        elif isinstance(data_1, np.ndarray):
            return np.all(data_1 == data_2)
        else:
            return data_1 == data_2
    else:
        return False


def check_reset_seed(env: gym.Env):
    """Check that the environment can be reset with a seed.

    Args:
        env: The environment to check

    Raises:
        AssertionError: The environment cannot be reset with a random seed,
            even though `seed` or `kwargs` appear in the signature.
    """
    signature = inspect.signature(env.reset)
    if "seed" in signature.parameters or (
        "kwargs" in signature.parameters
        and signature.parameters["kwargs"].kind is inspect.Parameter.VAR_KEYWORD
    ):
        try:
            obs_1 = env.reset(seed=123)
            assert (
                obs_1 in env.observation_space
            ), "The observation returned by `env.reset(seed=123)` is not within the observation space"
            assert (
                env.unwrapped._np_random is not None
            ), "Expects the random number generator to have been generated given a seed was passed to reset. Mostly likely the environment reset function does not call `super().reset(seed=seed)`."
            seed_123_rng = deepcopy(env.unwrapped._np_random)

            obs_2 = env.reset(seed=123)
            assert (
                obs_2 in env.observation_space
            ), "The observation returned by `env.reset(seed=123)` is not within the observation space"
            if env.spec is not None and env.spec.nondeterministic is False:
                assert data_equivalence(
                    obs_1, obs_2
                ), "`env.reset(seed=123)` is not deterministic as the observations are not equivalent"
            assert (
                env.unwrapped._np_random.bit_generator.state
                == seed_123_rng.bit_generator.state
            ), (
                "Mostly likely the environment reset function does not call `super().reset(seed=seed)` "
                "as the random generates are not same when the same seeds are passed to `env.reset`."
            )

            obs_3 = env.reset(seed=456)
            assert (
                obs_3 in env.observation_space
            ), "The observation returned by `env.reset(seed=456)` is not within the observation space"
            assert (
                env.unwrapped._np_random is not None
            ), "Expects the random number generator to have been generated given a seed was passed to reset. Mostly likely the environment reset function does not call `super().reset(seed=seed)`."
            assert (
                env.unwrapped._np_random.bit_generator.state
                != seed_123_rng.bit_generator.state
            ), (
                "Mostly likely the environment reset function does not call `super().reset(seed=seed)` "
                "as the random number generators are not different when different seeds are passed to `env.reset`."
            )

        except TypeError as e:
            raise AssertionError(
                "The environment cannot be reset with a random seed, even though `seed` or `kwargs` appear in the signature. "
                "This should never happen, please report this issue. "
                f"The error was: {e}"
            )

        if env.unwrapped._np_random is None:
            logger.warn(
                "Resetting the environment did not result in seeding its random number generator. "
                "This is likely due to not calling `super().reset(seed=seed)` in the `reset` method. "
                "If you do not use the python-level random number generator, this is not a problem."
            )

        seed_param = signature.parameters.get("seed")
        # Check the default value is None
        if seed_param is not None and seed_param.default is not None:
            logger.warn(
                "The default seed argument in reset should be `None`, "
                "otherwise the environment will by default always be deterministic. "
                f"Actual default: {seed_param.default}"
            )
    else:
        raise gym.error.Error(
            "The `reset` method does not provide the `seed` keyword argument"
        )


def check_reset_info(env: gym.Env):
    """Checks that :meth:`reset` supports the ``return_info`` keyword.

    Args:
        env: The environment to check

    Raises:
        AssertionError: The environment cannot be reset with `return_info=True`,
            even though `return_info` or `kwargs` appear in the signature.
    """
    signature = inspect.signature(env.reset)
    if "return_info" in signature.parameters or (
        "kwargs" in signature.parameters
        and signature.parameters["kwargs"].kind is inspect.Parameter.VAR_KEYWORD
    ):
        try:
            obs = env.reset(return_info=False)
            assert (
                obs in env.observation_space
            ), "The value returned by `env.reset(return_info=True)` is not within the observation space"

            result = env.reset(return_info=True)
            assert isinstance(
                result, tuple
            ), f"Calling the reset method with `return_info=True` did not return a tuple, actual type: {type(result)}"
            assert (
                len(result) == 2
            ), f"Calling the reset method with `return_info=True` did not return a 2-tuple, actual length: {len(result)}"

            obs, info = result
            assert (
                obs in env.observation_space
            ), "The first element returned by `env.reset(return_info=True)` is not within the observation space"
            assert isinstance(
                info, dict
            ), "The second element returned by `env.reset(return_info=True)` was not a dictionary"
        except TypeError as e:
            raise AssertionError(
                "The environment cannot be reset with `return_info=True`, even though `return_info` or `kwargs` "
                "appear in the signature. This should never happen, please report this issue. "
                f"The error was: {e}"
            )
    else:
        raise gym.error.Error(
            "The `reset` method does not provide the `return_info` keyword argument"
        )


def check_reset_options(env: gym.Env):
    """Check that the environment can be reset with options.

    Args:
        env: The environment to check

    Raises:
        AssertionError: The environment cannot be reset with options,
            even though `options` or `kwargs` appear in the signature.
    """
    signature = inspect.signature(env.reset)
    if "options" in signature.parameters or (
        "kwargs" in signature.parameters
        and signature.parameters["kwargs"].kind is inspect.Parameter.VAR_KEYWORD
    ):
        try:
            env.reset(options={})
        except TypeError as e:
            raise AssertionError(
                "The environment cannot be reset with options, even though `options` or `kwargs` appear in the signature. "
                "This should never happen, please report this issue. "
                f"The error was: {e}"
            )
    else:
        raise gym.error.Error(
            "The `reset` method does not provide the `options` keyword argument"
        )


def check_space_limit(space, space_type: str):
    """Check the space limit for only the Box space as a test that only runs as part of `check_env`."""
    if isinstance(space, spaces.Box):
        if np.any(np.equal(space.low, -np.inf)):
            logger.warn(
                f"The {space_type} Box space minimum value is -infinity. This is probably too low."
            )
        if np.any(np.equal(space.high, np.inf)):
            logger.warn(
                f"The {space_type} Box space maximum value is -infinity. This is probably too high."
            )

        # Check that the Box space is normalized
        if space_type == "action":
            if len(space.shape) == 1:  # for vector boxes
                if (
                    np.any(
                        np.logical_and(
                            space.low != np.zeros_like(space.low),
                            np.abs(space.low) != np.abs(space.high),
                        )
                    )
                    or np.any(space.low < -1)
                    or np.any(space.high > 1)
                ):
                    logger.warn(
                        "We recommend you to use a symmetric and normalized Box action space (range=[-1, 1] or [0, 1]) "
                        "https://stable-baselines3.readthedocs.io/en/master/guide/rl_tips.html"  # TODO Add to gymlibrary.ml?
                    )
    elif isinstance(space, spaces.Tuple):
        for subspace in space.spaces:
            check_space_limit(subspace, space_type)
    elif isinstance(space, spaces.Dict):
        for subspace in space.values():
            check_space_limit(subspace, space_type)


def check_env(env: gym.Env, warn: bool = None, skip_render_check: bool = False):
    """Check that an environment follows Gym API.

    This is an invasive function that calls the environment's reset and step.

    This is particularly useful when using a custom environment.
    Please take a look at https://www.gymlibrary.ml/content/environment_creation/
    for more information about the API.

    Args:
        env: The Gym environment that will be checked
        warn: Ignored
        skip_render_check: Whether to skip the checks for the render method. True by default (useful for the CI)
    """
    if warn is not None:
        logger.warn("`check_env` warn parameter is now ignored.")

    assert isinstance(
        env, gym.Env
    ), "Your environment must inherit from the gym.Env class https://www.gymlibrary.ml/content/environment_creation/"

    # ============= Check the spaces (observation and action) ================
    assert hasattr(
        env, "action_space"
    ), "You must specify a action space. https://www.gymlibrary.ml/content/environment_creation/"
    check_action_space(env.action_space)
    check_space_limit(env.action_space, "action")

    assert hasattr(
        env, "observation_space"
    ), "You must specify an observation space. https://www.gymlibrary.ml/content/environment_creation/"
    check_observation_space(env.observation_space)
    check_space_limit(env.observation_space, "observation")

    # ==== Check the reset method ====
    check_reset_seed(env)
    check_reset_options(env)
    check_reset_info(env)

    # ============ Check the returned values ===============
    env_reset_passive_checker(env)
    env_step_passive_checker(env, env.action_space.sample())

    # ==== Check the render method and the declared render modes ====
    if not skip_render_check:
        if env.render_mode is not None:
            env_render_passive_checker(env)

        # todo: recreate the environment with a different render_mode for check that each work
