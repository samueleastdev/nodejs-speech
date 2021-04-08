# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.languages.node as node
from pathlib import Path

def patch(library: Path):
    # Manual helper methods override the streaming API so that it
    # accepts streamingConfig when calling streamingRecognize.
    # Rename the generated methods to avoid confusion.
    s.replace(f'src/{version}/{name}_client.ts', r'( +)streamingRecognize\(', '\\1_streamingRecognize(')
    s.replace(f'test/gapic_{name}_{version}.ts', r'client\.streamingRecognize\(', 'client._streamingRecognize(')
    s.replace(f'src/{version}/{name}_client.ts', r'\Z',
        '\n' +
        "import {ImprovedStreamingClient} from '../helpers';\n" +
        '// eslint-disable-next-line @typescript-eslint/no-empty-interface\n' +
        'export interface SpeechClient extends ImprovedStreamingClient {}\n'
    )

node.owlbot_main(
        staging_excludes=['package.json', 'src/index.ts'],

    )


templates = common_templates.node_library(source_location='build/src')
s.copy(templates)

node.postprocess_gapic_library()
