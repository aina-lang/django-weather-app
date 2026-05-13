# Django Weather App - Azure Deployment Guide

This Django-based weather application is containerized and ready for deployment to Azure using either Container Apps or App Service.

## Prerequisites

- Azure CLI installed and logged in
- Docker installed
- Azure Container Registry or Docker Hub account
- OpenWeatherMap API key

## Quick Start

1. **Clone and set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

2. **Build and test locally:**

   ```bash
   docker-compose up --build
   ```

3. **Deploy to Azure:**

   ```bash
   # For Container Apps:
   ./deploy-azure.sh

   # For App Service:
   ./deploy-azure-appservice.sh
   ```

## Environment Variables

Required environment variables (set in `.env` file):

- `SECRET_KEY`: Django secret key (generate using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (include your Azure domain)
- `OPENWEATHERMAP_API_KEY`: Your OpenWeatherMap API key

## Local Development

1. **Using Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Access at: http://localhost

2. **Native Django:**
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic
   python manage.py runserver
   ```
   Access at: http://localhost:8000

## Azure Deployment Options

### Option 1: Azure Container Apps (Recommended)

Azure Container Apps provides serverless containers with automatic scaling:

```bash
# Make script executable
chmod +x deploy-azure.sh

# Run deployment
./deploy-azure.sh
```

**Features:**

- Automatic scaling (0 to N instances)
- Built-in load balancing
- HTTPS termination
- Custom domains support
- Pay-per-use pricing

### Option 2: Azure App Service

Azure App Service provides PaaS hosting for containers:

```bash
# Make script executable
chmod +x deploy-azure-appservice.sh

# Run deployment
./deploy-azure-appservice.sh
```

**Features:**

- Always-on instances
- Integrated CI/CD
- Custom domains and SSL
- Application insights integration
- Staging slots

## Architecture

```
Internet → Azure Load Balancer → Nginx → Django (Gunicorn)
                                   ↓
                              Static Files
```

**Components:**

- **Nginx**: Reverse proxy, static file serving, SSL termination
- **Django + Gunicorn**: Python web application
- **WhiteNoise**: Backup static file serving
- **SQLite**: Database (consider upgrading to PostgreSQL for production)

## Configuration Files

- `Dockerfile`: Multi-stage build, non-root user, security best practices
- `docker-compose.yml`: Local development and testing
- `nginx/nginx.conf`: Production-ready Nginx configuration
- `.dockerignore`: Optimized Docker context
- `requirements.txt`: Python dependencies including production packages

## Security Features

- Non-root container user
- Security headers in Nginx
- Environment variable-based configuration
- Static file serving through Nginx
- HTTPS support ready
- Debug mode disabled in production

## Monitoring and Health Checks

- Health check endpoint: `/health/`
- Docker health checks configured
- Nginx access/error logs
- Django logging (configure as needed)

## Static Files

Static files are handled by:

1. **Nginx** (primary): Serves from `/static/` volume
2. **WhiteNoise** (fallback): Django middleware for static files
3. **Build time**: `collectstatic` runs during Docker build

## Database

Currently uses SQLite for simplicity. For production, consider:

```python
# settings.py - PostgreSQL example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

## Troubleshooting

### Container Issues

```bash
# Check container logs
docker-compose logs web
docker-compose logs nginx

# Check container status
docker-compose ps
```

### Azure Issues

```bash
# Check Azure Container Apps logs
az containerapp logs show --name weather-app --resource-group weather-rg

# Check App Service logs
az webapp log tail --name weather-app --resource-group weather-rg
```

### Common Issues

1. **Health check failing**: Check `/health/` endpoint accessibility
2. **Static files not loading**: Verify Nginx configuration and file paths
3. **Environment variables not set**: Check Azure app settings
4. **API key issues**: Verify OpenWeatherMap API key in environment

## Production Considerations

1. **Database**: Migrate to PostgreSQL or Azure SQL Database
2. **Redis**: Add Redis for caching and session storage
3. **CDN**: Use Azure CDN for static files
4. **SSL**: Configure custom domains with SSL certificates
5. **Monitoring**: Set up Application Insights or similar
6. **Backup**: Implement database backup strategy
7. **Scaling**: Configure auto-scaling rules

## Cost Optimization

- **Container Apps**: Pay only for what you use, scales to zero
- **App Service**: Use B1 or S1 tier for small applications
- **Storage**: Use Azure Storage for static files in large deployments
- **Monitoring**: Use built-in Azure monitoring to avoid additional costs

## Support

For issues or questions:

1. Check Azure portal for deployment status
2. Review container logs
3. Verify environment variables
4. Test locally with same configuration
