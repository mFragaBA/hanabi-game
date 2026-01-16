# Hanabi Game - Improvement Tasks

## Progress Tracker

- [x] 1. Fix hardcoded SECRET_KEY (Security Critical) - DONE
- [ ] 2. Fix bug in `handle_salir_del_lobby` (Crash Bug)
- [ ] 3. Implement disconnect handling
- [ ] ~~4. Thread-safe state management~~ (SKIPPED per user request)
- [ ] 5. Fix cookie parsing error handling in frontend
- [ ] 6. Change state-modifying endpoints from GET to POST
- [ ] 7. Implement proper input validation
- [ ] 8. Fix port mismatch between Dockerfile and serve.sh
- [ ] 9. Remove placeholder/dead code
- [ ] 10. Replace print() with proper logging

---

## Item Details

### 1. Fix Hardcoded SECRET_KEY
**File**: `hanabi-sv/flask-api/main.py:10`
**Issue**: `app.config['SECRET_KEY'] = 'secret!'`
**Fix**: Load from environment variable with fallback for development

### 2. Fix Bug in handle_salir_del_lobby
**File**: `hanabi-sv/flask-api/main.py:141`
**Issue**: References undefined `session` variable instead of `data['c_id']`
**Fix**: Change `session.get('value', '')` to `data['c_id']`

### 3. Implement Disconnect Handling
**File**: `hanabi-sv/flask-api/main.py:102-117`
**Issue**: Disconnect handler is completely commented out
**Fix**: Implement proper cleanup of player state on disconnect

### 4. Thread-Safe State Management (SKIPPED)
**File**: `hanabi-sv/flask-api/main.py:89-90`
**Issue**: Global dictionaries not thread-safe
**Status**: Skipped per user request

### 5. Fix Cookie Parsing in Frontend
**File**: `hanabi-react/src/App.js:77-79`
**Issue**: Crashes if c_id cookie is missing
**Fix**: Add null check before accessing split result

### 6. Change GET to POST for State Changes
**Files**: `hanabi-sv/flask-api/main.py`, `hanabi-react/src/App.js`
**Issue**: `/crear_lobby` and `/unirse_a_lobby` use GET
**Fix**: Convert to POST with JSON body

### 7. Implement Input Validation
**File**: `hanabi-sv/flask-api/main.py`
**Issue**: No validation on player names, lobby names
**Fix**: Add length limits, character restrictions

### 8. Fix Port Mismatch
**Files**: `hanabi-sv/fly.toml`, `hanabi-sv/serve.sh`, `hanabi-sv/requirements.txt`
**Issue**: Dockerfile expects 8080, serve.sh uses 5000; gunicorn missing from requirements
**Fix**: Align ports and add gunicorn dependency

### 9. Remove Placeholder/Dead Code
**Files**: `hanabi-react/src/LobbyView.js`, `hanabi-react/src/EntranceView.js`, `hanabi-sv/flask-api/main.py`
**Issue**: Hardcoded "asd" divs, "to be implemented" stubs, commented code
**Fix**: Remove or complete the incomplete features

### 10. Replace print() with Logging
**File**: `hanabi-sv/flask-api/main.py`
**Issue**: Uses print() for debugging
**Fix**: Use Python logging module with proper levels
