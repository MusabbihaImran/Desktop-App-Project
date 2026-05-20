# PixelAlchemy Gallery Export Microservice

A lightweight, read-only REST API microservice that exposes PixelAlchemy gallery data over HTTP. This service runs independently alongside the main Tkinter desktop application and provides standardized JSON endpoints for querying, filtering, and exporting artwork metadata and files.

---

## Overview

| Property | Value |
|----------|-------|
| **Name** | PixelAlchemy Gallery Export API |
| **Framework** | Flask 3.0+ |
| **Port** | 5050 |
| **Database** | SQLite (pixelalchemy.db) |
| **Mode** | Read-only access |
| **CORS** | Enabled for all origins |
| **Base URL** | `http://localhost:5050` |

---

## Quick Start

### 1. Install Dependencies

From the `PixelAlchemy/microservice/` directory:

```bash
pip install -r requirements_service.txt
```

**Dependencies:**
- `flask>=3.0.0` - Web framework
- `flask-cors>=4.0.0` - Cross-Origin Resource Sharing support

### 2. Start the Service

```bash
python gallery_service.py
```

You should see output like:

```
================================================================================
Starting PixelAlchemy Gallery Export API v1.0
Port: 5050
Database: ../pixelalchemy.db
Log file: ./service.log
================================================================================
 * Running on http://0.0.0.0:5050
 * Debug mode: on
```

### 3. Verify the Service

Open your browser or use curl:

```bash
curl http://localhost:5050/health
```

Expected response:
```json
{
  "status": "ok",
  "service": "PixelAlchemy Gallery Export API",
  "version": "1.0"
}
```

---

## API Endpoints

All endpoints return JSON responses with appropriate HTTP status codes.

### Health Check

#### `GET /health`
Check service status.

**Response (200):**
```json
{
  "status": "ok",
  "service": "PixelAlchemy Gallery Export API",
  "version": "1.0"
}
```

---

### Gallery Queries

#### `GET /gallery`
Retrieve all saved gallery items.

**Response (200):**
```json
{
  "count": 3,
  "items": [
    {
      "id": 1,
      "name": "Trial Artwork",
      "type": "canvas",
      "created_at": "2025-01-15 10:30:45",
      "file_path": "saved_art/trial_001.png"
    },
    {
      "id": 2,
      "name": "Sunset Filter",
      "type": "filter",
      "created_at": "2025-02-20 14:22:10",
      "file_path": "saved_art/filter_sunset.png"
    }
  ]
}
```

**Error Response (400):**
```json
{
  "error": "Database not found at ../pixelalchemy.db. Run PixelAlchemy first."
}
```

---

#### `GET /gallery/<int:item_id>`
Retrieve a single gallery item by ID.

**Example:** `GET /gallery/1`

**Response (200):**
```json
{
  "id": 1,
  "name": "Trial Artwork",
  "type": "canvas",
  "created_at": "2025-01-15 10:30:45",
  "file_path": "saved_art/trial_001.png"
}
```

**Error Response (404):**
```json
{
  "error": "Item not found"
}
```

---

#### `GET /gallery/type/<string:item_type>`
Filter gallery items by type: `canvas`, `filter`, or `pattern`.

**Example:** `GET /gallery/type/canvas`

**Response (200):**
```json
{
  "count": 2,
  "type": "canvas",
  "items": [
    {
      "id": 1,
      "name": "Trial Artwork",
      "type": "canvas",
      "created_at": "2025-01-15 10:30:45",
      "file_path": "saved_art/trial_001.png"
    }
  ]
}
```

**Error Response (400):**
```json
{
  "error": "Invalid type",
  "allowed_types": ["canvas", "filter", "pattern"]
}
```

---

### Statistics

#### `GET /gallery/stats`
Get summary statistics about the gallery.

**Response (200):**
```json
{
  "total_items": 5,
  "by_type": {
    "canvas": 2,
    "filter": 2,
    "pattern": 1
  },
  "oldest_item": "2025-01-01 09:00:00",
  "newest_item": "2025-05-15 16:45:30"
}
```

---

### Export

#### `GET /gallery/export/json`
Export full gallery metadata as a downloadable JSON file.

**Response (200):**
- Content-Type: `application/json`
- Content-Disposition: `attachment; filename=pixelalchemy_gallery_20250520_143022.json`

**JSON Content:**
```json
{
  "export_date": "2025-05-20T14:30:22.123456",
  "service": "PixelAlchemy Gallery Export API",
  "version": "1.0",
  "total_items": 3,
  "items": [...]
}
```

