# CouchDB Monitoring Plugin - Audit & Optimization Report (v5)

## Overview
This version of the plugin was optimized for **CouchDB 3.3.3+**. The original basic plugin contained legacy logic that caused several metrics to remain at zero or throw errors.

## Key Changes Made:

### 1. Endpoint Modernization
- **Change:** Removed trial-and-error fallback for the legacy `/_stats` endpoint.
- **Why:** CouchDB 3.3.3+ exclusively uses `/_node/_local/_stats`. The legacy endpoint caused unnecessary `404` errors in the logs.

### 2. Metric Mapping Fixes (Fixed "0" Values)
- **Issue:** The original script looked for `document_inserts` and `local_document_writes` inside a non-existent nested `couchdb` sub-folder in the JSON.
- **Change:** Updated logic to read these metrics directly from the root `stats` JSON object.
- **Result:** These metrics now correctly reflect real-time database activity instead of showing a flat `0`.

### 3. Modern Authentication Mapping
- **Issue:** `auth_cache_hits` and `auth_cache_misses` return `0` in modern CouchDB (they are legacy).
- **Change:** Added a fallback mechanism that maps modern authentication security metrics (`password_hashing_fast` and `password_hashing_slow`) to the dashboard auth fields.
- **Result:** The Auth graphs on the dashboard now correctly track successful and failed login attempts.

### 4. Stability & Robustness
- **Change:** Replaced fragile nested `if/else` structures with Python's `.get()` default method.
- **Why:** Prevented the plugin from crashing entirely if CouchDB returns a partial JSON response or if a specific metric key is missing.

---

