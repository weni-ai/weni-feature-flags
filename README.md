# Weni Feature Flags
**Weni feature flags SDK for Python backends**

## What is it
Weni Feature Flags is a Python Library that functions as an abstraction layer between Django projects and [GrowthBook](https://www.growthbook.io/).

## Requirements
- **Python**: 3.8+
- **Django**: 3.2.22+
- **Django REST Framework**: 3.12.0+
- **Celery**: 5.0+

This project also relies on **Celery** to update feature flags asynchronously.
This library uses Django's cache abstraction to avoid hitting the database constantly and also reduce latency.

## Installation
To install it, you can use both pip or Poetry.

### Using PIP
```bash
pip install weni-feature-flags
```

### Using Poetry
```bash
poetry add weni-feature-flags
```

## Initial configuration

On your Django project, you should add "weni_feature_flags" to INSTALLED_APPS.
When testing and deploying you should apply the migrations using:

```bash
python manage.py migrate
```

This library saves a snapshot of the feature flags on your database and cache layer to be resilient
to eventual GrowthBook unavailability.

## Quick Start

Here's a minimal example to get you started:

1. **Install the package**:
```bash
pip install weni-feature-flags
```

2. **Add to Django settings**:
```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'weni_feature_flags',
]

# Environment variables
GROWTHBOOK_CLIENT_KEY = "your-client-key"
GROWTHBOOK_HOST_BASE_URL = "https://your-growthbook-instance.com"
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Use in your code**:
```python
from weni_feature_flags.shortcuts import is_feature_active

# Check if a feature is active for a user
if is_feature_active("new-dashboard", "user@example.com", "project-uuid"):
    # Show new dashboard
    pass
```

## SDK Connection

On GrowthBook, you can create a Python SDK connection, which you generate your client key.
You should save this client key and use it as the GROWTHBOOK_CLIENT_KEY environment variable,
as well as your GrowthBook host to GROWTHBOOK_HOST_BASE_URL.

Remember to select the correct environment and project on the "New SDK Connection" modal.

## Webhooks

You can also configure webhooks to apply feature flags changes faster. For this,
first import the webhook view and configure it in your Django project's URLs

```python
from django.urls import path
from weni_feature_flags.views import FeatureFlagsWebhookView

urlpatterns = [
    path('webhooks/feature-flags/', FeatureFlagsWebhookView.as_view(), name='feature-flags-webhook'),
]
```

Then, create a strong secret and save it to GROWTHBOOK_WEBHOOK_SECRET.

On Growthbook, access **Settings -> Webhooks** and create a new event webhook. It should be configured to use POST as the method and, on the **Headers (JSON)** section, include the secret that you created:

```json
{
    "secret": "<YOUR SECRET HERE>"
}
```

You should select the events "feature.created", "feature.updated" and "feature.deleted" and select your environment and project.

## Usage

### Using the Service Class
You can import and use the whole feature flags service like this:
```python
from weni_feature_flags.services import FeatureFlagsService

service = FeatureFlagsService()

# Get all feature flags data
features = service.get_features()

# Get active feature flags for specific attributes
active_features = service.get_active_feature_flags_for_attributes({
    "userEmail": "user@example.com",
    "projectUUID": "8065619a-2b22-4351-9914-e37c6394b1d3"
})

# Evaluate a specific feature flag by attributes
is_active = service.evaluate_feature_flag_by_attributes(
    "feature-key", 
    {
        "userEmail": "user@example.com",
        "projectUUID": "8065619a-2b22-4351-9914-e37c6394b1d3"
    }
)
```

### Using Shortcuts
If you only really need to check whether a user and project have access to a feature, you can use shortcuts:

```python
from weni_feature_flags.shortcuts import is_feature_active, is_feature_active_for_attributes
```

### Using Shortcuts
If you want to check if a certain user in a certain project has access to a feature, you can use

```python
# feature key/name, user's email, project's UUID
if is_feature_active("featureKey", "user@email.com", "8065619a-2b22-4351-9914-e37c6394b1d3"):
    # Something cool happens
```

Or, if you set the feature up in a different way, you can pass the attributes directly using:
```python
# Just checks the project

# feature key/name, attributes
if is_feature_active_for_attributes("featureKey", {"projectUUID": "8065619a-2b22-4351-9914-e37c6394b1d3"}):
    pass

# Just checks the user's email
if is_feature_active_for_attributes("featureKey", {"userEmail": "user@email.com"}):
    pass

# Or any other rule that you have defined on GrowthBook
if is_feature_active_for_attributes("featureKey", {"example": "test"}):
    pass
```

## Technical Details

### Database Models
This library creates the following database models:
- **FeatureFlag**: Stores feature flag definitions and their current state
- **FeatureFlagSnapshot**: Maintains historical snapshots of feature flags for resilience

### Caching Strategy
- Feature flags are cached using Django's cache framework
- Cache keys are prefixed with `CACHE_KEY_PREFIX` (default: "weni_feature_flags")
- Cache TTL is configurable via `FEATURES_CACHE_TTL` (default: 60 seconds)
- When GrowthBook is unavailable, the library falls back to cached data

## Troubleshooting

### Common Issues

**Feature flags not updating**
- Check if Celery is running and processing tasks
- Verify webhook configuration and secret
- Check GrowthBook connection settings

**GrowthBook connection errors**
- Verify `GROWTHBOOK_CLIENT_KEY` and `GROWTHBOOK_HOST_BASE_URL`
- Check network connectivity to GrowthBook
- Review timeout settings (`GROWTHBOOK_REQUESTS_TIMEOUT`)

**Cache issues**
- Ensure that you have a caching backend, such as Redis, configured

**Webhook not working**
- Verify webhook URL is accessible
- Check `GROWTHBOOK_WEBHOOK_SECRET` matches GrowthBook configuration
- Review webhook event selection in GrowthBook

## All environment variables
<table>
    <tr>
        <th>Variable</th>
        <th>Required</th>
        <th>Default</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><code>GROWTHBOOK_CLIENT_KEY</code></td>
        <td>Yes</td>
        <td>-</td>
        <td>Client key for GrowthBook SDK connection</td>
    </tr>
    <tr>
        <td><code>GROWTHBOOK_HOST_BASE_URL</code></td>
        <td>Yes</td>
        <td>-</td>
        <td>Base URL of your GrowthBook instance</td>
    </tr>
    <tr>
        <td><code>GROWTHBOOK_REQUESTS_TIMEOUT</code></td>
        <td>No</td>
        <td>60</td>
        <td>Timeout in seconds for GrowthBook API requests</td>
    </tr>
    <tr>
        <td><code>GROWTHBOOK_WEBHOOK_SECRET</code></td>
        <td>No</td>
        <td>-</td>
        <td>Secret key for webhook authentication</td>
    </tr>
    <tr>
        <td><code>CACHE_KEY_PREFIX</code></td>
        <td>No</td>
        <td>weni_feature_flags</td>
        <td>Prefix for cache keys</td>
    </tr>
    <tr>
        <td><code>FEATURES_CACHE_TTL</code></td>
        <td>No</td>
        <td>60</td>
    <td>Cache TTL in seconds for feature flags</td>
</tr>
</table>

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

