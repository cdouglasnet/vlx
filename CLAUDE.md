# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Alfred workflow for Visualogyx (VLX) integration, allowing users to quickly search inspections, view details, and generate reports from VLX directly within Alfred. The workflow is written in Python 3 and uses only the standard library (no external dependencies).

**IMPORTANT**: This workflow is designed for public distribution. It must NOT contain any hardcoded API keys, credentials, or personal data. All sensitive information must be stored in Alfred's workflow environment variables.

## Key Architecture Components

### Main Entry Points
- `inspections.py` - Script Filter that searches VLX inspections via the API (`vlx` command)
- `get_report.py` - Run Script that generates and retrieves inspection report URLs
- `config.py` - Configuration management interface (`vlx:config` command)
- `configStore.py` - Stores configuration values in macOS Keychain or workflow settings

### Core Dependencies
- `workflow/` - Alfred-Workflow library for Alfred integration and Keychain support
  - `workflow.py` - Main Workflow class with password/keychain methods
  - `web.py` - HTTP utilities
  - `util.py` - Utility functions (LockFile, atomic_writer, etc.)

### Core Features
- **Secure API Key Storage**: API keys stored in macOS Keychain (not environment variables)
- **Zero External Dependencies**: Uses only Python 3 standard library (`urllib`, `json`, `os`, `sys`)
- **Menu Navigation**: List Filter provides inspection action menu
- **Report Generation**: Direct integration with VLX report API

### Configuration Storage
- **API keys stored in macOS Keychain** for security using `wf.save_password('vlxAPI', key)`
- **Fallback to environment variables** (`API_KEY`) for backwards compatibility
- Other settings stored in Alfred workflow settings via `wf.settings`
- Configuration accessed via `vlx:config` command

### Security Requirements
- **NEVER hardcode API keys or credentials in source code**
- **ALWAYS store API keys in macOS Keychain** using `wf.save_password()`
- **ALWAYS mask sensitive data when displaying in UI** (show only partial values)
- **This is redistributable software** - assume all code will be public

## Common Development Tasks

### Testing the Workflow
To test the workflow:
1. Build with `./build.sh` to create `VLX.alfredworkflow`
2. Install in Alfred by double-clicking the `.alfredworkflow` file
3. Configure API key using `vlx:config` command (stores securely in Keychain)
4. Test search with `vlx <search term>`
5. Test report generation by selecting an inspection and choosing "Report"

### API Key Configuration
The API key is stored securely in macOS Keychain:
```python
from workflow import Workflow, PasswordNotFound

wf = Workflow()
# Save API key
wf.save_password('vlxAPI', 'your_api_key')
# Get API key
api_key = wf.get_password('vlxAPI')
# Delete API key
wf.delete_password('vlxAPI')
```

### Local Testing (Development)
For testing scripts locally without Alfred:
1. Copy `.env.example` to `.env`
2. Add your `API_KEY=your_actual_key` to `.env`
3. Source the environment: `source .env`
4. Run scripts directly: `python3 inspections.py "search term"`

