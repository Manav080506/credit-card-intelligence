# Chrome Extension Architecture

## Goals
- Capture user spend profile quickly.
- Show top 3 card recommendations with explainability.
- Sync with backend APIs securely.

## Components
- popup.html + popup.js:
  - User input UI (monthly spend, selected cards, persona).
  - Displays recommendation cards and confidence.
- content.js:
  - Optional merchant/page context extraction.
  - Lightweight and permission-scoped.
- background service worker:
  - Handles API calls, retries, and token refresh.
  - Centralizes telemetry and error handling.
- manifest.json:
  - MV3 permissions and host allowlist.

## Data Flow
1. User submits spend profile in popup.
2. Popup sends message to background worker.
3. Background calls backend /insight_v2/optimize-spend and /compare routes.
4. Background returns normalized recommendation payload.
5. Popup renders top cards, yearly reward, confidence, reason.

## Security
- Store short-lived auth token in chrome.storage.session.
- Never persist raw transaction details by default.
- Restrict host_permissions to backend domain only.
- Validate API schema at boundary.

## Reliability
- Retry policy: exponential backoff for transient 5xx.
- Circuit-breaker for repeated failures.
- Offline fallback: cached last-success response.

## Telemetry
- Track request latency and API error rate.
- Track recommendation view/click conversion events.
- Avoid collecting PII by default.

## Versioning
- Feature flag for ML ranking rollout.
- Backward-compatible API contract for popup renderer.
