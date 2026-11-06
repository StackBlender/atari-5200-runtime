# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
"""Separate original ordinary-ram candidate, not product/provider approval."""
from timer_experiment import candidate as build_candidate,verify_checkout as check,main as export_main
EXTRA_INPUTS=('tools/timer_experiment.py', 'tools/ordinary_ram_image.py', 'tools/export_ordinary_ram_candidate.py', 'cmake/ordinary-ram-candidate.cmake', 'docs/ordinary-ram-profile.json')
def candidate(revision):return build_candidate('ordinary-ram',revision,__file__)
def verify_checkout(root,revision):return check(root,revision,EXTRA_INPUTS)
if __name__=='__main__':export_main('ordinary-ram',EXTRA_INPUTS,__file__)
