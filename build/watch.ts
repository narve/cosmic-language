// Reruns the build when any file in site/ changes: npm run watch. Node's own modules only.
// It polls instead of using fs.watch, because file events do not reliably cross the virtiofs mount from the host.
// A change is built once it has held for one poll, so a save in several steps gives one build; a change made during a
// build gives another build after it. A failed build is reported and the watcher goes on.
import { spawn } from "node:child_process";
import { lstat, readdir } from "node:fs/promises";
import { join, resolve } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";

const ROOT = resolve(import.meta.dirname, "..");
const SITE = join(ROOT, "site");
const POLL_MS = 500;

// Every path in site/ with its modification time and size. A file deleted while listing is simply left out.
async function snapshot(): Promise<string> {
  const paths = (await readdir(SITE, { recursive: true })).sort();
  const lines = await Promise.all(
    paths.map(async (path) => {
      const stat = await lstat(join(SITE, path)).catch(() => undefined);
      return stat ? `${path}\0${stat.mtimeMs}\0${stat.size}` : "";
    }),
  );
  return lines.join("\n");
}

function build(): Promise<number | null> {
  return new Promise((done) => {
    const child = spawn("npm", ["run", "--silent", "build"], { cwd: ROOT, stdio: "inherit" });
    child.on("error", (error) => {
      console.error(`watch: ${error.message}`);
      done(null);
    });
    child.on("close", done);
  });
}

const time = () => new Date().toLocaleTimeString("en-GB");

let built = await snapshot();
let previous = built;
console.log(`Watching site/ (every ${POLL_MS} ms)`);

while (true) {
  await sleep(POLL_MS);
  let current: string;
  try {
    current = await snapshot();
  } catch (error) {
    console.error(`watch: ${(error as Error).message}`);
    continue;
  }
  if (current !== built && current === previous) {
    built = current;
    console.log(`[${time()}] site/ changed, building`);
    const status = await build();
    console.log(`[${time()}] ${status === 0 ? "build passed" : `build FAILED (exit ${status})`}`);
  }
  previous = current;
}
