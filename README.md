# VLX Fast Access

An [Alfred](https://www.alfredapp.com/) workflow for fast access to the [Visualogyx (VLX)](https://www.visualogyx.com/) API. Search, view, and interact with VLX inspections and reports directly from Alfred on macOS.

## Features

- **Search Inspections** — Instantly search your VLX inspections by name, description, or location
- **Inspection Details** — View title, description, status, location, and date
- **Generate Reports** — Call the VLX report API and open the report URL in your browser
- **Alfred Navigation** — Full menu-driven navigation with keyboard shortcuts
- **Configurable** — Set your API key and keyword in Alfred's workflow configuration

## Requirements

- [Alfred](https://www.alfredapp.com/) 4 or 5 with Powerpack
- Python 3 (macOS built-in or via Homebrew)
- A valid [VLX API key](https://developer.vlx.ai/reference/getting-started-with-your-api)

## Installation

1. Download or clone this repository
2. Double-click `VLX.alfredworkflow` (or import the `info.plist` into Alfred)
3. Open Alfred Preferences → Workflows → VLX
4. Set your **API Key** in the workflow configuration

## Configuration

| Variable       | Default                          | Description                                      |
|----------------|----------------------------------|--------------------------------------------------|
| `API_KEY`      | *(required)*                     | Your VLX API key                                 |
| `key`          | `vlx`                            | Alfred keyword to trigger the workflow           |
| `team`         | `Admin`                          | Team name                                        |
| `team_id`      | `8ea84391-dbb3-4d97-a35b-...`    | Team ID                                          |

Copy `.env.example` to `.env` and fill in your values for local development/testing:

```sh
cp .env.example .env
# Edit .env and set API_KEY=your_actual_key
```

## Usage

1. **Search Inspections**

   Type your keyword (default: `vlx`) followed by a search query:

   ```
   vlx site inspection
   ```

   Alfred will display matching inspections with status, date, location, and description.

2. **Select an Inspection**

   Press `Enter` to open the inspection actions menu, which includes:

   | Action      | Description                                 |
   |-------------|---------------------------------------------|
   | → Title     | Show the inspection title (Large Type)      |
   | → Description | Show the full description (Large Type)    |
   | → Status    | Show the inspection status (Large Type)     |
   | → Location  | Show the location (Large Type)              |
   | Report      | Generate and open the inspection report URL |
   | → Settings  | Open Alfred workflow settings               |
   | ← Go Back  | Return to the inspection search             |
   | VLX Website | Open https://app.visualogyx.com/            |

3. **Generate a Report**

   Select **Report** from the menu. Alfred calls `POST /v1/inspection/report` with the inspection ID and opens the report URL in your default browser.

## Scripts

### `inspections.py`

Script Filter that calls `GET https://api.visualogyx.com/v1/inspections?page=1&page_size=10`.

- Uses the `access-token` header for authentication
- Filters results by query (matches name, description, location)
- Outputs Alfred JSON with `id`, `title`, `status`, `date`, `location`, `description` as variables

### `get_report.py`

Run Script that calls `POST https://api.visualogyx.com/v1/inspection/report`.

- Sends `{"inspection_id": "<id>"}` in the request body
- Extracts `report_url` from the response and prints it
- The URL is then opened by Alfred's Open URL action

## Workflow Structure

```
[Keyword: vlx] → [Script Filter: inspections.py]
                          ↓
                  [List Filter: Actions Menu]
                          ↓
               [Conditional Router: {var:route}]
               ↙    ↙    ↙    ↙    ↙    ↙    ↙    ↙
          title desc status location report settings back link
            ↓    ↓      ↓       ↓       ↓      ↓      ↓    ↓
         Large  Large  Large  Large  [get_   Open   Back  Open
         Type   Type   Type   Type  report] URL    (vlx) URL
                                       ↓
                                   [Open URL]
```

## API Reference

- Base URL: `https://api.visualogyx.com/`
- API Docs: [https://developer.vlx.ai/reference/getting-started-with-your-api](https://developer.vlx.ai/reference/getting-started-with-your-api)
- Auth: `access-token` header

### Endpoints Used

| Method | Endpoint                       | Description                  |
|--------|--------------------------------|------------------------------|
| GET    | `/v1/inspections`              | List/search inspections      |
| POST   | `/v1/inspection/report`        | Generate inspection report   |

## Contributing

- Follow the structure and logic in this repository for all new features
- Use Python 3 for all scripts
- Keep all Alfred variables and connections in sync with `info.plist`
- Bundle ID: `net.cdoug.vlx`

## License

See [LICENSE](LICENSE).
