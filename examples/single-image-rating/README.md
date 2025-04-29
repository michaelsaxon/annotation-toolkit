# Image Rating Webform

A web application for collecting image ratings with a Flask backend and static HTML frontend.

## Project Structure

```
Webform/
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ └── data/
├── index.html # Development version
├── index.prod.html # Production version
└── README.md
```
## Local Development Setup

1. Clone the repository and set up the environment:

```bash
git clone <repository-url>
cd Webform/backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create data directory for storing results:

```bash
mkdir -p data
chmod -R 777 data
```

3. Run the Flask application:

```bash
python app.py
```

4. In another terminal, serve the frontend:

```bash
python -m http.server 8080
```

5. Open your browser and navigate to http://localhost:8080.

I'll add the Apache hosting section to the README.md. I'll use indentation for code blocks instead of backticks:

## Production Deployment with Apache

### 1. Install Required Packages

First, install Apache and required Python packages:
```bash
sudo apt-get update
sudo apt-get install apache2
pip install gunicorn
```

### 2. Set Up the Flask Backend Service

1. Create a systemd service file at /etc/systemd/system/webform.service:

```bash
[Unit]
Description=Webform Flask Application
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/Webform/backend
Environment="PATH=/path/to/your/venv/bin"
ExecStart=/path/to/your/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

2. Start and enable the service:

```bash
sudo systemctl start webform
sudo systemctl enable webform
sudo systemctl status webform
```

### 3. Configure Apache Reverse Proxy

1. Enable required Apache modules:

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
```

2. Add the following configuration to /etc/apache2/sites-available/000-default.conf:

```apache
<VirtualHost *:80>
    # ... existing config ...

    # Proxy settings for Flask backend
    ProxyPass /api/submit http://localhost:5000/submit
    ProxyPassReverse /api/submit http://localhost:5000/submit

    # ... rest of existing config ...
</VirtualHost>
```

3. Restart Apache:

```bash
sudo systemctl restart apache2
```

### 4. Deploy Frontend Files

1. Copy the production frontend and prompt data files:

```bash
sudo mkdir -p /var/www/html/webform
sudo cp index.prod.html /var/www/html/webform/index.html
sudo cp prompts* /var/www/html/webform/
```

2. Set proper permissions:

```bash
sudo chown -R www-data:www-data /var/www/html/webform
sudo chmod -R 755 /var/www/html/webform
```

### 5. Testing the Deployment

1. Check the Flask service status:

```bash
sudo systemctl status webform
```

2. Check Apache status:

```bash
sudo systemctl status apache2
```

3. View logs if needed:

```bash
sudo journalctl -u webform  # Flask logs
sudo tail -f /var/log/apache2/error.log  # Apache error logs
```

4. Access your form:

```bash
http://your-server-name/webform/?source=retrieved_images&start_x=0&end_x=19&ext=jpg
```

### 6. Troubleshooting

1. If the form doesn't submit, check:
   - Flask service is running
   - Apache proxy configuration is correct
   - Permissions on the data directory

2. Common fixes:
   - Restart services:

```bash
sudo systemctl restart webform
sudo systemctl restart apache2
```

   - Check data directory permissions:

```bash
sudo chown -R www-data:www-data /path/to/Webform/backend/data
sudo chmod -R 777 /path/to/Webform/backend/data
```

   - Check Apache error logs:

```bash
sudo tail -f /var/log/apache2/error.log
```

### 7. Security Considerations

1. The data directory needs to be writable by the web server:
   - Use appropriate permissions (777 is permissive for testing)
   - Consider more restrictive permissions for production

2. The Flask service runs on localhost only (127.0.0.1)
   - Only accessible through Apache proxy
   - No direct external access to port 5000

3. Apache handles all external connections
   - Standard HTTP/HTTPS ports (80/443)
   - No additional ports need to be opened in firewall

