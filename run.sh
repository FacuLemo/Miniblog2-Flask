#!/bin/bash
# Sleep for 10 seconds before running migrations
echo 'sleep 10 secs'
sleep 10

echo 'run db script'
# Define the number of retries

# Run your first command (e.g., flask db init)
echo 'run flask db init'
sleep 10
flask db init

# Run your second command (e.g., another command)
echo 'run flask db migrate'
sleep 10
flask db migrate -m "initial migration"

# Run your third command (e.g., yet another command)
echo 'run flask db upgrade'
sleep 10
flask db upgrade

# Start your Flask application
echo 'start gunicorn server'
gunicorn app:app --bind 0.0.0.0:5040 --reload