# Datasets

Place shared manufacturing datasets here (CSV, Parquet, etc.).

Load with `shared-core/data_loader.py`:

```python
from data_loader import load_csv  # add shared-core to PYTHONPATH
df = load_csv("../datasets/your_file.csv")
```
