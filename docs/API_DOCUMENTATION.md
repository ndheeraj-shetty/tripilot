# Zombie Run Cost Killer - REST API Documentation

## Base URL
`http://localhost:8000/api/v1`

---

## Endpoints Summary

### 1. Health Check
#### `GET /health`
Returns system status, environment details, PostgreSQL database connectivity, and database ping latency.

**Response (200 OK)**:
```json
{
  "status": "online",
  "app_name": "Zombie Run Cost Killer",
  "version": "1.0.0",
  "environment": "development",
  "database_status": "healthy",
  "latency_ms": 2.45
}
```

---

### 2. Projects API

#### `GET /projects`
List all registered ML projects with pagination support (`skip`, `limit`).

#### `POST /projects`
Create a new ML project configuration.

**Request Body**:
```json
{
  "name": "ResNet50 ImageNet Fine-Tuning",
  "description": "Classification fine-tuning",
  "framework": "PyTorch",
  "model_name": "resnet50",
  "dataset_path": "C:/datasets/imagenet",
  "training_script_path": "C:/models/train.py",
  "output_dir": "./storage/outputs",
  "checkpoint_dir": "./storage/checkpoints",
  "automation_enabled": true
}
```

#### `GET /projects/{id}`
Retrieve a specific project by UUID.

#### `PUT /projects/{id}`
Update an existing project's parameters.

#### `DELETE /projects/{id}`
Delete a project record from PostgreSQL. Returns `204 No Content`.

---

### 3. Settings API

#### `GET /settings`
Get system configuration settings and default storage directory paths.

#### `PUT /settings`
Update application settings keys and values.
