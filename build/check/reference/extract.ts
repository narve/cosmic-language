// Extracts the reference values the message's measurements are checked against, from the downloaded
// tables in this directory, into reference.json. Run with `npm run reference` after replacing a table.
// Numbers are kept as decimal strings, digit for digit as published, so nothing is lost to rounding.
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const dir = import.meta.dirname;
const read = (file: string) => readFileSync(join(dir, file), "latin1").split(/\r?\n/);

const SOURCES = {
  codata: {
    title: "CODATA Recommended Values of the Fundamental Physical Constants: 2022",
    citation: "P. J. Mohr, D. B. Newell, B. N. Taylor and E. Tiesinga, Rev. Mod. Phys. 97, 025002 (2025)",
    url: "https://physics.nist.gov/cuu/Constants/Table/allascii.txt",
    file: "codata-2022-allascii.txt",
    retrieved: "2026-11-17",
  },
  nubase: {
    title: "The NUBASE2020 evaluation of nuclear physics properties",
    citation: "F. G. Kondev, M. Wang, W. J. Huang, S. Naimi and G. Audi, Chin. Phys. C 45, 030001 (2021)",
    url: "https://www-nds.iaea.org/amdc/ame2020/nubase_4.mas20.txt",
    file: "nubase_4.mas20.txt",
    retrieved: "2026-11-17",
  },
  ame: {
    title: "The AME 2020 atomic mass evaluation",
    citation: "M. Wang, W. J. Huang, F. G. Kondev, G. Audi and S. Naimi, Chin. Phys. C 45, 030003 (2021)",
    url: "https://www-nds.iaea.org/amdc/ame2020/mass_1.mas20.txt",
    file: "mass_1.mas20.txt",
    retrieved: "2026-11-17",
  },
};

// The CODATA quantities the message uses, by their names in the table.
const CONSTANTS = [
  "speed of light in vacuum",
  "Planck constant",
  "reduced Planck constant",
  "Newtonian constant of gravitation",
  "elementary charge",
  "Boltzmann constant",
  "Stefan-Boltzmann constant",
  "vacuum electric permittivity",
  "vacuum mag. permeability",
  "fine-structure constant",
  "inverse fine-structure constant",
  "Rydberg constant",
  "Rydberg constant times hc in J",
  "electron mass",
  "proton mass",
  "neutron mass",
  "deuteron mass",
  "atomic mass constant",
  "electron mass energy equivalent",
  "proton-electron mass ratio",
  "neutron-electron mass ratio",
  "neutron-proton mass ratio",
  "Planck length",
  "Planck time",
  "Planck mass",
  "Planck temperature",
];

// The nuclides the message mentions: the free neutron and the isotopes of its elements, as [A, Z].
const NUCLIDES: [number, number][] = [
  [1, 0], [1, 1], [2, 1], [3, 1], [3, 2], [4, 2], [12, 6], [13, 6], [14, 6], [16, 8],
];

function fail(message: string): never {
  throw new Error(`reference data: ${message}`);
}

// "6.674 30 e-11" → "6.67430e-11". A value ending in "..." is exact but cut off in the table.
function number(text: string): { value: string; truncated: boolean } {
  const truncated = text.includes("...");
  const value = text.replace("...", "").replace(/\s+/g, "");
  if (!/^-?\d+(\.\d+)?(e-?\d+)?$/.test(value)) fail(`cannot read the number "${text}"`);
  return { value, truncated };
}

// CODATA: fixed columns after the line of dashes: the name (60 characters), the value (25), the uncertainty (25), the unit.
function codata() {
  const lines = read(SOURCES.codata.file);
  if (!lines.some((line) => line.includes("2022 CODATA adjustment"))) fail("the CODATA table is not the 2022 adjustment");
  const rule = lines.findIndex((line) => line.startsWith("-----"));
  const [value, uncertainty, unit] = [60, 85, 110];
  const rows = new Map<string, string>();
  for (const line of lines.slice(rule + 1)) if (line.trim()) rows.set(line.slice(0, value).trim(), line);
  return Object.fromEntries(
    CONSTANTS.map((name) => {
      const line = rows.get(name) ?? fail(`"${name}" is not in the CODATA table`);
      const u = line.slice(uncertainty, unit).trim();
      const exact = u === "(exact)";
      const entry = {
        ...number(line.slice(value, uncertainty)),
        uncertainty: exact ? "0" : number(u).value,
        exact,
        unit: line.slice(unit).trim(),
      };
      return [name, entry];
    }),
  );
}

// NUBASE: fixed columns as described at the top of the file (1-based, inclusive). Ground states only.
function nubase() {
  const column = (line: string, from: number, to: number) => line.slice(from - 1, to).trim();
  const found = new Map<string, object>();
  for (const line of read(SOURCES.nubase.file)) {
    if (line.startsWith("#") || !line.trim()) continue;
    const zi = column(line, 5, 8);
    if (!zi.endsWith("0")) continue; // isomers and other levels
    const a = Number(column(line, 1, 3));
    const z = Number(zi.slice(0, 3));
    const halfLife = column(line, 70, 78);
    const entry: Record<string, unknown> = {
      name: column(line, 12, 16),
      massExcess: { value: column(line, 19, 31), uncertainty: column(line, 32, 42), unit: "keV" },
      stable: halfLife === "stbl",
    };
    if (halfLife !== "stbl") entry.halfLife = { value: halfLife, uncertainty: column(line, 82, 88), unit: column(line, 79, 80) };
    found.set(`${a},${z}`, entry);
  }
  return found;
}

// AME: the atomic mass is the last pair of columns, in micro-u, written as "1 008664.91590".
function ame() {
  const found = new Map<string, object>();
  const lines = read(SOURCES.ame.file);
  const start = lines.findIndex((line) => line.startsWith("1N-Z"));
  for (const line of lines.slice(start + 2)) {
    if (line.length < 123) continue;
    const z = Number(line.slice(9, 14));
    const a = Number(line.slice(14, 19));
    found.set(`${a},${z}`, {
      value: line.slice(106, 123).replace(/\s+/g, ""),
      uncertainty: line.slice(123, 135).trim(),
      unit: "micro-u",
    });
  }
  return found;
}

const [masses, properties] = [ame(), nubase()];
const nuclides = Object.fromEntries(
  NUCLIDES.map(([a, z]) => {
    const key = `${a},${z}`;
    const entry = properties.get(key) ?? fail(`nuclide A=${a}, Z=${z} is not in NUBASE`);
    const atomicMass = masses.get(key) ?? fail(`nuclide A=${a}, Z=${z} is not in the AME mass table`);
    const { name, ...rest } = entry as { name: string };
    for (const part of [atomicMass, ...Object.values(rest)]) {
      if (JSON.stringify(part).includes("#")) fail(`${name}: a value is estimated (#), not measured`);
    }
    return [name, { a, z, neutrons: a - z, ...rest, atomicMass }];
  }),
);

const out = {
  about: "Reference values for checking the message's measurements. Generated by `npm run reference` from the tables in this directory; do not edit.",
  sources: SOURCES,
  constants: codata(),
  nuclides,
};
writeFileSync(join(dir, "reference.json"), JSON.stringify(out, null, 2) + "\n");
console.log(`reference.json: ${CONSTANTS.length} constants, ${NUCLIDES.length} nuclides`);
