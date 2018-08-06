echo "db = db.getSiblingDB('fedssh');"
echo "db.createUser({user: '$FED_SSH_USERNAME', pwd: '$FED_SSH_PASSWORD', roles: ['readWrite']});"
