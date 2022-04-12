from __future__ import annotations

import contextlib
import copy
import difflib
import importlib
import importlib.util
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Optional, Tuple, Type, Union

from gym.envs.__relocated__ import internal_env_relocation_map
from gym.wrappers import AutoResetWrapper, OrderEnforcing, TimeLimit

if sys.version_info < (3, 10):
    import importlib_metadata as metadata  # type: ignore
else:
    import importlib.metadata as metadata

from gym import error, logger

ENV_ID_RE: re.Pattern = re.compile(
    r"^(?:(?P<namespace>[\w:-]+)\/)?(?:(?P<name>[\w:.-]+?))(?:-v(?P<version>\d+))?$"
)


def load(name: str) -> Type:
    mod_name, attr_name = name.split(":")
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, attr_name)
    return fn


def parse_env_id(id: str) -> Tuple[Optional[str], str, Optional[int]]:
    """Parse environment ID string format.

    This format is true today, but it's *not* an official spec.
    [namespace/](env-name)-v(version)    env-name is group 1, version is group 2

    2016-10-31: We're experimentally expanding the environment ID format
    to include an optional namespace.
    """
    match = ENV_ID_RE.fullmatch(id)
    if not match:
        raise error.Error(
            f"Malformed environment ID: {id}."
            f"(Currently all IDs must be of the form {ENV_ID_RE}.)"
        )
    namespace, name, version = match.group("namespace", "name", "version")
    if version is not None:
        version = int(version)

    return namespace, name, version


def get_env_id(ns: Optional[str], name: str, version: Optional[int]):
    """Get the full env ID given a name and (optional) version and namespace.
    Inverse of parse_env_id."""

    full_name = name
    if version is not None:
        full_name += f"-v{version}"
    if ns is not None:
        full_name = ns + "/" + full_name
    return full_name


@dataclass
class EnvSpec:
    id: str
    entry_point: Optional[Union[Callable, str]] = field(default=None)
    reward_threshold: Optional[float] = field(default=None)
    nondeterministic: bool = field(default=False)
    max_episode_steps: Optional[int] = field(default=None)
    order_enforce: bool = field(default=True)
    autoreset: bool = field(default=False)
    kwargs: dict = field(default_factory=dict)

    namespace: Optional[str] = field(init=False)
    name: str = field(init=False)
    version: Optional[int] = field(init=False)

    def __post_init__(self):
        # Initialize namespace, name, version
        self.namespace, self.name, self.version = parse_env_id(self.id)

    def make(self, **kwargs) -> Type:
        # For compatibility purposes
        return make(self, **kwargs)


# Global registry of environments. Meant to be accessed through `register` and `make`
registry: dict[str, EnvSpec] = dict()
current_namespace: Optional[str] = None


@contextlib.contextmanager
def namespace(ns: str):
    global current_namespace
    old_namespace = current_namespace
    current_namespace = ns
    yield
    current_namespace = old_namespace


def register(id: str, **kwargs):
    global registry, current_namespace
    full_id = (current_namespace or "") + id
    spec = EnvSpec(id=full_id, **kwargs)
    check_spec_register(spec)
    if spec.id in registry:
        raise error.RegistrationError(
            f"Attempted to register {spec.id} but it was already registered"
        )
    registry[spec.id] = spec


