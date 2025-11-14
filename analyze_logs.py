import argparse
import json
import pathlib

from app import services


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SentinelForge offline log analyzer.")
    parser.add_argument("--file", required=True, type=pathlib.Path, help="Path to JSON log dataset.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not args.file.exists():
        raise SystemExit(f"File not found: {args.file}")
    entries = json.loads(args.file.read_text(encoding="utf-8"))
    alerts = services.ingest_logs(entries)
    print(f"Ingested {len(entries)} events. Generated {len(alerts)} alerts.")
    for alert in alerts:
        print(f"[{alert.severity.upper()}] {alert.rule_id} - {alert.description} ({alert.entities})")


if __name__ == "__main__":
    main()

