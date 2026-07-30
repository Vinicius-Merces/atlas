# Migration to 0.1.0-beta.5

Apply the incremental patch only over `0.1.0-beta.4`.

After copying the patch:

```bash
python scripts/validate_runtime_contract.py
python scripts/validate_conformance.py
python scripts/validate_registry.py
python scripts/validate_package.py
```

The cumulative beta.5 package can be regenerated when a clean installation or
recovery is needed.
