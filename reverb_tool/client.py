from __future__ import annotations

import json
import time
from typing import Any
from urllib import error, parse, request


class ReverbAPIError(RuntimeError):
    """Raised when the Reverb API returns an unrecoverable error."""


class ReverbClient:
    def __init__(
        self,
        token: str,
        base_url: str = "https://api.reverb.com/api",
        timeout_s: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.6,
    ) -> None:
        if not token:
            raise ValueError("Token is required")

        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "reverb-api-control-tool/0.1.0",
        }

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if query:
            url = f"{url}?{parse.urlencode(query, doseq=True)}"

        data_bytes = json.dumps(body).encode("utf-8") if body is not None else None
        last_err: str | None = None

        for attempt in range(self.max_retries + 1):
            req = request.Request(url=url, data=data_bytes, method=method.upper(), headers=self.headers)
            try:
                with request.urlopen(req, timeout=self.timeout_s) as response:
                    payload = response.read()
                    if not payload:
                        return {"status": "ok", "code": response.status}
                    return json.loads(payload.decode("utf-8"))
            except error.HTTPError as exc:
                status = exc.code
                raw = exc.read().decode("utf-8", errors="replace")
                if status in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    sleep_s = self.backoff_factor * (2**attempt)
                    time.sleep(sleep_s)
                    continue

                try:
                    payload = json.loads(raw)
                except ValueError:
                    payload = {"raw": raw}
                last_err = f"HTTP {status}: {payload}"
                break
            except error.URLError as exc:
                if attempt < self.max_retries:
                    sleep_s = self.backoff_factor * (2**attempt)
                    time.sleep(sleep_s)
                    continue
                last_err = f"Connection error: {exc.reason}"
                break

        raise ReverbAPIError(last_err or "Unknown API error")
