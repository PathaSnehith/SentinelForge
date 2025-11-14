from __future__ import annotations

import datetime as dt
from typing import Optional

from sqlmodel import Field, SQLModel


class LogEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: dt.datetime
    source_ip: str
    user: str
    action: str
    status: str
    device: Optional[str] = None
    resource: Optional[str] = None
    bytes_transferred: Optional[int] = 0
    geo: Optional[str] = None


class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: dt.datetime
    rule_id: str
    severity: str
    description: str
    entities: str

