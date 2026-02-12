#!/bin/bash

set -e  

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

echo "=========================================="
echo "RabbitMQ Monitoring User Setup"
echo "=========================================="
echo ""
echo "A dedicated RabbitMQ monitoring user with the following read-only permissions will be created:"
echo "  Tag: monitoring"
echo "  Permissions: Read-only access to all vhosts"
echo ""

read -p "Enter RabbitMQ Management URL (e.g., http://localhost:15672): " RABBITMQ_URL

if [ -z "$RABBITMQ_URL" ]; then
    print_error "RabbitMQ URL cannot be empty!"
    exit 1
fi

RABBITMQ_URL=$(echo "$RABBITMQ_URL" | sed 's:/*$::')  

read -p "Enter Admin Username: " ADMIN_USER

if [ -z "$ADMIN_USER" ]; then
    print_error "Admin username cannot be empty!"
    exit 1
fi

read -sp "Enter Admin Password: " ADMIN_PASS
echo ""

if [ -z "$ADMIN_PASS" ]; then
    print_error "Admin password cannot be empty!"
    exit 1
fi

print_info "Testing connection to RabbitMQ at $RABBITMQ_URL..."
CONN_TEST=$(curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" "$RABBITMQ_URL/api/overview" -o /dev/null -w "%{http_code}" 2>&1)
if [ "$CONN_TEST" != "200" ]; then
    print_error "Failed to connect to RabbitMQ (HTTP $CONN_TEST). Please check URL and credentials."
    echo "  URL: $RABBITMQ_URL"
    echo "  Username: $ADMIN_USER"
    exit 1
fi

echo ""

print_info "Connection successful!"
echo ""

read -p "Enter Monitoring Username to create/update: " MONITOR_USER

if [ -z "$MONITOR_USER" ]; then
    print_error "Monitoring username cannot be empty!"
    exit 1
fi

while true; do
    read -sp "Enter Monitoring Password: " MONITOR_PASS
    echo ""
    
    if [ -z "$MONITOR_PASS" ]; then
        print_error "Monitoring password cannot be empty!"
        exit 1
    fi
    
    read -sp "Re-enter Password to Confirm: " MONITOR_PASS_CONFIRM
    echo ""
    
    if [ "$MONITOR_PASS" = "$MONITOR_PASS_CONFIRM" ]; then
        break
    else
        print_error "Passwords do not match! Please try again."
        echo ""
    fi
done

print_info "Checking if user '$MONITOR_USER' exists..."
USER_EXISTS=$(curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" "$RABBITMQ_URL/api/users/$MONITOR_USER" -o /dev/null -w "%{http_code}")

while [ "$USER_EXISTS" = "200" ]; do
    print_warning "User '$MONITOR_USER' already exists!"
    echo "This will update the user's password and permissions."
    read -p "Do you want to continue? (y/n): " CONTINUE
    
    if [ "$CONTINUE" = "y" ] || [ "$CONTINUE" = "Y" ]; then
        print_info "Updating password and tag for user '$MONITOR_USER'..."
        curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" -X PUT "$RABBITMQ_URL/api/users/$MONITOR_USER" \
            -H "content-type:application/json" \
            -d "{\"password\":\"$MONITOR_PASS\",\"tags\":\"monitoring\"}" > /dev/null
        print_info "User updated successfully!"
        break
    else
        print_info "User update cancelled. Please provide new credentials."
        echo ""
        read -p "Enter New Monitoring Username: " MONITOR_USER
        
        if [ -z "$MONITOR_USER" ]; then
            print_error "Monitoring username cannot be empty!"
            exit 1
        fi
        
        while true; do
            read -sp "Enter New Monitoring Password: " MONITOR_PASS
            echo ""
            
            if [ -z "$MONITOR_PASS" ]; then
                print_error "Monitoring password cannot be empty!"
                exit 1
            fi
            
            read -sp "Re-enter Password to Confirm: " MONITOR_PASS_CONFIRM
            echo ""
            
            if [ "$MONITOR_PASS" = "$MONITOR_PASS_CONFIRM" ]; then
                print_info "Passwords match!"
                break
            else
                print_error "Passwords do not match! Please try again."
                echo ""
            fi
        done
        
        USER_EXISTS=$(curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" "$RABBITMQ_URL/api/users/$MONITOR_USER" -o /dev/null -w "%{http_code}")
    fi
done

if [ "$USER_EXISTS" != "200" ]; then
    print_info "Creating new user '$MONITOR_USER' with 'monitoring' tag..."
    curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" -X PUT "$RABBITMQ_URL/api/users/$MONITOR_USER" \
        -H "content-type:application/json" \
        -d "{\"password\":\"$MONITOR_PASS\",\"tags\":\"monitoring\"}" > /dev/null
    print_info "User created successfully!"
fi
echo ""

print_info "Fetching all vhosts..."
VHOSTS=$(curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" "$RABBITMQ_URL/api/vhosts" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)

if [ -z "$VHOSTS" ]; then
    print_error "No vhosts found or failed to fetch vhosts."
    exit 1
fi

print_info "Found vhosts:"
echo "$VHOSTS" | while read vhost; do
    echo "  - $vhost"
done
echo ""

print_info "Granting read-only permissions to all vhosts..."
echo "$VHOSTS" | while read vhost; do
    ENCODED_VHOST=$(echo "$vhost" | sed 's/\//%2F/g')
    
    print_info "Setting permissions for vhost: $vhost"
    
    curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" -X PUT "$RABBITMQ_URL/api/permissions/$ENCODED_VHOST/$MONITOR_USER" \
        -H "content-type:application/json" \
        -d '{"configure":"^$","write":"^$","read":".*"}' > /dev/null
    print_info "   Permissions set for vhost: $vhost"
done
echo ""

print_info "Verifying permissions for user '$MONITOR_USER'..."
curl -k -s -u "$ADMIN_USER:$ADMIN_PASS" "$RABBITMQ_URL/api/users/$MONITOR_USER/permissions" | \
    grep -o '"vhost":"[^"]*"' | cut -d'"' -f4 | while read vhost; do
    echo "  - Vhost: $vhost (Read-only access)"
done
echo ""

print_info "Testing monitoring user access..."
sleep 1  
TEST_RESULT=$(curl -k -s -u "$MONITOR_USER:$MONITOR_PASS" "$RABBITMQ_URL/api/overview" -o /dev/null -w "%{http_code}")
if [ "$TEST_RESULT" = "200" ]; then
    print_info " Monitoring user can access the Management API successfully!"
elif [ "$TEST_RESULT" = "401" ]; then
    print_warning "User authentication failed (HTTP 401). Possible reasons:"
    print_warning "  - User changes may need time to propagate"
    print_info "Retrying in 2 seconds..."
    sleep 2
    TEST_RESULT=$(curl -k -s -u "$MONITOR_USER:$MONITOR_PASS" "$RABBITMQ_URL/api/overview" -o /dev/null -w "%{http_code}")
    if [ "$TEST_RESULT" = "200" ]; then
        print_info " Monitoring user can access the Management API successfully (retry successful)!"
    else
        print_error " Still cannot access the Management API (HTTP $TEST_RESULT)"
        print_info "Please verify credentials manually:"
        echo "  curl -k -u $MONITOR_USER:PASSWORD $RABBITMQ_URL/api/overview"
        echo ""
        print_error "User setup failed! User cannot authenticate."
        exit 1
    fi
else
    print_error " Monitoring user cannot access the Management API (HTTP $TEST_RESULT)"
    echo ""
    print_error "User setup failed! Unexpected error."
    exit 1
fi
echo ""

echo "=========================================="
print_info "User setup completed successfully!"
echo "=========================================="
echo ""
echo "User Details:"
echo "  Username: $MONITOR_USER"
echo "  Tag: monitoring"
echo "  Permissions: Read-only access to all vhosts"