#!/bin/bash

##
# Copyright (c) 2017-2021 LocalStack maintainers and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

##
# Please make sure you have watchman installed before running this script
# https://facebook.github.io/watchman/
#
# Usage examples:
#     watchman.sh folder 'command'
#     watchman.sh src './gradlew buildHot'
##

trap "watchman watch-del $(pwd)" EXIT

folder=$(pwd)/$1
echo "watching folder $folder for changes"

while watchman-wait $folder; do
  bash -c "$2"
  watchman watch-del $(pwd)
done
