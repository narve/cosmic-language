// Makes what a blind reader receives from a message file: the message sent REPEAT times in a row, received
// from a random bit inside the first repetition to a random bit inside the last, every bit inverted unless
// INVERT is "0", packed eight bits to a byte (the first bit received is the most significant bit of the first
// byte). Both cuts fall on any bit; the last byte is filled up with random bits, which look like noise
// received after the message stopped.
//   node stream.mjs message.bin out.bin [repeat=5] [invert=1]
// The cut points go to standard error, for the record; the reader never sees them.
import { readFileSync, writeFileSync } from "node:fs";
import { randomInt } from "node:crypto";

const [, , input, output, repeatArg = "5", invert = "1"] = process.argv;
const message = readFileSync(input);
const n = message.length * 8;
const repeat = Math.max(1, Number(repeatArg));
const bit = (i) => (message[(i % n) >> 3] >> (7 - (i & 7))) & 1;

let start = 0, end = n * repeat;
if (repeat > 1) {
  start = randomInt(1, n); // inside the first repetition, never at its first bit
  end = randomInt(n * (repeat - 1) + 1, n * repeat); // inside the last repetition, never at its last bit
}
const length = end - start;
const out = Buffer.alloc(Math.ceil(length / 8));
for (let k = 0; k < out.length * 8; k++) {
  const b = k < length ? bit(start + k) ^ (invert === "0" ? 0 : 1) : randomInt(0, 2); // after the end: noise
  if (b) out[k >> 3] |= 0x80 >> (k & 7);
}
writeFileSync(output, out);
console.error(`stream: message ${n} bits × ${repeat}, received bits ${start} to ${end} (${length} bits, then ${out.length * 8 - length} random bits to fill ${out.length} bytes; starts ${start} bits into a repetition, ends ${end - n * (repeat - 1)} bits into the last), ${invert === "0" ? "not inverted" : "inverted"}`);
