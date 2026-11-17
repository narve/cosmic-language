// Prints a blind-decoding prompt: a task text from this directory, followed by the bits of docs/message.bin.
// The reader gets nothing else: no tools, no files, no project instructions. Run `npm run build` first.
//
//   npm run --silent blind:prompt             the prompt on standard output, for any model or person
//   npm run --silent blind > result.txt       the same, answered by a headless `claude` without tools,
//                                             started in an empty temporary directory
//   BLIND_MODEL=opus npm run --silent blind   the same with a named model (the default model's safety filter
//                                             has rejected the long block of bits; see plan.md)
//
// The first argument names the task (default: last-statement, i.e. last-statement.txt).
import { readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const task = process.argv[2] ?? "last-statement";
// BLIND_MESSAGE names another message than docs/message.bin, e.g. docs/core/message.bin.
const bytes = readFileSync(resolve(import.meta.dirname, "../../..", process.env.BLIND_MESSAGE ?? "docs/message.bin"));
// message.bin has no padding today (the stream is a whole number of bytes); if that changes, the last byte's
// padding bits would be included here.
const bits = Array.from(bytes, (byte) => byte.toString(2).padStart(8, "0")).join("");
const WIDTH = 100; // not a multiple of the chunk size, so the wrapping gives nothing away
const lines: string[] = [];
for (let i = 0; i < bits.length; i += WIDTH) lines.push(bits.slice(i, i + WIDTH));
process.stdout.write(readFileSync(join(import.meta.dirname, `${task}.txt`), "utf8") + lines.join("\n") + "\n");
