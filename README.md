# MLOps Engineering Internship – Technical Assessment

This repository contains a simple batch-style MLOps pipeline built using Python and Docker.

The objective of this project is to demonstrate:

- Reproducibility
- Configuration-based execution
- Structured logging
- Metrics tracking
- Error handling
- Containerized deployment

The pipeline processes cryptocurrency OHLCV data and generates a trading signal based on a rolling mean of the `close` price.

---

## Project Structure

```
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── metrics.json
├── run.log
└── README.md
```

---

## ⚙️ How the Pipeline Works

1. Loads configuration from `config.yaml`
2. Sets a fixed random seed for reproducibility
3. Reads the input CSV file
4. Computes a rolling mean on the `close` column
5. Generates a trading signal:
   - `1` if `close > rolling_mean`
   - `0` otherwise
6. Calculates:
   - Total rows processed
   - Signal rate
   - Execution latency (in milliseconds)
7. Writes structured output to `metrics.json`
8. Logs execution details to `run.log`

---

## 📝 Configuration

The configuration file (`config.yaml`) contains:

```yaml
seed: 42
window: 5
version: "v1"
```

### Parameters

| Parameter | Description                            |
| --------- | -------------------------------------- |
| `seed`    | Random seed for deterministic behavior |
| `window`  | Rolling window size for moving average |
| `version` | Version identifier included in metrics |

---

## 🛠 Setup Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

After execution, the following files will be generated:

- `metrics.json`
- `run.log`

---

## 🐳 Docker Instructions

### Build Docker Image

```bash
docker build -t mlops-task .
```

### Run Container

```bash
docker run --rm mlops-task
```

The container will:

- Execute the job automatically
- Print metrics to stdout
- Generate `metrics.json`
- Generate `run.log`
- Exit with status code `0` on success

---

## 📊 Expected Metrics Output

### Successful Run

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```

### Error Case

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}
```

---

## 📦 Dependencies

- pandas
- numpy
- pyyaml

All dependencies are listed in `requirements.txt`.

---

## 🧪 Reproducibility & Design Notes

- The pipeline is deterministic due to the fixed seed.
- No hardcoded paths are used.
- Logging is implemented using Python’s built-in `logging` module.
- Structured JSON output ensures easy integration with monitoring systems.
- Error handling covers:
  - Missing input files
  - Invalid CSV format
  - Empty files
  - Missing required columns (`close`)
  - Invalid configuration structure

---

## 🎯 Key MLOps Concepts Demonstrated

- Batch data processing
- Config-driven execution
- Deterministic pipelines
- Structured metrics tracking
- Logging best practices
- Containerized reproducibility