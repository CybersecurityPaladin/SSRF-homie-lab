#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

LEVEL=""
while [[ $# -gt 0 ]]; do
case "$1" in
-l)
LEVEL="$2"
shift 2
      ;;
-[0-9]*)
LEVEL="${1#-}"
shift
      ;;
*)
exit 1
      ;;
esac
done

if [[ -z "$LEVEL" ]]; then
echo "specify the level: $0 -l <N>"
exit 1
fi

LEVEL_DIR="level$LEVEL"
if [[ ! -d "$LEVEL_DIR" ]]; then
echo "$LEVEL_DIR not found"
exit 1
fi

cd "$LEVEL_DIR"

pids=()
cleanup() {
for pid in "${pids[@]}"; do
kill "$pid" 2>/dev/null || true
done
exit 0
}
trap cleanup INT TERM

case "$LEVEL" in
1)
python3 internal_target.py &
pids+=($!)
sleep 0.5
python3 app.py &
pids+=($!)
    ;;
*)
exit 1
    ;;
esac

wait