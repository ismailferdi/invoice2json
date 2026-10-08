"""Invoice2JSON: fine-tuning a 0.5B open-weight model for reliable structured invoice extraction.

Sub-packages and the phase that populates each:
- src.data → Phase 1 (data pipeline).
- src.template → Phase 2 (template toolkit).
- src.training → Phase 4 (QLoRA training).
- src.evaluation → Phases 3 & 5 (baselines and evaluation harness).
- src.registry → Phase 6 (adapter registry).
- src.serving → Phase 6 (serving stack).
- src.monitoring → Phase 7 (monitoring).
- src.utils → cross-cutting (logging, config, hub).
"""
