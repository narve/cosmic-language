#!/bin/sh
# A blind-decoding run in which the reader may compute: a headless `claude` whose only tool runs Python inside a
# Docker container without network that holds nothing but the message (as /work/bits.txt). No built-in tools, no
# settings, no project instructions; started in an empty temporary directory. Run `npm run build` first.
#
#   npm run --silent blind [task] > answer.txt          task defaults to purpose; the tasks are the .txt files here
#   BLIND_MODEL=opus npm run --silent blind              with a named model
#   BLIND_MESSAGE=docs/minimal/message.bin npm run --silent blind purpose
#                                                        with another message than docs/message.bin (here the minimal one)
#   BLIND_INVERT=0 npm run --silent blind                 without inverting the bits (inverted by default)
#   npm run --silent blind interpretation                 the whole interpretation: format, vocabulary (a table that
#                                                        can be scored against spec §9) and the knowledge in the message
#
# The answer goes to standard output. The full record (every piece of code the reader ran, as JSON lines) is
# written to the file named on standard error.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
message=$(cd "$here/../../.." && realpath "${BLIND_MESSAGE:-docs/message.bin}")
task=${1:-purpose}
dir=$(mktemp -d)
box="blind-$$"
export BLIND_CONTAINER="$box"

# Nothing in a stream of bits says which of the two values is "1". By default every bit is inverted, so the
# reader cannot rely on our choice; BLIND_INVERT=0 gives the bits as they are.
node -e '
  const bytes = require("fs").readFileSync(process.argv[1]);
  const bits = Array.from(bytes, (b) => b.toString(2).padStart(8, "0")).join("");
  process.stdout.write((process.argv[2] === "0" ? bits : bits.replace(/[01]/g, (c) => (c === "0" ? "1" : "0"))) + "\n");
' "$message" "${BLIND_INVERT:-1}" > "$dir/bits.txt"

docker run -d --rm --name "$box" --network none python:3.12-alpine sleep infinity > /dev/null
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
