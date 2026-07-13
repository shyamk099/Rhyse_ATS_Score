# Pipeline Runner Design Document

## Book 03 — Entity Extraction | Pipeline Validation

### Purpose

The E2E pipeline runner (`scripts/run_pipeline.py`) acts as a synchronized validation harness to execute the ingestion-to-extraction flow. It loads configurations and active rules, feeds the document segments through downstream processors, packages them into a unified DTO, and writes outputs to a designated folder.

### Architectural Decisions

#### 1. Decoupled Runner CLI
The script lives in `scripts/run_pipeline.py` and is not imported by any core domain classes. This keeps the production codebase free of script utility logic.

#### 2. Synchronous Logging
Logging is fully hooked into the project's structured logging infrastructure. Every phase writes JSON logs to standard output, detailing start and success events, as well as timestamps and execution times.

#### 3. Strict Failure Boundary
If any processing phase raises an exception, the runner stops immediately, prints the stack trace, and terminates with a non-zero exit code (1). This enforces pipeline completeness and guarantees that partial, silent failures are never masked.

#### 4. Raw File Integrity
The runner reads inputs directly from the `samples/` directory and writes JSON payloads to the `output/` directory with 4 spaces indentation and UTF-8 encoding.

### Integration Verification

A dedicated integration test suite (`tests/integration/test_pipeline_runner.py`) asserts pipeline compliance:
- Parses PDF and DOCX successfully.
- Stopping on corrupted files (raising exceptions).
- Stopping on empty layouts.
- Rejecting unsupported formats.
- Correctly generating JSON outputs under `output/`.
