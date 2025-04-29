# Hilite Webform Production Deployment Guide

This guide provides instructions for deploying the Hilite Webform to a production Apache server.

## Prerequisites

- Apache web server with mod_headers, mod_rewrite, mod_deflate, and mod_expires enabled
- Python 3.6+ for the backend server
- Access to the server's file system

## Deployment Steps

### 1. Upload Files

Upload the following files to your Apache server:
- `index.html` - The main webform
- `.htaccess` - Apache configuration
- `backend/` directory - Contains the Flask backend

### 2. Configure Apache

Ensure your Apache server has the following modules enabled:
```
a2enmod headers
a2enmod rewrite
a2enmod deflate
a2enmod expires
```

### 3. Set Up the Backend

1. Install the required Python packages:
   ```
   pip install -r backend/requirements.txt
   ```

2. Configure the backend to run as a service:
   - Create a systemd service file (e.g., `/etc/systemd/system/hilite-webform.service`)
   - Example service configuration:
     ```
     [Unit]
     Description=Hilite Webform Backend
     After=network.target

     [Service]
     User=www-data
     WorkingDirectory=/path/to/hilite-webform/backend
     ExecStart=/usr/bin/python3 app.py
     Restart=always

     [Install]
     WantedBy=multi-user.target
     ```

3. Start the service:
   ```
   sudo systemctl enable hilite-webform
   sudo systemctl start hilite-webform
   ```

### 4. Configure Apache Virtual Host

Add the following to your Apache virtual host configuration:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/hilite-webform

    # Proxy requests to the backend
    ProxyPass /submit http://localhost:5050/submit
    ProxyPassReverse /submit http://localhost:5050/submit

    # Enable .htaccess
    <Directory /path/to/hilite-webform>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

### 5. Test the Deployment

1. Access the webform at `http://your-domain.com/`
2. Test the form submission
3. Verify that the CSV files are being saved correctly

## Troubleshooting

- **CORS Issues**: Ensure the Apache headers module is enabled and the .htaccess file is being read
- **Backend Connection**: Check that the backend service is running and accessible
- **File Permissions**: Ensure the backend has write permissions to the directory where CSV files are saved

## Security Considerations

- Consider adding HTTPS using Let's Encrypt
- Restrict access to the backend API if needed
- Regularly update dependencies to address security vulnerabilities 