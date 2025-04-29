# Hilite Webform

A web-based form for evaluating cultural relevance and text matching of images.

## Development Setup

1. Start the Flask backend:
   ```
   cd backend
   python app.py
   ```

2. Open `index.html` in a web browser or serve it using a local server.

3. Access the form with URL parameters:
   - `country`: The country to evaluate (e.g., india, brazil, japan)
   - `debug`: Set to "true" for debug mode (5 samples) or "ghost" for ghost mode (no ratings required)

Example: `http://localhost:5050/?country=india&debug=true`

## Production Setup

1. Upload the following files to your Apache server:
   - `index.prod.html` (rename to `index.html` on the server)
   - `.htaccess`
   - `backend/` directory

2. Configure Apache to proxy requests to the Flask backend:
   ```apache
   ProxyPass /submit http://localhost:5050/submit
   ProxyPassReverse /submit http://localhost:5050/submit
   ```
   
   You can add these lines to your Apache configuration file (e.g., `/etc/apache2/sites-available/000-default.conf`).

3. Set up the backend service:
   ```
   cd /path/to/hilite-webform/backend
   ./setup.sh
   ```
   
   This script will:
   - Create a virtual environment
   - Install dependencies including Gunicorn
   - Set up and start the systemd service

4. Check the service status:
   ```
   sudo systemctl status hilite-webform
   ```

5. View logs if needed:
   ```
   sudo journalctl -u hilite-webform
   ```

## Debug Modes

- **Normal Mode**: No debug parameter, shows all 110 samples
- **Debug Mode**: `debug=true`, shows only 5 samples
- **Ghost Mode**: `debug=ghost`, allows navigation without ratings (for image verification)

## Features

- Random presentation of input/output images
- Cultural relevance rating (1-5 scale)
- Text matching rating (1-5 scale)
- Auto-advance when all ratings are completed
- Progress tracking
- Completion code generation
- CSV export of ratings

## File Structure

- `index.html` / `index.prod.html`: Main webform
- `.htaccess`: Apache configuration
- `backend/`: Flask backend
  - `app.py`: Backend server
  - `hilite-webform.service`: Systemd service file
  - `apache-reverse-proxy.conf`: Apache proxy configuration
  - `setup.sh`: Setup script
  - `requirements.txt`: Python dependencies
  - `responses/`: Directory for CSV files 