---

#### `GET /gallery/export/zip`
Export gallery as ZIP archive containing all image files + manifest.json.

**Response (200):**
- Content-Type: `application/zip`
- Content-Disposition: `attachment; filename=pixelalchemy_export_20250520_143022.zip`

**ZIP Contents:**
```
pixelalchemy_export.zip
├── manifest.json          # Metadata and file counts
├── trial_001.png
├── filter_sunset.png
└── pattern_waves.png
```

**Manifest Content:**
```json
{
  "export_date": "2025-05-20T14:30:22.123456",
  "service": "PixelAlchemy Gallery Export API",
  "version": "1.0",
  "total_items": 3,
  "files_included": 3,
  "files_missing": 0,
  "items": [...]
}
```

**Notes:**
- Missing image files are skipped gracefully
- A warning is logged for each missing file
- The export completes successfully even if some files are unavailable
- File count statistics are included in the manifest

---

## Error Handling

All error responses include error details and appropriate HTTP status codes.

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **200** | Success | Data returned successfully |
| **400** | Bad Request | Database not found, invalid type |
| **404** | Not Found | Gallery item doesn't exist, endpoint not found |
| **500** | Server Error | Database connection error, file system error |

### Error Response Format

```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

---

## Logging

All activities are logged to `microservice/service.log`:

```
2025-05-20 14:30:15,123 - INFO - ================================================================================
2025-05-20 14:30:15,234 - INFO - Starting PixelAlchemy Gallery Export API v1.0
2025-05-20 14:30:15,345 - INFO - Port: 5050
2025-05-20 14:30:15,456 - INFO - Database: ../pixelalchemy.db
2025-05-20 14:30:15,567 - INFO - Log file: ./service.log
2025-05-20 14:30:15,678 - INFO - ================================================================================
2025-05-20 14:30:22,234 - INFO - GET /gallery - 200 (3 items)
2025-05-20 14:30:25,345 - INFO - GET /gallery/1 - 200
2025-05-20 14:30:28,456 - INFO - GET /gallery/99 - 404 (Item 99 not found)
2025-05-20 14:30:31,567 - ERROR - Could not add file /path/to/missing.png: [Errno 2] No such file or directory
2025-05-20 14:30:35,678 - INFO - GET /gallery/export/zip - 200 (Exported 3 files, 0 missing)
```

---

## Example Usage

### Using curl

```bash
# Get all gallery items
curl http://localhost:5050/gallery

# Get item with ID 1
curl http://localhost:5050/gallery/1

# Filter by type
curl http://localhost:5050/gallery/type/canvas

# Get statistics
curl http://localhost:5050/gallery/stats

# Export as JSON (saves to file)
curl -O http://localhost:5050/gallery/export/json

# Export as ZIP (saves to file)
curl -O http://localhost:5050/gallery/export/zip
```

### Using Python requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:5050"

# Get all items
response = requests.get(f"{BASE_URL}/gallery")
data = response.json()
print(f"Found {data['count']} items")

# Get specific item
response = requests.get(f"{BASE_URL}/gallery/1")
if response.status_code == 200:
    item = response.json()
    print(f"Item: {item['name']}")
else:
    print(f"Error: {response.json()['error']}")

# Get stats
response = requests.get(f"{BASE_URL}/gallery/stats")
stats = response.json()
print(f"Total items: {stats['total_items']}")
print(f"By type: {stats['by_type']}")

# Download JSON export
response = requests.get(f"{BASE_URL}/gallery/export/json")
with open("gallery.json", "wb") as f:
    f.write(response.content)

# Download ZIP export
response = requests.get(f"{BASE_URL}/gallery/export/zip")
with open("gallery.zip", "wb") as f:
    f.write(response.content)
```

### Using JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:5050";

// Get all items
fetch(`${BASE_URL}/gallery`)
  .then(res => res.json())
  .then(data => console.log(`Found ${data.count} items`))
  .catch(err => console.error(err));

// Get specific item
fetch(`${BASE_URL}/gallery/1`)
  .then(res => res.json())
  .then(item => console.log(`Item: ${item.name}`))
  .catch(err => console.error(err));

// Get statistics
fetch(`${BASE_URL}/gallery/stats`)
  .then(res => res.json())
  .then(stats => console.log(stats))
  .catch(err => console.error(err));
