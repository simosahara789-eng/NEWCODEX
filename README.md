# Reverb API Control Tool

A professional Python CLI and reusable SDK to operate your Reverb API account with one token.

## What this tool gives you

- Unified control for all common Reverb API domains visible in your token scopes:
  - feedback, payouts, listings, lists/feed, messages, offers, orders, profile, reviews, addresses
- Strong defaults:
  - bearer token auth
  - request timeout
  - retries with exponential backoff for transient errors (`429`, `5xx`)
  - clear JSON output
- Flexible operation:
  - list supported operations
  - call operations by name
  - pass query/body JSON from CLI
  - override API base URL if needed

## 1) Generate your Reverb token (recommended scopes)

From your screenshot page, create a Personal Access Token and choose scopes based on what you need.

Typical full-control set (for your own account data and actions):

- `public`
- `read_feedback`, `write_feedback`
- `read_payouts`
- `read_listings`, `write_listings`
- `read_lists`, `write_lists`
- `read_messages`, `write_messages`
- `read_offers`, `write_offers`
- `read_orders`, `write_orders`
- `read_profile`, `write_profile`
- `read_reviews`, `write_reviews`
- `read_addresses`, `write_addresses`

> Security tip: only grant scopes you truly need.

## 2) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set environment variables:

```bash
export REVERB_API_TOKEN="<your_token_here>"
export REVERB_API_BASE_URL="https://api.reverb.com/api"   # default already
```

## 3) Basic usage

List all supported operations:

```bash
reverbctl list-ops
```

Call an operation (GET profile):

```bash
reverbctl call read_profile
```

Call with query params:

```bash
reverbctl call read_orders --query '{"page": 1, "per_page": 20}'
```

Call with body (example write/update):

```bash
reverbctl call write_profile --body '{"shop": {"name": "My Shop"}}'
```

Pretty output is enabled by default. For compact JSON:

```bash
reverbctl call read_listings --compact
```

## 4) Python SDK usage

```python
from reverb_tool.client import ReverbClient
from reverb_tool.endpoints import OPERATIONS

client = ReverbClient(token="<token>")

# Example: read profile
op = OPERATIONS["read_profile"]
result = client.request(op.method, op.path)
print(result)
```

## 5) How the operation model works

Each named operation maps to an HTTP method + endpoint path.

Example:
- `read_profile` -> `GET /my/profile`
- `write_profile` -> `PUT /my/profile`

You can extend `reverb_tool/endpoints.py` with additional endpoint mappings if your account/API plan exposes more resources.

## 6) Troubleshooting

- `401 Unauthorized`: token missing/invalid.
- `403 Forbidden`: token exists but lacks required scope.
- `404 Not Found`: endpoint may differ by API version/resource path.
- `429 Too Many Requests`: tool auto-retries; reduce frequency if persistent.

## 7) Disclaimer

Reverb may evolve endpoints and payload formats over time. This tool is structured so you can quickly adjust mappings/payloads in one place.
