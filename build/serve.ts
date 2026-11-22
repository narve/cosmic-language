// A small static server for docs/, for reading the generated pages locally: npm run serve. Node's own modules only.
// Safe by default: it listens on 127.0.0.1 only, answers GET and HEAD, serves regular files inside docs/ and nothing
// else (no dotfiles, no directory listings, no symlink that leads out of docs/). A directory serves its index.html.
// Each request reads docs/ afresh, so a rebuild needs no restart. PORT and HOST change where it listens.
import { constants } from "node:fs";
import { open, realpath, type FileHandle } from "node:fs/promises";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { extname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { pipeline } from "node:stream/promises";

const DOCS = resolve(import.meta.dirname, "..", "docs");
const HOST = process.env.HOST ?? "127.0.0.1";
const PORT = Number(process.env.PORT ?? 8080);
const LOOPBACK = new Set(["127.0.0.1", "localhost", "[::1]", "::1"]);

const TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".svg": "image/svg+xml",
  ".jpg": "image/jpeg",
  ".txt": "text/plain; charset=utf-8",
  ".bits": "text/plain; charset=utf-8",
  ".bin": "application/octet-stream",
};

const HEADERS = {
  "Cache-Control": "no-store", // a rebuild shows at once
  "Content-Security-Policy":
    "default-src 'none'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; " +
    "img-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
  "Cross-Origin-Resource-Policy": "same-origin",
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
};

// The decoded parts of a request's path, or undefined if any part is not a plain name. Refusing every part that starts
// with "." covers both ".." and dotfiles; refusing empty parts covers "//evil.example", which must never be redirected.
function pathParts(url: string): { parts: string[]; slash: boolean } | undefined {
  if (!url.startsWith("/")) return undefined;
  const end = url.search(/[?#]/);
  const raw = (end < 0 ? url : url.slice(0, end)).slice(1).split("/");
  const slash = raw[raw.length - 1] === "";
  if (slash) raw.pop();
  const parts: string[] = [];
  for (const part of raw) {
    let name: string;
    try {
      name = decodeURIComponent(part);
    } catch {
      return undefined;
    }
    if (name === "" || name.startsWith(".") || /[/\\\p{Cc}]/u.test(name)) return undefined;
    parts.push(name);
  }
  return { parts, slash };
}

interface Opened { handle: FileHandle; path: string; size: number; directory: boolean }

// Opens a path if, with its symlinks resolved, it is a regular file or a directory inside docs/ and no part of it is hidden.
async function openInside(root: string, path: string): Promise<Opened | undefined> {
  const real = await realpath(path);
  const inside = relative(root, real);
  if (isAbsolute(inside) || inside.split(sep).some((part) => part.startsWith("."))) return undefined;
  // O_NOFOLLOW: the file cannot have become a symlink since the check; O_NONBLOCK: opening a pipe cannot hang.
  const handle = await open(real, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
  const stat = await handle.stat();
  if (stat.isFile() || stat.isDirectory()) return { handle, path: real, size: stat.size, directory: stat.isDirectory() };
  await handle.close();
  return undefined;
}

function plain(response: ServerResponse, status: number, text: string, extra: Record<string, string> = {}): void {
  // Fixed texts only: nothing from the request is ever echoed.
  response.writeHead(status, { ...HEADERS, "Content-Type": "text/plain; charset=utf-8", "Content-Length": Buffer.byteLength(text), ...extra });
  response.end(response.req.method === "HEAD" ? undefined : text);
}

// With a loopback address, only loopback host names: a web page cannot reach this server by rebinding its own domain.
function hostAllowed(request: IncomingMessage): boolean {
  if (!LOOPBACK.has(HOST)) return true;
  try {
    return LOOPBACK.has(new URL(`http://${request.headers.host}`).hostname);
  } catch {
    return false;
  }
}

async function handle(request: IncomingMessage, response: ServerResponse): Promise<void> {
  if (request.method !== "GET" && request.method !== "HEAD") return plain(response, 405, "Method not allowed\n", { Allow: "GET, HEAD" });
  if (!hostAllowed(request)) return plain(response, 403, "Forbidden\n");
  const notFound = () => plain(response, 404, "Not found\n");
  const target = pathParts(request.url ?? "");
  if (!target) return notFound();

  let file: Opened | undefined;
  try {
    const root = await realpath(DOCS);
    file = await openInside(root, join(root, ...target.parts));
    if (!file) return notFound();
    if (file.directory) {
      await file.handle.close();
      const directory = file.path;
      file = undefined;
      // A directory is addressed with a final slash, so that the relative links of its index.html work.
      if (!target.slash) {
        const location = `/${target.parts.map(encodeURIComponent).join("/")}/`;
        return plain(response, 301, "Moved\n", { Location: location });
      }
      file = await openInside(root, join(directory, "index.html"));
      if (!file || file.directory) return notFound();
    } else if (target.slash) {
      return notFound(); // a file is not a directory
    }
    response.writeHead(200, {
      ...HEADERS,
      "Content-Type": TYPES[extname(file.path).toLowerCase()] ?? "application/octet-stream",
      "Content-Length": file.size,
    });
    if (request.method === "HEAD" || file.size === 0) {
      response.end();
      return;
    }
    await pipeline(file.handle.createReadStream({ start: 0, end: file.size - 1, autoClose: false }), response);
  } catch (error) {
    if (response.headersSent) {
      response.destroy(); // the file changed or the reader left: never send a partial page as if it were whole
      return;
    }
    const code = (error as NodeJS.ErrnoException).code ?? "";
    if (["ENOENT", "ENOTDIR", "ELOOP", "EACCES", "ENAMETOOLONG"].includes(code)) return notFound();
    console.error("serve:", code || error);
    plain(response, 500, "Server error\n");
  } finally {
    await file?.handle.close().catch(() => {});
  }
}

if (!Number.isInteger(PORT) || PORT < 1 || PORT > 65535) {
  console.error("serve: PORT must be a number from 1 to 65535");
  process.exit(1);
}
const server = createServer((request, response) => void handle(request, response));
server.headersTimeout = 10_000;
server.requestTimeout = 15_000;
server.on("error", (error) => {
  console.error(`serve: ${error.message}`);
  process.exit(1);
});
server.listen(PORT, HOST, () => {
  console.log(`Serving docs/ on http://${HOST.includes(":") ? `[${HOST}]` : HOST}:${PORT}/`);
  if (!LOOPBACK.has(HOST)) console.log("Warning: this address can be reached from other machines.");
});
