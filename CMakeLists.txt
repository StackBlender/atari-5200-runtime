# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
cmake_minimum_required(VERSION 3.20)
project(atari_5200_runtime VERSION 0.1.0 LANGUAGES NONE)
find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)

# This generates a tool fixture with zero runtime capabilities, not the future
# sb5200-runtime-image provider. No firmware, compiler or network is needed.
add_custom_command(
  OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/generated/layout-test.bin"
         "${CMAKE_CURRENT_BINARY_DIR}/generated/layout-test.json"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/layout_fixture.py"
          --output-dir "${CMAKE_CURRENT_BINARY_DIR}/generated"
  DEPENDS tools/layout_fixture.py tools/emitter.py
  VERBATIM)
add_custom_target(layout_fixture ALL DEPENDS
  "${CMAKE_CURRENT_BINARY_DIR}/generated/layout-test.bin"
  "${CMAKE_CURRENT_BINARY_DIR}/generated/layout-test.json")
include(CTest)
if(BUILD_TESTING)
  add_test(NAME emitter_contract COMMAND "${Python3_EXECUTABLE}"
    -m unittest discover -s "${CMAKE_CURRENT_SOURCE_DIR}/tests" -v)
  set_tests_properties(emitter_contract PROPERTIES TIMEOUT 30
    ENVIRONMENT "PYTHONDONTWRITEBYTECODE=1")
endif()
