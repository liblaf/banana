#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

git_root=$(git rev-parse --show-toplevel)
readarray -t files < <(fd --fixed-strings --type file '__init__.pyi' "$git_root")
for file in "${files[@]}"; do
  cat > "$(dirname "$file")/__init__.py" <<- EOF
import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
EOF
done