```

---

## Architecture

### Database Connection
The service uses a centralized `get_db_connection()` helper function to manage SQLite connections. This approach:
- Reduces code duplication
- Ensures consistent connection handling
- Makes error management uniform
- Simplifies future refactoring

### Read-Only Access
All database operations are SELECT queries. The service **never modifies** the database:
- No INSERT operations
- No UPDATE operations
- No DELETE operations
- Safe to run alongside the desktop application

### File Handling
The ZIP export gracefully handles missing image files:
- Checks file existence before adding to ZIP
- Logs warnings for missing files
- Continues processing remaining files
- Includes file count statistics in manifest

---

## Troubleshooting

### "Database not found" error
**Problem:** The service can't find `pixelalchemy.db`

**Solution:** 
1. Make sure PixelAlchemy desktop app has been run at least once to create the database
2. Verify the database file exists at: `PixelAlchemy/pixelalchemy.db`
3. Run the service from the correct directory

### Port 5050 already in use
**Problem:** "Address already in use"

**Solution:**
```bash
# Find and kill the process using port 5050
# Windows:
netstat -ano | findstr :5050
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5050
kill -9 <PID>
```

### CORS issues from browser
**Problem:** "Cross-Origin Request Blocked"

**Solution:** The service has CORS enabled by default. If issues persist:
1. Ensure you're using the correct base URL
2. Check that the service is running
3. See the CORS headers in the response

### Export ZIP contains missing files
**Problem:** Not all image files are in the ZIP

**Solution:**
1. Check `service.log` for warnings about missing files
2. Verify file paths stored in the database are correct
3. Ensure saved_art folder is accessible

---

## Security Considerations

⚠️ **Important**: This service is designed for **development and local use only**.

- **No authentication**: All endpoints are publicly accessible
- **No rate limiting**: High-volume requests are not restricted
- **CORS enabled for all origins**: Any website can call these endpoints
- **Read-only access**: Cannot modify data, but information is exposed

**For production use:**
1. Add authentication (API keys, OAuth)
2. Implement rate limiting
3. Restrict CORS to specific origins
4. Add request validation
5. Use HTTPS/TLS encryption
6. Monitor and audit all requests

---

## Development

### Code Structure

```
gallery_service.py
├── Configuration & Setup
│   ├── Flask app initialization
│   ├── CORS setup
│   ├── Logging configuration
│   └── Database path
├── Database Helpers
│   ├── get_db_connection() - Centralized connection
│   ├── check_db_exists() - File existence check
│   └── execute_query() - Query execution with error handling
├── Endpoints
│   ├── Health Check
│   ├── Gallery Queries (4 endpoints)
│   ├── Exports (2 endpoints)
│   └── Statistics (1 endpoint)
├── Error Handlers
│   ├── 404 Handler
│   └── 500 Handler
└── Service Startup
    └── Main entry point with logging
```

### Adding New Endpoints

Template for new endpoints:

```python
@app.route('/gallery/new_endpoint', methods=['GET'])
def new_endpoint():
    """Endpoint description"""
    try:
        # Check database exists
        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"GET /gallery/new_endpoint - {db_msg}")
            logger.info(f"{request.method} {request.path} - 400")
            return jsonify({"error": db_msg}), 400
        
        # Query database
        success, data, error = execute_query("SELECT ...")
        if not success:
            logger.error(f"GET /gallery/new_endpoint - Database error: {error}")
            logger.info(f"{request.method} {request.path} - 500")
            return jsonify({"error": "Database error", "detail": error}), 500
        
        # Process and return
        logger.info(f"{request.method} {request.path} - 200")
        return jsonify(data), 200
        
    except Exception as e:
        logger.error(f"Error in new_endpoint: {str(e)}", exc_info=True)
        logger.info(f"{request.method} {request.path} - 500")
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500
```

---

## Future Enhancements

- [ ] Add search endpoint with keyword filtering
- [ ] Add pagination for large galleries
- [ ] Add image thumbnail generation
- [ ] Add authentication and API keys
- [ ] Add rate limiting
- [ ] Add metrics/monitoring dashboard
- [ ] Add database backup functionality
- [ ] Add filter for items by date range
- [ ] Add sorting options (by name, date, type)
- [ ] Add WebSocket support for real-time updates

---

## License

Part of PixelAlchemy project. See main LICENSE file for details.

---

## Support

For issues or questions:
1. Check `service.log` for error details
2. Verify database file exists and is accessible
3. Ensure Flask and Flask-CORS are properly installed
4. Check that port 5050 is available
5. Review this README for common issues

---

**Version:** 1.0  
**Last Updated:** May 20, 2026  
**Status:** Stable
