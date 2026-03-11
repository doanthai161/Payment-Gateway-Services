## Shared Libraries

`shared_libs/` contains code shared across services.

The Python shared library currently lives at:

- `shared_libs/python/`
  - package `common` (e.g. `common.base_models`)

---

## Installation (dev)

From the repo root:

```bash
pip install -e .\shared_libs\python
```

Then you can import it in services:

```python
from common.base_models import TimeStampedModel, UUIDModel
```

---

## Current contents

- `common.base_models.TimeStampedModel`
- `common.base_models.UUIDModel`

