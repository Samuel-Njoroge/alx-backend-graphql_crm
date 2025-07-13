#!/bin/bash

# Navigate to the Django project directory
cd "$(dirname "$0")/../.." || exit

# Run Django shell command to delete inactive customers and log results
deleted_count=$(./manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

cutoff_date = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(last_order__lt=cutoff_date)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log output with timestamp
echo \"[\$(date '+%Y-%m-%d %H:%M:%S')] Deleted \$deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
