# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
# New explicit target; old producer exports are never widened to smaller boards.
find_package(Python3 3.10 REQUIRED COMPONENTS Interpreter)
find_package(Git REQUIRED)
get_filename_component(_sb5200_linear8k_root "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)
if(NOT DEFINED SB5200_LINEAR8K_GUARDED_SOURCE_REVISION)
  execute_process(COMMAND "${GIT_EXECUTABLE}" -C "${_sb5200_linear8k_root}"
    rev-parse --verify HEAD OUTPUT_VARIABLE SB5200_LINEAR8K_GUARDED_SOURCE_REVISION
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ERROR_IS_FATAL ANY)
endif()
string(LENGTH "${SB5200_LINEAR8K_GUARDED_SOURCE_REVISION}" _sb5200_linear8k_length)
if(NOT _sb5200_linear8k_length EQUAL 40 OR
   NOT SB5200_LINEAR8K_GUARDED_SOURCE_REVISION MATCHES "^[0-9a-f]+$")
  message(FATAL_ERROR "SB5200_LINEAR8K_GUARDED_SOURCE_REVISION must be full lowercase commit")
endif()
set(_sb5200_linear8k_dir "${CMAKE_CURRENT_BINARY_DIR}/linear8k-guarded-candidate")
add_custom_target(sb5200-linear8k-guarded-image
  COMMAND "${Python3_EXECUTABLE}" "${_sb5200_linear8k_root}/tools/export_linear8k_guarded_candidate.py"
    --source-revision "${SB5200_LINEAR8K_GUARDED_SOURCE_REVISION}" --output-dir "${_sb5200_linear8k_dir}"
  BYPRODUCTS "${_sb5200_linear8k_dir}/startup.bin" "${_sb5200_linear8k_dir}/startup-map.json"
    "${_sb5200_linear8k_dir}/startup-manifest.json" VERBATIM)
set_target_properties(sb5200-linear8k-guarded-image PROPERTIES
  SB5200_IMAGE_FILE "${_sb5200_linear8k_dir}/startup.bin"
  SB5200_MANIFEST_FILE "${_sb5200_linear8k_dir}/startup-manifest.json"
  SB5200_MAP_FILE "${_sb5200_linear8k_dir}/startup-map.json"
  SB5200_SOURCE_REVISION "${SB5200_LINEAR8K_GUARDED_SOURCE_REVISION}")