### Debugging
- Use `sys.stderr.write()` for error messages (visible in Alfred's debug console)
- Enable Alfred's debug mode: Alfred Preferences → Workflows → [workflow icon] → Debug
- Test API calls with `curl`:
  ```bash
  curl -H "access-token: YOUR_KEY" \
       "https://api.visualogyx.com/v1/inspections?page=1&page_size=10"
  ```

### API Integration
The VLX API v1 endpoints used:
- `GET /v1/inspections` - Retrieve inspections (paginated)
  - Query params: `page`, `page_size`
  - Headers: `access-token`, `Content-Type: application/json`
- `POST /v1/inspection/report` - Generate inspection report
  - Body: `{"inspection_id": "<id>"}`
  - Returns: `{"report_url": "https://..."}`
  - Headers: `access-token`, `Content-Type: application/json`

API Documentation: https://developer.vlx.ai/reference/getting-started-with-your-api

### Python 3 Standard Library Implementation
This project intentionally uses NO external dependencies:
- `urllib.request` - HTTP requests (instead of `requests`)
- `urllib.parse` - URL encoding/parsing
- `urllib.error` - HTTP error handling
- `json` - JSON parsing and formatting
- `os` - Environment variable access
- `sys` - Command line arguments and stderr

**Why?** This ensures the workflow runs on any macOS system with Python 3 without requiring pip installations or virtual environments.

## Critical Lessons Learned

### Successful Workflow Build Process
1. **Use the build script**: `./build.sh`
2. **Verify the build**: `unzip -t VLX.alfredworkflow`
3. **Check structure**: `unzip -l VLX.alfredworkflow | head`
4. **Install with Alfred**: Double-click or `open VLX.alfredworkflow`
5. **Test configuration**: Try `vlx` command to ensure no import errors

### Workflow Packaging and Testing
**IMPORTANT**: When building/modifying the workflow, always test the actual `.alfredworkflow` file installation, not just local Python execution. Issues that work locally may fail in Alfred due to:
- Python environment differences (system Python vs Homebrew Python)
- Working directory differences
- Environment variable availability
- File permissions

### Known Issues and Fixes

#### 1. Missing API Key Error
- **Issue**: Workflow shows "API Key not configured"
- **Fix**: Use `vlx:config` to set your API key (stored securely in Keychain)
- **Alternative**: Set `API_KEY` environment variable for backwards compatibility
- **Why**: API keys are now stored in macOS Keychain for security

#### 2. Empty Results or API Errors
- **Issue**: "No inspections found" or HTTP 401/403 errors
- **Fix**: Verify API key is valid and has correct permissions
- **Debug**: Check Alfred's debug console for detailed error messages
- **Why**: VLX API requires valid access token in headers

#### 3. UTF-8 Encoding Issues
- **Issue**: Special characters in inspection names/descriptions cause errors
- **Fix**: Use `.encode("utf-8")` for POST data, `.decode("utf-8")` for responses
- **Why**: HTTP requires byte strings, JSON requires Unicode strings

#### 4. Report URL Not Opening
- **Issue**: Report generation succeeds but URL doesn't open
- **Fix**: Ensure `get_report.py` prints the URL to stdout (not stderr)
- **Why**: Alfred's "Open URL" action reads from stdout

### Building and Packaging

#### Build Script (`build.sh`)
```bash
#!/bin/bash
# Critical: Preserve directory structure for List Filter Images!
rsync -a --exclude='.DS_Store' "List Filter Images/" "$BUILD_DIR/List Filter Images/"

# CRITICAL: Zip files at root level!
cd "$BUILD_DIR"
zip -r "$OLDPWD/$WORKFLOW_NAME.alfredworkflow" .
# NOT: zip -r name.alfredworkflow foldername/
```

#### Common Packaging Mistakes
1. **DON'T** include `.git`, `.DS_Store`, `.env`, or `__pycache__` files
2. **DON'T** create workflow with files in a subfolder - Alfred expects files at root
3. **DON'T** hardcode API keys or sensitive data in scripts
4. **DO** test the packaged workflow file, not just local execution
5. **DO** verify zip structure with `unzip -l VLX.alfredworkflow | head`
6. **DO** preserve directory structure for `List Filter Images/`

### Debugging Import/Installation Errors

#### "The workflow you are trying to import is invalid"
When Alfred shows this error:

1. **Check zip structure** (MOST COMMON ISSUE):
   ```bash
   unzip -l VLX.alfredworkflow | head
   # Files should be at root: info.plist, inspections.py, icon.png, etc.
   # NOT: VLX/info.plist, VLX/inspections.py
   ```

2. **Verify info.plist**:
   ```bash
   plutil -lint info.plist  # Should output "OK"
   ```

3. **Check for Python syntax errors**:
   ```bash
   python3 -m py_compile inspections.py
   python3 -m py_compile get_report.py
   ```

4. **Test scripts directly**:
   ```bash
   export API_KEY="your_test_key"
   python3 inspections.py "test"
   ```

#### HTTP/API Errors
- **401 Unauthorized**: API key is invalid or missing
- **403 Forbidden**: API key lacks necessary permissions
- **404 Not Found**: Endpoint URL is incorrect
- **500 Server Error**: VLX API issue (check status page)

### API Response Handling
The VLX API returns inspection data in various formats. Handle both:
```python
# API may return array directly or wrapped in object
inspections = data if isinstance(data, list) else \
              data.get("inspections", data.get("data", []))
```

Inspection fields may vary:
- ID: `id` (always present)
- Name: `name` or `title`
- Location: `location` or `address`
- Inspector: `created_by` (may be string or dict with `name`/`email`)
- Date: `created_at` or `date` (ISO format: `2024-03-06T12:30:00Z`)

### Best Practices
1. **Incremental Changes**: Make one fix at a time and test
2. **Preserve Working State**: Keep a known-working `.alfredworkflow` file
3. **Test Installation**: Always test by installing the workflow, not just running locally
4. **Error Handling**: Always catch `urllib.error.HTTPError` and general `Exception`
5. **User Feedback**: Provide clear error messages in Alfred's result items
6. **Environment Variables**: Never hardcode API keys; always use `os.environ.get()`

### Testing Checklist
Before committing changes:
- [ ] Build succeeds: `./build.sh`
- [ ] Zip structure is correct: `unzip -l VLX.alfredworkflow | head`
- [ ] Workflow installs in Alfred without errors
- [ ] Search works: `vlx test`
- [ ] Report generation works
- [ ] No API keys in source code
- [ ] All scripts have proper error handling
- [ ] UTF-8 encoding handled correctly

## Project Information
- **Bundle ID**: net.cdoug.vlx
- **Version**: Extracted from info.plist
- **Python Version**: Python 3.x (system Python on macOS)
- **Dependencies**: None (standard library only)
- **Alfred Version**: 4 or 5 with Powerpack
- **API Documentation**: https://developer.vlx.ai/reference/getting-started-with-your-api
- **VLX Website**: https://www.visualogyx.com/

## File Structure
```
vlx/
├── inspections.py        # Script Filter: Search inspections
├── get_report.py         # Run Script: Generate report URL
├── config.py             # Script Filter: Configuration menu
├── configStore.py        # Run Script: Store configuration values
├── info.plist            # Alfred workflow configuration
├── icon.png              # Workflow icon
├── LICENSE               # GPL v2.0
├── README.md             # User documentation
├── build.sh              # Build script
├── .env.example          # Environment template
├── .gitignore            # Git ignore patterns
├── workflow/             # Alfred-Workflow library
│   ├── __init__.py       # Package exports
│   ├── workflow.py       # Main Workflow class (Keychain support)
│   ├── web.py            # HTTP utilities
│   └── util.py           # Utility functions
└── List Filter Images/   # Menu icons
    ├── back.png
    ├── email.png
    ├── icon.png
    ├── link.png
    ├── question.png
    ├── rbang.png
    ├── send.png
    ├── settings.png
    ├── star.png
    ├── starblue.png
    ├── stargreen.png
    ├── starorange.png
    ├── starpurple.png
    ├── starred.png
    └── ybang.png
```

## Setting Up vlx:config Command in Alfred
To enable the `vlx:config` command for API key configuration:

1. Open Alfred Preferences → Workflows → VLX Fast Access
2. Add a new Keyword Input:
   - Keyword: `vlx:config`
   - Title: "VLX Configuration"
   - Argument: Optional (with space)
3. Add a Script Filter connected to the keyword:
   - Language: /usr/bin/python3
   - Script: `python3 config.py "{query}"`
   - Script Filter should output Alfred JSON
4. Add a Run Script connected to the Script Filter:
   - Language: /usr/bin/python3
   - Script: `python3 configStore.py "{query}"`
   - This handles saving to Keychain

## Workflow Flow
```
User types "vlx <query>"
    ↓
inspections.py (Script Filter)
    ↓ API GET /v1/inspections
    ↓
Alfred displays results
    ↓ User selects inspection
    ↓
List Filter (Action Menu)
    - → Title (Large Type)
    - → Description (Large Type)
    - → Status (Large Type)
    - → Location (Large Type)
    - Report (generates URL)
    - → Settings
    - ← Go Back
    - VLX Website
    ↓ User selects action
    ↓
Conditional Router → Appropriate action
    ↓ (if Report selected)
    ↓
get_report.py (Run Script)
    ↓ API POST /v1/inspection/report
    ↓ Returns report_url
    ↓
Open URL in browser
```

## Future Enhancements
- Pagination support for large inspection lists
- Filtering by status, date range, location
- Create/edit inspections directly from Alfred
- Cache recent inspections for offline access
- Add fuzzy matching for better search results
- Support multiple VLX teams/organizations

