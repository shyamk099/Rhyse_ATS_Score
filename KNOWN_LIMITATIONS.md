# Known Limitations

## 1. Algorithmic Constraints
* **Exact Matching Only**: No fuzzy matching, semantic AI, embeddings, or scoring is supported. Features are matched based on exact matching of canonical database identifiers or normalized case-insensitive string value equivalencies.
* **No Semantic Equivalency**: E.g., "Software Engineer" will not match "Developer" or "Software Developer" unless they share the same canonical experience identifier, or their names are structurally identical under string normalization.

## 2. Scalability Limits
* **Cartesian Matches**: In the case of raw features that share duplicate names, using the `KEEP_ALL` policy can match them Cartesian-product-wise. In large datasets with duplicate entries, this leads to $O(N \times M)$ match results, which can grow rapidly.
* **Telemetry Summation**: Aggregate statistics in the pipeline sum feature counts across individual matcher collections. Since each matcher receives the flattened feature lists from the matching service pipeline, the resulting `total_resume_features` in the `CanonicalMatchCollection` counts aggregated feature scopes, rather than unique resume-level feature nodes.

## 3. Data Integrity & Ingestion
* **No In-Place Repairs**: The system enforces read-only processing at all stages. Incomplete or malformed inputs are flagged as warnings or errors in the `ValidationSummary`, but never auto-corrected or filled with dummy defaults.
