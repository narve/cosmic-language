#!/bin/sh
# A blind-decoding run in which the reader may compute: a headless `claude` whose only tool runs Python inside a
# Docker container without network that holds nothing but the message (as /work/bits.txt). No built-in tools, no
# settings, no project instructions; started in an empty temporary directory. Run `npm run build` first.
#
#   npm run --silent blind:code [task] > answer.txt     task defaults to last-statement-code
#   BLIND_MODEL=opus npm run --silent blind:code         with a named model
#   BLIND_MESSAGE=docs/minimal/message.bin npm run --silent blind:code purpose-code
#                                                        with another message than docs/message.bin (here the core)
#   npm run --silent blind:code interpretation-code       the whole interpretation: format, vocabulary (a table that
#                                                        can be scored against spec §9) and the knowledge in the message
#
# The answer goes to standard output. The full record (every piece of code the reader ran, as JSON lines) is
# written to the file named on standard error.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
message=$(cd "$here/../../.." && realpath "${BLIND_MESSAGE:-docs/message.bin}")
task=${1:-last-statement-code}
dir=$(mktemp -d)
box="blind-$$"
export BLIND_CONTAINER="$box"

node -e '
  const bytes = require("fs").readFileSync(process.argv[1]);
  process.stdout.write(Array.from(bytes, (b) => b.toString(2).padStart(8, "0")).join("") + "\n");
' "$message" > "$dir/bits.txt"

docker run -d --rm --name "$box" --network none python:3.12-alpine sleep 7200 > /dev/null
trap 'docker rm -f "$box" > /dev/null 2>&1' EXIT
docker exec "$box" mkdir -p /work
docker cp -q "$dir/bits.txt" "$box:/work/bits.txt"
rm "$dir/bits.txt"

cat > "$dir/mcp.json" <<JSON
{ "mcpServers": { "sandbox": { "command": "node", "args": ["$here/sandbox-server.mjs"], "env": { "BLIND_CONTAINER": "$box" } } } }
JSON

cd "$dir"
claude -p ${BLIND_MODEL:+--model $BLIND_MODEL} --tools "" --strict-mcp-config --mcp-config "$dir/mcp.json" \
  --allowedTools "mcp__sandbox__run_python" --setting-sources "" \
  --system-prompt "You are a careful analyst. Your only tool runs Python in a sandbox. Work only from what you find there." \
  --output-format stream-json --verbose < "$here/$task.txt" > "$dir/record.jsonl"

node -e '
  const lines = require("fs").readFileSync(process.argv[1], "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l));
  const result = lines.filter((l) => l.type === "result").pop();
  process.stdout.write((result?.result ?? "(no result)") + "\n");
' "$dir/record.jsonl"
echo "record: $dir/record.jsonl" >&2