def make(
    env_id: str | EnvSpec,
    max_episode_steps: Optional[int] = None,
    autoreset: bool = False,
    **kwargs,
):
    if isinstance(env_id, EnvSpec):
        spec = env_id
    else:
        spec = registry.get(env_id)

        ns, name, version = parse_env_id(env_id)
        latest_version = find_newest_version(ns, name)
        if (
            version is not None
            and latest_version is not None
            and latest_version > version
        ):
            logger.warn(
                f"The environment {env_id} is out of date. You should consider "
                f"upgrading to version `v{latest_version}`."
            )
        if version is None and latest_version is not None:
            version = latest_version
            new_env_id = get_env_id(ns, name, version)
            spec = registry.get(new_env_id)
            logger.warn(
                f"Using the latest versioned environment `{new_env_id}` "
                f"instead of the unversioned environment `{env_id}`."
            )

        if spec is None:
            check_version_exists(ns, name, version)
            raise error.Error(f"No registered env with id: {env_id}")

    _kwargs = spec.kwargs.copy()
    _kwargs.update(kwargs)

    # TODO: add a minimal env checker on initialization
    if spec.entry_point is None:
        raise error.Error(f"{spec.id} registered but entry_point is not specified")
    elif callable(spec.entry_point):
        cls = spec.entry_point
    else:
        # Assume it's a string
        cls = load(spec.entry_point)

    env = cls(**_kwargs)

    spec = copy.deepcopy(spec)
    spec.kwargs = _kwargs

    env.unwrapped.spec = spec

    if spec.order_enforce:
        env = OrderEnforcing(env)

    if max_episode_steps is not None:
        env = TimeLimit(env, max_episode_steps)
    elif spec.max_episode_steps is not None:
        env = TimeLimit(env, spec.max_episode_steps)

    if autoreset:
        env = AutoResetWrapper(env)

    return env


def spec(env_id: str) -> EnvSpec:
    spec_ = registry.get(env_id)
    if spec_ is None:
        ns, name, version = parse_env_id(env_id)
        check_version_exists(ns, name, version)
        raise error.Error(f"No registered env with id: {env_id}")
    else:
        assert isinstance(spec_, EnvSpec)
        return spec_


def check_namespace_exists(ns: Optional[str]):
    if ns is None:
        return
    namespaces = {
        spec_.namespace for spec_ in registry.values() if spec_.namespace is not None
    }
    if ns in namespaces:
        return

    suggestion = (
        difflib.get_close_matches(ns, namespaces, n=1) if len(namespaces) > 0 else None
    )
    suggestion_msg = (
        f"Did you mean: `{suggestion[0]}`?"
        if suggestion
        else f"Have you installed the proper package for {ns}?"
    )

    raise error.NamespaceNotFound(f"Namespace {ns} not found. {suggestion_msg}")


def check_name_exists(ns: Optional[str], name: str):
    check_namespace_exists(ns)
    names = {spec_.name for spec_ in registry.values()}

    if name in names:
        return

    if namespace is None and name in internal_env_relocation_map:
        relocated_namespace, relocated_package = internal_env_relocation_map[name]
        message = f"The environment `{name}` has been moved out of Gym to the package `{relocated_package}`."

        # Check if the package is installed
        # If not instruct the user to install the package and then how to instantiate the env
        if importlib.util.find_spec(relocated_package) is None:
            message += (
                f" Please install the package via `pip install {relocated_package}`."
            )

        # Otherwise the user should be able to instantiate the environment directly
        if namespace != relocated_namespace:
            message += f" You can instantiate the new namespaced environment as `{relocated_namespace}/{name}`."

        raise error.NameNotFound(message)

    suggestion = difflib.get_close_matches(name, names, n=1)
    namespace_msg = f" in namespace {ns}" if ns else ""
    suggestion_msg = f"Did you mean: `{suggestion[0]}`?" if suggestion else ""

    raise error.NameNotFound(
        f"Environment {name} doesn't exist{namespace_msg}. {suggestion_msg}"
    )


