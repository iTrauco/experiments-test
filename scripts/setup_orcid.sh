#!/bin/bash

# get project root from script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
README="$PROJECT_ROOT/README.md"
REF_DIR="$PROJECT_ROOT/references"

# create references dir and bib files
mkdir -p "$REF_DIR"
touch "$REF_DIR"/citations.bib "$REF_DIR"/datasets.bib "$REF_DIR"/software.bib

# write README in references
echo "Contains .bib files used for citation tracking and dataset provenance in this project." > "$REF_DIR/README.md"

# append author + references block if not already present
if ! grep -q "0009-0005-8113-6528" "$README"; then
cat <<'EOF' >> "$README"

---
**Author:** Christopher Trauco | [ORCID: 0009-0005-8113-6528](https://orcid.org/0009-0005-8113-6528)

---

## References

This repository includes citation tracking files located in the `references/` directory:

* [`citations.bib`](references/citations.bib)
* [`datasets.bib`](references/datasets.bib)
* [`software.bib`](references/software.bib)

These BibTeX files help manage research provenance and provide citation records for notebooks and datasets used in this project.
EOF

  echo "✅ ORCID and references block added to README.md"
else
  echo "⚠️  ORCID section already present in README.md"
fi
