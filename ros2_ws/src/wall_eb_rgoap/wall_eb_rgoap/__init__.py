# Copyright (c) 2013, Felix Kolbe
# All rights reserved. BSD License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# * Neither the name of the {organization} nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from common import WorldState, Condition
from common import Precondition, Effect, VariableEffect
from common import Goal, Action

from memory import Memory, MemoryCondition

from planning import Node, Planner, PlanExecutor

from runner import Runner


## shutdown check

def is_shutdown():
    return False

def set_shutdown_check(cb):
    import sys
    sys.modules[__name__].is_shutdown = cb

## logging

import logging
_logger = logging.getLogger('rgoap')
"""The logger used in this library"""
_logger.setLevel(logging.INFO)

# add default console output
_loghandler = logging.StreamHandler()
_loghandler.setLevel(logging.INFO)
_loghandler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
_logger.addHandler(_loghandler)

def remove_default_loghandler():
    """Call this to mute this library or to prevent duplicate messages
    when adding another log handler to the logger named 'rgoap'."""
    _logger.removeHandler(_loghandler)
