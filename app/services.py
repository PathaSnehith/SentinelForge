from __future__ import annotations

import datetime as dt
import json
import pathlib
from typing import Iterable, List

from sqlmodel import func, select

from . import detections
from .database import get_session, init_db
from .models import Alert, LogEntry


def parse_log(entry: dict) -> LogEntry:
    timestamp = entry.get("timestamp")
    if isinstance(timestamp, str):
        timestamp = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    return LogEntry(
        timestamp=timestamp,
        source_ip=entry.get("source_ip", ""),
        user=entry.get("user", "unknown"),
        action=entry.get("action", ""),
        status=entry.get("status", ""),
        device=entry.get("device"),
        resource=entry.get("resource"),
        bytes_transferred=entry.get("bytes_transferred", 0),
        geo=entry.get("geo"),
    )


def ingest_logs(entries: Iterable[dict]) -> List[Alert]:
    init_db()
    parsed = [parse_log(e) for e in entries]
    alerts = detections.run_detections(parsed)
    with get_session() as session:
        for log in parsed:
            session.add(log)
        session.commit()

    with get_session() as session:
        persisted = []
        for alert in alerts:
            alert_row = Alert(
                created_at=dt.datetime.utcnow(),
                rule_id=alert.rule_id,
                severity=alert.severity,
                description=alert.description,
                entities=alert.entities,
            )
            session.add(alert_row)
            persisted.append(alert_row)
        session.commit()
        return persisted


def load_alerts() -> List[Alert]:
    init_db()
    with get_session() as session:
        return session.query(Alert).order_by(Alert.created_at.desc()).all()


def load_logs(limit: int = 1000) -> List[LogEntry]:
    init_db()
    with get_session() as session:
        return session.query(LogEntry).order_by(LogEntry.timestamp.desc()).limit(limit).all()


def ingest_from_file(path: str) -> List[Alert]:
    entries = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    return ingest_logs(entries)


def get_stats() -> dict:
    init_db()
    with get_session() as session:
        log_count = session.exec(select(func.count(LogEntry.id))).one()
        alert_count = session.exec(select(func.count(Alert.id))).one()
        severity_rows = session.exec(
            select(Alert.severity, func.count(Alert.id)).group_by(Alert.severity)
        ).all()
        severity_breakdown = {row[0]: row[1] for row in severity_rows}
        top_users = session.exec(
            select(LogEntry.user, func.count(LogEntry.id))
            .group_by(LogEntry.user)
            .order_by(func.count(LogEntry.id).desc())
            .limit(5)
        ).all()
        return {
            "logs": log_count,
            "alerts": alert_count,
            "severity_breakdown": severity_breakdown,
            "top_users": [{"user": user, "events": count} for user, count in top_users],
        }

