from __future__ import annotations

import datetime as dt
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, List

from .models import LogEntry

ADMIN_USERS = {"charlie", "diana"}
SENSITIVE_RESOURCES = {"finance", "payroll", "genome", "quarterly"}
PRIVILEGED_ACTIONS = {"config_change", "privilege_escalation"}


@dataclass
class DetectionResult:
    rule_id: str
    severity: str
    description: str
    entities: str


def brute_force_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    failed_attempts = defaultdict(list)
    alerts = []
    for log in sorted(logs, key=lambda l: l.timestamp):
        if log.action == "login" and log.status == "failed":
            failed_attempts[(log.source_ip, log.user)].append(log.timestamp)
            window = [
                t for t in failed_attempts[(log.source_ip, log.user)] if (log.timestamp - t) <= dt.timedelta(minutes=5)
            ]
            failed_attempts[(log.source_ip, log.user)] = window
            if len(window) >= 5:
                alerts.append(
                    DetectionResult(
                        rule_id="BRUTE_FORCE",
                        severity="high",
                        description=f"Five+ failed logins for {log.user} from {log.source_ip} within 5 minutes.",
                        entities=f"user={log.user};ip={log.source_ip}",
                    )
                )
    return alerts


def impossible_travel_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    last_seen = {}
    alerts = []
    for log in sorted(logs, key=lambda l: l.timestamp):
        if log.source_ip in ("", None):
            continue
        last = last_seen.get(log.user)
        if last:
            delta = log.timestamp - last["timestamp"]
            if delta.total_seconds() > 0 and delta.total_seconds() < 3600 and log.geo != last["geo"]:
                alerts.append(
                    DetectionResult(
                        rule_id="IMPOSSIBLE_TRAVEL",
                        severity="medium",
                        description=f"User {log.user} logged in from {last['geo']} and {log.geo} within {delta}.",
                        entities=f"user={log.user};geoA={last['geo']};geoB={log.geo}",
                    )
                )
        last_seen[log.user] = {"timestamp": log.timestamp, "geo": log.geo}
    return alerts


def data_exfil_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    alerts = []
    for log in logs:
        if log.action == "download" and log.bytes_transferred and log.bytes_transferred > 200 * 1024 * 1024:
            alerts.append(
                DetectionResult(
                    rule_id="DATA_EXFIL",
                    severity="high",
                    description=f"{log.user} downloaded {log.bytes_transferred / (1024 * 1024):.1f} MB from {log.resource}.",
                    entities=f"user={log.user};resource={log.resource}",
                )
            )
    return alerts


def admin_after_hours_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    alerts: List[DetectionResult] = []
    for log in logs:
        if log.user in ADMIN_USERS and log.action == "login" and log.status == "success":
            hour = log.timestamp.hour
            if hour >= 22 or hour < 6:
                alerts.append(
                    DetectionResult(
                        rule_id="ADMIN_AFTER_HOURS",
                        severity="medium",
                        description=f"Privileged user {log.user} logged in at {log.timestamp.strftime('%H:%M')} UTC.",
                        entities=f"user={log.user};hour={hour}",
                    )
                )
    return alerts


def sensitive_resource_anomaly_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    alerts: List[DetectionResult] = []
    for log in logs:
        if log.action == "download" and log.resource:
            resource_lower = log.resource.lower()
            if any(keyword in resource_lower for keyword in SENSITIVE_RESOURCES) and "vdi" not in (log.device or ""):
                alerts.append(
                    DetectionResult(
                        rule_id="SENSITIVE_RESOURCE_ANOM",
                        severity="medium",
                        description=f"{log.user} downloaded {log.resource} from untrusted device {log.device}.",
                        entities=f"user={log.user};device={log.device};resource={log.resource}",
                    )
                )
    return alerts


def unauthorized_privileged_action_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    alerts: List[DetectionResult] = []
    for log in logs:
        if log.action in PRIVILEGED_ACTIONS and log.user not in ADMIN_USERS:
            alerts.append(
                DetectionResult(
                    rule_id="UNAUTHORIZED_PRIV_ACTION",
                    severity="critical",
                    description=f"{log.user} executed {log.action} on {log.resource or 'unknown resource'}.",
                    entities=f"user={log.user};resource={log.resource}",
                )
            )
    return alerts


def anomalous_success_rate_detector(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    alerts: List[DetectionResult] = []
    success_counts = defaultdict(int)
    device_counts = defaultdict(int)
    for log in logs:
        if log.action == "login":
            key = (log.user, log.device)
            device_counts[key] += 1
            if log.status == "success":
                success_counts[key] += 1

    for key, attempts in device_counts.items():
        user, device = key
        successes = success_counts.get(key, 0)
        if attempts >= 5 and successes / attempts < 0.2:
            alerts.append(
                DetectionResult(
                    rule_id="LOW_SUCCESS_RATE",
                    severity="medium",
                    description=f"{attempts} login attempts for {user} on {device} with {successes} successes.",
                    entities=f"user={user};device={device}",
                )
            )
    return alerts


DETECTORS = [
    brute_force_detector,
    impossible_travel_detector,
    data_exfil_detector,
    admin_after_hours_detector,
    sensitive_resource_anomaly_detector,
    unauthorized_privileged_action_detector,
    anomalous_success_rate_detector,
]


def run_detections(logs: Iterable[LogEntry]) -> List[DetectionResult]:
    results: List[DetectionResult] = []
    for detector in DETECTORS:
        results.extend(detector(logs))
    return results

