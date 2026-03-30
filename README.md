Project created by Gabriel Baptistussi
gabriel.baptistussi@gmail.com

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

### Store Private Key in SSM
```bash
aws ssm put-parameter \
  --name "/starkbank/private-key" \
  --value "$(cat keys/private_key.pem)" \
  --type "SecureString" \
  --region us-east-1
```

### Build
```bash
./scripts/build.sh cronjob
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


## Testing locally

- Run the scripts
```bash
uv run python -m src.invoices
```
