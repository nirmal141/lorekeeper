#!/bin/bash
set -e

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_DIR="$PROJ_DIR/.pids"
mkdir -p "$PID_DIR"

echo "Starting Lorekeeper..."

# 1. Temporal dev server
temporal server start-dev --log-format pretty > /dev/null 2>&1 &
echo $! > "$PID_DIR/temporal.pid"
echo "  Temporal server starting..."

# Wait for Temporal to be ready
for i in {1..15}; do
  if curl -s http://localhost:7233 > /dev/null 2>&1; then
    echo "  Temporal server ready"
    break
  fi
  sleep 1
done

# 2. Activate venv and start services from project root
cd "$PROJ_DIR"
source "$PROJ_DIR/backend/venv/bin/activate"

# 3. Temporal worker
python -m backend.temporal.worker > /dev/null 2>&1 &
echo $! > "$PID_DIR/worker.pid"
echo "  Temporal worker started"

# 4. FastAPI backend
uvicorn backend.main:app --reload --port 8000 > /dev/null 2>&1 &
echo $! > "$PID_DIR/backend.pid"
echo "  Backend starting..."
sleep 2

# 5. Frontend
cd "$PROJ_DIR/frontend"
npm run dev -- --host > /dev/null 2>&1 &
echo $! > "$PID_DIR/frontend.pid"
echo "  Frontend started"

echo ""
echo "All services running:"
echo "  Frontend:  http://localhost:5173"
echo "  Backend:   http://localhost:8000"
echo "  Temporal:  http://localhost:8233"
echo ""
echo "Run ./stop.sh to shut everything down"
