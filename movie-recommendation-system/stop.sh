#!/bin/bash

echo "🛑 Stopping Movie Recommendation System..."

# Kill processes on ports 5002 and 5003
lsof -ti :5003 2>/dev/null | xargs kill -9 2>/dev/null
lsof -ti :5002 2>/dev/null | xargs kill -9 2>/dev/null

echo "✅ All services stopped!"