def check_version_exists(ns: Optional[str], name: str, version: Optional[int]):
    if get_env_id(ns, name, version) in registry:
        return

    check_name_exists(ns, name)
    if version is None:
        return

    message = f"Environment version `v{version}` for environment `{get_env_id(ns, name, None)}` doesn't exist."

    env_specs = [
        spec_
        for spec_ in registry.values()
        if spec_.namespace == ns and spec_.name == name
    ]
    env_specs = sorted(env_specs, key=lambda spec_: int(spec_.version or -1))

    default_spec = [spec_ for spec_ in env_specs if spec_.version is None]

    if default_spec:
        message += f" It provides the default version {default_spec[0].id}`."
        if len(env_specs) == 1:
            raise error.DeprecatedEnv(message)

    # Process possible versioned environments

    versioned_specs = [spec_ for spec_ in env_specs if spec_.version is not None]

    latest_spec = max(versioned_specs, key=lambda spec: spec.version, default=None)
    if latest_spec is not None and version > latest_spec.version:
        version_list_msg = ", ".join(f"`v{spec_.version}`" for spec_ in env_specs)
        message += f" It provides versioned environments: [ {version_list_msg} ]."

        raise error.VersionNotFound(message)

    if latest_spec is not None and version < latest_spec.version:
        raise error.DeprecatedEnv(
            f"Environment version v{version} for `{get_env_id(ns, name, None)}` is deprecated. "
            f"Please use `{latest_spec.id}` instead."
        )


def find_newest_version(ns: Optional[str], name: str) -> Optional[int]:
    version: list[int] = [
        spec_.version
        for spec_ in registry.values()
        if spec_.namespace == ns and spec_.name == name and spec_.version is not None
    ]
    return max(version, default=None)


def check_spec_register(spec: EnvSpec):
    global registry, current_namespace
    if current_namespace is not None:
        if spec.namespace is not None:
            logger.warn(
                f"Custom namespace `{spec.namespace}` is being overridden "
                f"by namespace `{current_namespace}`. If you are developing a "
                "plugin you shouldn't specify a namespace in `register` "
                "calls. The namespace is specified through the "
                "entry point package metadata."
            )

    latest_versioned_spec = max(
        (
            spec_
            for spec_ in registry.values()
            if spec_.name == spec.name and spec_.version is not None
        ),
        key=lambda spec_: int(spec_.version),
        default=None,
    )

    unversioned_spec = next(
        (
            spec_
            for spec_ in registry.values()
            if spec_.namespace == spec.namespace
            and spec_.name == spec.name
            and spec_.version is None
        ),
        None,
    )

    if unversioned_spec and spec.version is not None:
        raise error.RegistrationError(
            "Can't register the versioned environment "
            f"`{spec.id}` when the unversioned environment "
            f"`{unversioned_spec.id}` of the same name already exists."
        )
    elif latest_versioned_spec and spec.version is None:
        raise error.RegistrationError(
            "Can't register the unversioned environment "
            f"`{spec.id}` when the versioned environment "
            f"`{latest_versioned_spec.id}` of the same name "
            f"already exists. Note: the default behavior is "
            f"that `gym.make` with the unversioned environment "
            f"will return the latest versioned environment"
        )


def load_env_plugins(entry_point: str = "gym.envs") -> None:
    # Load third-party environments
    for plugin in metadata.entry_points(group=entry_point):
        # Python 3.8 doesn't support plugin.module, plugin.attr
        # So we'll have to try and parse this ourselves
        try:
            module, attr = plugin.module, plugin.attr  # type: ignore  ## error: Cannot access member "attr" for type "EntryPoint"
        except AttributeError:
            if ":" in plugin.value:
                module, attr = plugin.value.split(":", maxsplit=1)
            else:
                module, attr = plugin.value, None
        except:
            module, attr = None, None
        finally:
            if attr is None:
                raise error.Error(
                    f"Gym environment plugin `{module}` must specify a function to execute, not a root module"
                )

        context = namespace(plugin.name)
        if plugin.name.startswith("__") and plugin.name.endswith("__"):
            # `__internal__` is an artifact of the plugin system when
            # the root namespace had an allow-list. The allow-list is now
            # removed and plugins can register environments in the root
            # namespace with the `__root__` magic key.
            if plugin.name == "__root__" or plugin.name == "__internal__":
                context = contextlib.nullcontext()
            else:
                logger.warn(
                    f"The environment namespace magic key `{plugin.name}` is unsupported. "
                    "To register an environment at the root namespace you should specify "
                    "the `__root__` namespace."
                )

        with context:
            fn = plugin.load()
            try:
                fn()
            except Exception as e:
                logger.warn(str(e))
