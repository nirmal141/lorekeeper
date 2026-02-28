#!/bin/bash

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_DIR="$PROJ_DIR/.pids"

echo "Stopping Lorekeeper..."

for service in frontend backend worker temporal; do
  pidfile="$PID_DIR/$service.pid"
  if [ -f "$pidfile" ]; then
    pid=$(cat "$pidfile")
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null
      echo "  Stopped $service (pid $pid)"
    fi
    rm -f "$pidfile"
  fi
done

# Cleanup any stragglers on known ports
lsof -ti:8000 -ti:7233 -ti:5173 -ti:8233 2>/dev/null | xargs kill -9 2>/dev/null
pkill -f "temporal server" 2>/dev/null
pkill -f "backend.temporal.worker" 2>/dev/null

echo "All services stopped"
