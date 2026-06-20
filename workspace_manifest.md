# WORKSPACE MANIFEST: OPS-SANDBOX

## Current Phase: Core Infrastructure (Pillar 1)
- **Status:** Initialized & Locked to Local Compute
- **Backend Port:** `http://127.0.0.1:11434/v1` (Ollama)
- **Target Model:** `deepseek-coder-v2:16b`

## Project Architecture
- `/.agent/rules/core.md` -> Master autonomous execution protocol (Saved)
- `/workspace_manifest.md` -> Current environment state tracker (Active)
- `/self_healer.py` -> Core feedback loop controller (Pending Deployment)

## Next Milestone
Deploy the runtime interceptor script to catch script exceptions and automate local code patching.
