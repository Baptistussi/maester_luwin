Project created by Gabriel Baptistussi
gabriel.baptistussi@gmail.com

## Cronjob Deployment

### Prerequisites
- AWS CLI configured with appropriate credentials
- Terraform >= 1.0 installed

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
