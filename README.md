Project created by Gabriel Baptistussi
gabriel.baptistussi@gmail.com

## Task 1

This repository sets up an AWS Lambda cronjob that runs on a schedule (via EventBridge Scheduler) to generate and create invoices using the Starkbank SDK.

**How it works:**
- **EventBridge Scheduler** triggers the Lambda function on a schedule (configurable via `var.cron_schedule`)
- **Lambda function** (`src/cronjob/add_invoices.py`) generates 8-12 fake invoices with random amounts, names, and CPFs using the Starkbank SDK
- **SSM Parameter Store** stores the Starkbank private key securely at `/starkbank/private-key` (created via Terraform)
- The Lambda fetches the private key from SSM at runtime and authenticates with Starkbank using the project ID from variables

## Task 2

This task adds a webhook endpoint that receives events from Starkbank. When an invoice event is received, it parses the event and executes a transfer.

**How it works:**
- **Lambda Function URL** exposes a POST endpoint to receive webhook events from Starkbank
- **Lambda function** (`src/webhook/webhook.py`) parses the event signature, extracts invoice amount, and executes a transfer
- Reuses the same SSM parameter and build artifacts from Task 1

## Setting up environment

### Sync uv environment

```bash
uv sync
```

### Set env vars

- Copy .env.example into .env:
```bash
cp .env.example .env
```

- Edit .env with your project id and path to api key
- Load .env
```bash
source .env
```

## Cronjob Deployment

### Prerequisites
- AWS CLI configured with appropriate credentials
- Terraform >= 1.0 installed

### Build
```bash
./scripts/build.sh
```

### Deploy
```bash
cd aws
terraform init
terraform plan -var="environment=dev"
terraform apply -var="environment=dev"
```

### Configure Schedule
The cronjob runs every 3 hours by default. To change the schedule, modify `aws/variables.tf`:

```hcl
cron_schedule = "rate(3 hours)"  # Every 3 hours
cron_schedule = "cron(0 12 * * ? *)"  # Daily at noon UTC
cron_schedule = "cron(0/30 * * * ? *)"  # Every 30 minutes
```

