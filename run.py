import argparse
import json
import logging
import os
import sys
import time
import numpy as np
import pandas as pd
import yaml


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError("Configuration file not found")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise ValueError("Invalid configuration file structure")

    return config


def load_data(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input CSV file not found")

    try:
        df = pd.read_csv(input_path)
    except Exception:
        raise ValueError("Invalid CSV file format")

    if df.empty:
        raise ValueError("Input file is empty")

    if "close" not in df.columns:
        raise ValueError("Missing required column: close")

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logging(args.log_file)
    logging.info("Job started")

    start_time = time.time()

    try:
        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        np.random.seed(seed)

        # Load data
        df = load_data(args.input)
        rows_processed = len(df)

        logging.info(f"Data loaded: {rows_processed} rows")

        # Rolling mean
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        print(df[["close", "rolling_mean"]].head(10))
        logging.info(f"Rolling mean calculated with window={window}")

        # Signal generation
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
        logging.info("Signals generated")

        # Metrics
        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        output = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(output, f, indent=4)

        logging.info(f"Metrics: signal_rate={signal_rate:.4f}, rows_processed={rows_processed}")
        logging.info(f"Job completed successfully in {latency_ms}ms")

        print(json.dumps(output, indent=4))
        sys.exit(0)

    except Exception as e:
        latency_ms = int((time.time() - start_time) * 1000)

        error_output = {
            "version": config["version"] if 'config' in locals() else "unknown",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=4)

        logging.error(f"Error occurred: {str(e)}")
        logging.info(f"Job failed in {latency_ms}ms")

        print(json.dumps(error_output, indent=4))
        sys.exit(1)


if __name__ == "__main__":
    main()