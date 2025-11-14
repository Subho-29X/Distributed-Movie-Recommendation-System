#!/bin/bash

echo "🎬 Starting Movie Recommendation System..."
echo ""

# Kill any existing processes on ports 5002 and 5003
echo "Cleaning up any existing services..."
lsof -ti :5003 2>/dev/null | xargs kill -9 2>/dev/null
lsof -ti :5002 2>/dev/null | xargs kill -9 2>/dev/null
sleep 1

# Get the directory where this script is located
DIR="$(cd "$(dirname "$0")" && pwd)"

# Start recommender service
echo "Starting Recommender Service (Port 5003)..."
cd "$DIR/recommender_service"
nohup python3 app.py > /tmp/recommender.log 2>&1 &
RECOMMENDER_PID=$!
echo "  ✓ Recommender Service started (PID: $RECOMMENDER_PID)"

# Wait a bit for recommender to start
sleep 2

# Start user service
echo "Starting User Service (Port 5002)..."
cd "$DIR/user_service"
nohup python3 app.py > /tmp/user.log 2>&1 &
USER_PID=$!
echo "  ✓ User Service started (PID: $USER_PID)"

# Wait for services to fully start
sleep 2

echo ""
echo "✅ Both services are running!"
echo ""
echo "🌐 Open your browser and go to:"
echo "   http://localhost:5002"
echo ""
echo "📝 To stop the services, run:"
echo "   ./stop.sh"
echo ""
echo "📋 Log files:"
echo "   Recommender: /tmp/recommender.log"
echo "   User Service: /tmp/user.log"
