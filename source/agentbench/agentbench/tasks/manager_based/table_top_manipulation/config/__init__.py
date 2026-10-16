# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configurations for the table top manipulation environments."""

# We leave this file empty since we don't want to expose any configs in this package directly.
# We still need this file to import the "config" module in the parent package.

from . import hanoi  # noqa: F401
from . import rubiks_cube  # noqa: F401
from . import sharpa_hanoi  # noqa: F401
from . import sharpa_hanoi_no_arm  # noqa: F401
from . import pocket_cube  # noqa: F401
from . import kongming_lock  # noqa: F401

from . import organize_bookshelf  # noqa: F401
