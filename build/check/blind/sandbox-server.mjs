// A minimal MCP server (JSON-RPC over standard input and output) with one tool, run_python.
// The code runs inside the Docker container named by BLIND_CONTAINER, which has no network and holds only the
// message. This is the only tool the blind reader gets (see run-with-code.sh).
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";

const container = process.env.BLIND_CONTAINER;
const LIMIT = 20000; // characters of output returned to the reader
const TIMEOUT = 120; // seconds per run

const tool = {
  name: "run_python",
  description:
    "Run Python 3 code in an isolated sandbox (no network). The code is given on standard input to `python3 -`. " +
    "Returns what it prints (standard output and standard error), cut off after " + LIMIT + " characters. " +
    "Files written under /work stay there between calls. Each run is stopped after " + TIMEOUT + " seconds.",
  inputSchema: { type: "object", properties: { code: { type: "string", description: "Python 3 source" } }, required: ["code"] },
};

function run(code) {
  return new Promise((done) => {
    const child = spawn("docker", ["exec", "-i", "-w", "/work", container, "timeout", String(TIMEOUT), "python3", "-"]);
    let out = "";
    child.stdout.on("data", (data) => (out += data));
    child.stderr.on("data", (data) => (out += data));
    child.on("close", (status) => {
      if (out.length > LIMIT) out = out.slice(0, LIMIT) + `\n[output cut off after ${LIMIT} characters]`;
      done({ content: [{ type: "text", text: out || "(no output)" }], isError: status !== 0 });
    });
    child.stdin.end(code);
  });
}

const send = (message) => process.stdout.write(JSON.stringify(message) + "\n");

createInterface({ input: process.stdin }).on("line", async (text) => {
  if (!text.trim()) return;
  const { id, method, params } = JSON.parse(text);
  if (id === undefined) return; // a notification
  if (method === "initialize") {
    send({ jsonrpc: "2.0", id, result: { protocolVersion: params.protocolVersion, capabilities: { tools: {} }, serverInfo: { name: "sandbox", version: "1" } } });
  } else if (method === "tools/list") send({ jsonrpc: "2.0", id, result: { tools: [tool] } });
  else if (method === "tools/call" && params.name === tool.name) send({ jsonrpc: "2.0", id, result: await run(String(params.arguments?.code ?? "")) });
  else if (method === "ping") send({ jsonrpc: "2.0", id, result: {} });
  else send({ jsonrpc: "2.0", id, error: { code: -32601, message: `unknown method ${method}` } });
});
