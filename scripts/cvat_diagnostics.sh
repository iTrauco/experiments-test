#!/bin/bash

# CVAT Annotation Count Issue Diagnostics
# Focused on identifying why job statistics aren't updating

OUTPUT_FILE="cvat_annotation_diagnostics_$(date +%Y%m%d_%H%M%S).txt"

echo "CVAT Annotation Count Diagnostics" > "$OUTPUT_FILE"
echo "Issue: Job showing '1 annotating • 1 total' when ~30 frames annotated" >> "$OUTPUT_FILE"
echo "Generated: $(date)" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

# 1. Container status - what's running?
echo "1. RUNNING CONTAINERS:" >> "$OUTPUT_FILE"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" >> "$OUTPUT_FILE" 2>&1
echo "" >> "$OUTPUT_FILE"

# 2. Database container volumes - is data persisting?
echo "2. DATABASE PERSISTENCE:" >> "$OUTPUT_FILE"
DB_CONTAINER=$(docker ps --format "{{.Names}}" | grep -E "(postgres|db)" | head -1)
if [ ! -z "$DB_CONTAINER" ]; then
    echo "Database container: $DB_CONTAINER" >> "$OUTPUT_FILE"
    docker inspect "$DB_CONTAINER" --format='{{range .Mounts}}{{.Type}}: {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' >> "$OUTPUT_FILE" 2>&1
else
    echo "No database container found" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 3. CVAT container volumes
echo "3. CVAT DATA PERSISTENCE:" >> "$OUTPUT_FILE"
CVAT_CONTAINER=$(docker ps --format "{{.Names}}" | grep -i cvat | grep -v postgres | head -1)
if [ ! -z "$CVAT_CONTAINER" ]; then
    echo "CVAT container: $CVAT_CONTAINER" >> "$OUTPUT_FILE"
    docker inspect "$CVAT_CONTAINER" --format='{{range .Mounts}}{{.Type}}: {{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' >> "$OUTPUT_FILE" 2>&1
else
    echo "No CVAT container found" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 4. Recent logs for job status errors
echo "4. RECENT LOGS (job/annotation related):" >> "$OUTPUT_FILE"
if [ ! -z "$CVAT_CONTAINER" ]; then
    echo "--- CVAT container logs (last 20 lines) ---" >> "$OUTPUT_FILE"
    docker logs --tail 20 "$CVAT_CONTAINER" 2>&1 | grep -E "(job|annotation|save|complete)" >> "$OUTPUT_FILE" || echo "No job-related log entries found" >> "$OUTPUT_FILE"
fi
if [ ! -z "$DB_CONTAINER" ]; then
    echo "--- Database logs (last 10 lines) ---" >> "$OUTPUT_FILE"
    docker logs --tail 10 "$DB_CONTAINER" 2>&1 | grep -E "(error|ERROR|connection)" >> "$OUTPUT_FILE" || echo "No database errors found" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 5. Docker compose configuration
echo "5. DOCKER COMPOSE CONFIG:" >> "$OUTPUT_FILE"
if [ -f "docker-compose.yml" ]; then
    echo "Found docker-compose.yml" >> "$OUTPUT_FILE"
    grep -A 5 -B 5 "volumes:" docker-compose.yml >> "$OUTPUT_FILE" 2>&1
elif [ -f "docker-compose.yaml" ]; then
    echo "Found docker-compose.yaml" >> "$OUTPUT_FILE"
    grep -A 5 -B 5 "volumes:" docker-compose.yaml >> "$OUTPUT_FILE" 2>&1
else
    echo "No docker-compose file found in current directory" >> "$OUTPUT_FILE"
fi

echo "========================================" >> "$OUTPUT_FILE"
echo "Diagnostics complete: $OUTPUT_FILE"