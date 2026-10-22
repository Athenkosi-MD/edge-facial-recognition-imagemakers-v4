"""
Timezone helpers.

Most columns in this app are written with ``datetime.utcnow()`` or the
database's ``CURRENT_TIMESTAMP`` default, so they are stored as *naive UTC*.
A few columns written by the recognizer (``first_seen_at``, ``last_seen_at``,
``captured_at``) and all Trip times are already *naive SAST*.

Everything shown to users must be SAST (UTC+2), so UTC-stored values are
converted at display time with ``to_sast`` / the ``sast`` Jinja filter.
Do NOT apply these to columns that are already SAST.
"""
from datetime import datetime, timedelta, timezone

SAST = timezone(timedelta(hours=2), 'SAST')  # South Africa has no DST


def to_sast(dt):
    """Naive-UTC (or tz-aware) datetime -> naive SAST datetime. None-safe."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SAST).replace(tzinfo=None)


def fmt_sast(dt, fmt='%Y-%m-%d %H:%M'):
    """Format a naive-UTC datetime as SAST text; None -> None."""
    dt = to_sast(dt)
    return dt.strftime(fmt) if dt else None


def now_sast():
    """Current wall-clock time in SAST (naive)."""
    return datetime.now(SAST).replace(tzinfo=None)


def sast_filter(dt, fmt='%d %b %Y %H:%M'):
    """Jinja filter: {{ some_utc_dt|sast('%d %b %Y %H:%M') }}. None -> ''."""
    return fmt_sast(dt, fmt) or ''
