import json
from pathlib import Path

import requests


DATASET = "lmarena-ai/leaderboard-dataset"
ROWS_URL = "https://datasets-server.huggingface.co/rows"
CONFIGS = ("text_to_image", "image_edit", "text_to_video", "image_to_video")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "arena_data"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for config in CONFIGS:
        response = requests.get(
            ROWS_URL,
            params={
                "dataset": DATASET,
                "config": config,
                "split": "latest",
                "offset": 0,
                "length": 100,
            },
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
        if not payload.get("rows"):
            raise RuntimeError(f"Arena dataset returned no rows for {config}")
        output_path = OUTPUT_DIR / f"{config}.json"
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Updated {config}: {len(payload['rows'])} rows")


if __name__ == "__main__":
    main()
