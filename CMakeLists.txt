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
# Authored approved-scope module; independent execution/provider acceptance pending.
add_custom_command(
  OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/generated/startup.bin"
         "${CMAKE_CURRENT_BINARY_DIR}/generated/startup-map.json"
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/startup_image.py"
          --output-dir "${CMAKE_CURRENT_BINARY_DIR}/generated"
  DEPENDS tools/startup_image.py tools/emitter.py docs/allocation-plan.json
  VERBATIM)
add_custom_target(authored_startup ALL DEPENDS
  "${CMAKE_CURRENT_BINARY_DIR}/generated/startup.bin"
  "${CMAKE_CURRENT_BINARY_DIR}/generated/startup-map.json")
# Candidate artifact boundary. Mars owns byte verification and C++ conversion.
# A pinned Git checkout is required; export verifies every generation input.
find_package(Git REQUIRED)
if(NOT DEFINED SB5200_SOURCE_REVISION)
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${CMAKE_CURRENT_SOURCE_DIR}"
    rev-parse --verify HEAD OUTPUT_VARIABLE SB5200_SOURCE_REVISION
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ERROR_IS_FATAL ANY)
endif()
string(LENGTH "${SB5200_SOURCE_REVISION}" _sb5200_revision_length)
if(NOT _sb5200_revision_length EQUAL 40 OR
   NOT SB5200_SOURCE_REVISION MATCHES "^[0-9a-f]+$")
  message(FATAL_ERROR "SB5200_SOURCE_REVISION must be a full lowercase commit")
endif()
set(_sb5200_export_dir "${CMAKE_CURRENT_BINARY_DIR}/candidate")
add_custom_target(sb5200-runtime-image
  COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tools/export_candidate.py"
    --source-revision "${SB5200_SOURCE_REVISION}" --output-dir "${_sb5200_export_dir}"
  BYPRODUCTS "${_sb5200_export_dir}/startup.bin"
    "${_sb5200_export_dir}/startup-manifest.json" "${_sb5200_export_dir}/startup-map.json"
  DEPENDS tools/export_candidate.py tools/startup_image.py tools/emitter.py
    docs/allocation-plan.json
  VERBATIM)
set_target_properties(sb5200-runtime-image PROPERTIES
  SB5200_IMAGE_FILE "${_sb5200_export_dir}/startup.bin"
  SB5200_MANIFEST_FILE "${_sb5200_export_dir}/startup-manifest.json"
  SB5200_MAP_FILE "${_sb5200_export_dir}/startup-map.json"
  SB5200_SOURCE_REVISION "${SB5200_SOURCE_REVISION}")
include(CTest)
if(BUILD_TESTING)
  add_test(NAME emitter_contract COMMAND "${Python3_EXECUTABLE}"
    -m unittest discover -s "${CMAKE_CURRENT_SOURCE_DIR}/tests" -v)
  set_tests_properties(emitter_contract PROPERTIES TIMEOUT 30
    ENVIRONMENT "PYTHONDONTWRITEBYTECODE=1")
endif()
