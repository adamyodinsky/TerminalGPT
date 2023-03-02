#!/bin/sh

set -e

cat "$(which terminalgpt)" | sed '1d' > /tmp/terminalgpt
echo "#!/usr/bin/env bash" > "$(which terminalgpt)"

echo "export OPENAI_API_KEY=${OPENAI_API_KEY}" >> "$(which terminalgpt)"
cat /tmp/terminalgpt >> "$(which terminalgpt)"
