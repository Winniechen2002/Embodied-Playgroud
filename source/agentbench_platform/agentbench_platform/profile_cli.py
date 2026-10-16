"""Capability configuration for environment launchers; optional tools require explicit grants."""
from .profiles import RunProfile, CAPABILITY_VERSION


def frozen_profile(observation, tools=(), experience='none', *, available_tools=(), capability_level=None):
    profile = RunProfile(observation=observation, tools=tuple(tools), experience=experience,
        capability_level=capability_level,
        capability_profile_version=CAPABILITY_VERSION if capability_level is not None else None)
    if set(profile.tools) - set(available_tools):
        raise ValueError('Selected tools unavailable')
    return profile.public_record()


def add_profile_arguments(parser):
    parser.add_argument('--profile',choices=('privileged','rgb','rgbd'),default='privileged')
    parser.add_argument('--capability-level',type=int,choices=range(4),default=None,
                        help='Versioned environment grant; does not certify an external client')
    parser.add_argument('--experience-profile',choices=('none','reference'),default='none')
    parser.add_argument('--tool',action='append',default=[])
    parser.add_argument('--tool-setup',help='Trusted offline plugin setup manifest')
    parser.add_argument('--cube-solver-setup',help='Legacy option; no cube solver is bundled in the environment distribution')
    parser.add_argument('--disable-cube-solver',action='store_true',help='Compatibility flag; environment launchers never grant a solver by default')


def selected_tools(args):
    tools=list(args.tool)
    disabled=getattr(args,'disable_cube_solver',False)
    if disabled and 'cube_solver' in tools:
        raise ValueError('cube_solver cannot be both selected and disabled')
    return tuple(tools)


def profile_from_args(args, *, available_tools=()):
    return frozen_profile(args.profile,selected_tools(args),args.experience_profile,available_tools=available_tools,
                          capability_level=getattr(args,'capability_level',None))


