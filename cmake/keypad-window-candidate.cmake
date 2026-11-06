# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
# Explicit parent opt-in: include this file after adding the baseline module.
# Separate target preserves the original711a2e9 CMake/export input contract.
find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)
find_package(Git REQUIRED)
get_filename_component(_sb5200_keypad_window_root "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)
if(NOT DEFINED SB5200_KEYPAD_WINDOW_SOURCE_REVISION)
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${_sb5200_keypad_window_root}"
    rev-parse --verify HEAD OUTPUT_VARIABLE SB5200_KEYPAD_WINDOW_SOURCE_REVISION
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ERROR_IS_FATAL ANY)
endif()
string(LENGTH "${SB5200_KEYPAD_WINDOW_SOURCE_REVISION}" _sb5200_keypad_window_length)
if(NOT _sb5200_keypad_window_length EQUAL 40 OR
   NOT SB5200_KEYPAD_WINDOW_SOURCE_REVISION MATCHES "^[0-9a-f]+$")
  message(FATAL_ERROR "SB5200_KEYPAD_WINDOW_SOURCE_REVISION must be a full lowercase commit")
endif()
set(_sb5200_keypad_window_dir "${CMAKE_CURRENT_BINARY_DIR}/keypad-window-candidate")
add_custom_target(sb5200-keypad-window-image
  COMMAND "${Python3_EXECUTABLE}" "${_sb5200_keypad_window_root}/tools/export_keypad_window_candidate.py"
    --source-revision "${SB5200_KEYPAD_WINDOW_SOURCE_REVISION}" --output-dir "${_sb5200_keypad_window_dir}"
  BYPRODUCTS "${_sb5200_keypad_window_dir}/startup.bin"
    "${_sb5200_keypad_window_dir}/startup-manifest.json" "${_sb5200_keypad_window_dir}/startup-map.json"
  VERBATIM)
set_target_properties(sb5200-keypad-window-image PROPERTIES
  SB5200_IMAGE_FILE "${_sb5200_keypad_window_dir}/startup.bin"
  SB5200_MANIFEST_FILE "${_sb5200_keypad_window_dir}/startup-manifest.json"
  SB5200_MAP_FILE "${_sb5200_keypad_window_dir}/startup-map.json"
  SB5200_SOURCE_REVISION "${SB5200_KEYPAD_WINDOW_SOURCE_REVISION}")
