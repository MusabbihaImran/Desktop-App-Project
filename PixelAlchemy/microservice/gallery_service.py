"""
PixelAlchemy Gallery Export Microservice
A standalone Flask REST API for exporting and querying PixelAlchemy gallery data
Port: 5050
Database: Read-only access to pixelalchemy.db
"""

import logging
import sqlite3
import json
import os
import sys
import zipfile
from datetime import datetime
from io import BytesIO
from pathlib import Path

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS

# ============================================================================
# CONFIGURATION
# ============================================================================

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Set up logging to microservice/service.log and stderr
log_file = os.path.join(os.path.dirname(__file__), 'service.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Database path (relative to microservice folder: ../pixelalchemy.db)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'pixelalchemy.db')

SERVICE_NAME = "PixelAlchemy Gallery Export API"
SERVICE_VERSION = "1.0"
SERVICE_PORT = 5050

# ============================================================================
# REFACTORING SCHEME & HELPERS
# ============================================================================

# LEGACY CODE (before refactor)
# Original pattern - database connection repeated in every route:
#
# @app.route('/gallery', methods=['GET'])
# def get_gallery():
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM artworks")
#         rows = cursor.fetchall()
#         conn.close()
#         return jsonify([dict(row) for row in rows])
#     except sqlite3.DatabaseError as e:
#         return jsonify({"error": "Database error", "detail": str(e)}), 500
#
# @app.route('/gallery/<int:item_id>', methods=['GET'])
# def get_gallery_item(item_id):
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM artworks WHERE id = ?", (item_id,))
#         row = cursor.fetchone()
#         conn.close()
#         if not row:
#             return jsonify({"error": "Not found"}), 404
#         return jsonify(dict(row))
#     except sqlite3.DatabaseError as e:
#         return jsonify({"error": "Database error", "detail": str(e)}), 500

# REFACTORED CODE
def get_db_connection():
    """
    Create and return a database connection with Row factory.
    Centralizes connection logic to reduce code duplication and enforce consistency.
    Returns: sqlite3.Connection object with row_factory set
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def check_db_exists():
    """
    Check if the SQLite database file exists.
    Returns: (bool, str) - (exists, error_message_or_success_message)
    """
    if not os.path.exists(DB_PATH):
        return False, "Database not found. Run PixelAlchemy first."
    return True, "Database found"


def get_file_created_at(file_path):
    """
    Helper to extract the file creation/modification time on disk if it exists,
    providing a fallback value if missing.
    Returns: YYYY-MM-DD HH:MM:SS format
    """
    if not file_path:
        return "2026-05-20 11:00:00"
    
    resolved_path = None
    paths_to_check = [
        os.path.join(os.path.dirname(__file__), '..', '..', file_path),
        os.path.join(os.path.dirname(__file__), '..', file_path),
        file_path
    ]
    for p in paths_to_check:
        if os.path.exists(p):
            resolved_path = p
            break
            
    if resolved_path:
        try:
            mtime = os.path.getmtime(resolved_path)
            return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
    return "2026-05-20 11:00:00"

# ============================================================================
# LOGGING MIDDLEWARE
# ============================================================================

@app.after_request
def log_request(response):
    """
    Automatically log details for every incoming request, including
    method, request path, and returned HTTP status code.
    """
    logger.info(f"{request.method} {request.path} - {response.status_code}")
    return response

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """
    Returns service health status and metadata.
    """
    try:
        return jsonify({
            "status": "ok",
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION
        }), 200
    except Exception as e:
        logger.error(f"Error in /health endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Health check failed",
            "detail": str(e)
        }), 500


@app.route('/gallery', methods=['GET'])
def get_gallery():
    """
    Retrieves all saved items from the artworks table.
    Transforms data to match the requested API response schema.
    """
    try:
        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"Database missing on GET /gallery: {db_msg}")
            return jsonify({"error": db_msg}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artworks ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append({
                "id": row["id"],
                "name": row["title"],
                "type": row["type"],
                "created_at": get_file_created_at(row["image_path"]),
                "file_path": row["image_path"]
            })

        return jsonify({
            "count": len(items),
            "items": items
        }), 200

    except sqlite3.DatabaseError as e:
        logger.error(f"Database error in get_gallery: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_gallery: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "detail": str(e)
        }), 500


@app.route('/gallery/<int:item_id>', methods=['GET'])
def get_gallery_item(item_id):
    """
    Retrieves a single gallery item by its database ID.
    """
    try:
        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"Database missing on GET /gallery/{item_id}: {db_msg}")
            return jsonify({"error": db_msg}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artworks WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({"error": "Item not found"}), 404

        item = {
            "id": row["id"],
            "name": row["title"],
            "type": row["type"],
            "created_at": get_file_created_at(row["image_path"]),
            "file_path": row["image_path"]
        }
        return jsonify(item), 200

    except sqlite3.DatabaseError as e:
        logger.error(f"Database error in get_gallery_item for ID {item_id}: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_gallery_item for ID {item_id}: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "detail": str(e)
        }), 500


@app.route('/gallery/type/<string:item_type>', methods=['GET'])
def get_gallery_by_type(item_type):
    """
    Filters gallery items by type: canvas, filter, or pattern.
    """
    try:
        # REVIEW: Musabbiha - Enforce validation of the requested item_type
        # to ensure it strictly belongs to the supported set of types.
        allowed_types = ['canvas', 'filter', 'pattern']
        normalized_type = item_type.lower()
        if normalized_type not in allowed_types:
            logger.warning(f"Invalid type requested: {item_type}")
            return jsonify({
                "error": "Invalid type",
                "allowed_types": allowed_types
            }), 400

        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"Database missing on GET /gallery/type/{item_type}: {db_msg}")
            return jsonify({"error": db_msg}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artworks WHERE type = ? ORDER BY id DESC", (normalized_type,))
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append({
                "id": row["id"],
                "name": row["title"],
                "type": row["type"],
                "created_at": get_file_created_at(row["image_path"]),
                "file_path": row["image_path"]
            })

        return jsonify({
            "count": len(items),
            "items": items
        }), 200

    except sqlite3.DatabaseError as e:
        logger.error(f"Database error in get_gallery_by_type ({item_type}): {str(e)}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_gallery_by_type ({item_type}): {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "detail": str(e)
        }), 500


@app.route('/gallery/export/json', methods=['GET'])
def export_json():
    """
    Exports full gallery metadata as a downloadable .json file attachment.
    """
    try:
        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"Database missing on GET /gallery/export/json: {db_msg}")
            return jsonify({"error": db_msg}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artworks ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append({
                "id": row["id"],
                "name": row["title"],
                "type": row["type"],
                "created_at": get_file_created_at(row["image_path"]),
                "file_path": row["image_path"]
            })

        export_data = {
            "count": len(items),
            "items": items
        }

        # Format output cleanly with indentation
        json_str = json.dumps(export_data, indent=2)
        json_bytes = BytesIO(json_str.encode('utf-8'))

        return send_file(
            json_bytes,
            mimetype='application/json',
            as_attachment=True,
            download_name='pixelalchemy_gallery.json'
        ), 200

    except sqlite3.DatabaseError as e:
        logger.error(f"Database error in export_json: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in export_json: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Export failed",
            "detail": str(e)
        }), 500


@app.route('/gallery/export/zip', methods=['GET'])
def export_zip():
    """
    Packages all saved image files and a metadata manifest.json into a ZIP archive.
    Gracefully handles and logs missing files without crashing.
    """
    try:
        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"Database missing on GET /gallery/export/zip: {db_msg}")
            return jsonify({"error": db_msg}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artworks ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        items = []
        for row in rows:
            items.append({
                "id": row["id"],
                "name": row["title"],
                "type": row["type"],
                "created_at": get_file_created_at(row["image_path"]),
                "file_path": row["image_path"]
            })

        zip_buffer = BytesIO()
        files_included = 0
        files_missing = 0

        # Build ZIP archive in memory
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for item in items:
                file_path = item.get('file_path')
                if not file_path:
                    logger.warning(f"Warning: Item ID {item['id']} lacks a file path.")
                    files_missing += 1
                    continue
                
                # Check multiple resolution paths
                resolved_path = None
                paths_to_check = [
                    os.path.join(os.path.dirname(__file__), '..', '..', file_path),
                    os.path.join(os.path.dirname(__file__), '..', file_path),
                    file_path
                ]
                for p in paths_to_check:
                    if os.path.exists(p):
                        resolved_path = p
                        break

                if resolved_path:
                    try:
                        # Write the image file into the zip root
                        arcname = os.path.basename(resolved_path)
                        zip_file.write(resolved_path, arcname=arcname)
                        files_included += 1
                    except (OSError, FileNotFoundError) as e:
                        # Log error and skip file gracefully
                        logger.error(f"File error loading {resolved_path} for ZIP export: {str(e)}")
                        files_missing += 1
                else:
                    logger.warning(f"File not found on disk: {file_path} for item ID {item['id']}")
                    files_missing += 1

            # REVIEW: Musabbiha - Include detailed metadata statistics in the ZIP manifest
            # to verify integrity on retrieval.
            manifest = {
                "export_date": datetime.now().isoformat(),
                "service": SERVICE_NAME,
                "version": SERVICE_VERSION,
                "total_items": len(items),
                "items": items,
                "files_included": files_included,
                "files_missing": files_missing
            }
            manifest_json = json.dumps(manifest, indent=2)
            zip_file.writestr('manifest.json', manifest_json)

        zip_buffer.seek(0)
        logger.info(f"ZIP package generated. Included: {files_included}, Missing: {files_missing}")

        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='pixelalchemy_export.zip'
        ), 200

    except sqlite3.DatabaseError as e:
        logger.error(f"Database error in export_zip: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500
    except (FileNotFoundError, OSError) as e:
        logger.error(f"File handling exception in export_zip: {str(e)}", exc_info=True)
        return jsonify({
            "error": "File system error",
            "detail": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in export_zip: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Export failed",
            "detail": str(e)
        }), 500


@app.route('/gallery/stats', methods=['GET'])
def get_stats():
    """
    Returns summary statistics for items in the gallery.
    """
    try:
        db_exists, db_msg = check_db_exists()
        if not db_exists:
            logger.warning(f"Database missing on GET /gallery/stats: {db_msg}")
            return jsonify({"error": db_msg}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM artworks ORDER BY id ASC")
        rows = cursor.fetchall()
        conn.close()

        total_items = len(rows)
        by_type = {}
        dates = []

        for row in rows:
            item_type = row["type"]
            by_type[item_type] = by_type.get(item_type, 0) + 1
            
            created_at = get_file_created_at(row["image_path"])
            if created_at:
                dates.append(created_at[:10])  # YYYY-MM-DD format

        oldest_item = None
        newest_item = None
        if dates:
            dates.sort()
            oldest_item = dates[0]
            newest_item = dates[-1]

        return jsonify({
            "total_items": total_items,
            "by_type": by_type,
            "oldest_item": oldest_item,
            "newest_item": newest_item
        }), 200

    except sqlite3.DatabaseError as e:
        logger.error(f"Database error in get_stats: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Database error",
            "detail": str(e)
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_stats: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal server error",
            "detail": str(e)
        }), 500

# ============================================================================
# SERVICE STARTUP
# ============================================================================

if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}")
    logger.info(f"Port: {SERVICE_PORT}")
    logger.info(f"Database: {DB_PATH}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 80)
    
    app.run(debug=True, port=SERVICE_PORT, host='0.0.0.0')
