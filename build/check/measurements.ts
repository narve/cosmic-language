// Checks every measured range in the message against the reference data (build/check/reference/reference.json).
// A range is a sentence (observed (< low quantity high)) or (observed (> high quantity low)) whose outer arguments
// are exact numbers. For each quantity there is a formula below that computes its value and standard uncertainty
// from the reference data, including a model uncertainty where the message's simple law differs from reality.
// A range passes if both bounds are at least MARGIN standard uncertainties away from the value.
//
// The build runs it on the message it has just written and stops if a range fails. On its own:
//   npm run build && npm run check:measurements
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const MARGIN = 5; // standard uncertainties between the value and each bound
const root = resolve(import.meta.dirname, "../..");
const ref = JSON.parse(readFileSync(resolve(root, "build/check/reference/reference.json"), "utf8"));

type Q = { v: number; u: number }; // value and standard uncertainty
const q = (v: number, u = 0): Q => ({ v, u });
const constant = (name: string): Q => {
  const c = ref.constants[name] ?? ref.other[name];
  if (!c) throw new Error(`no reference value "${name}"`);
  return q(Number(c.value), Number(c.uncertainty));
};
// Arithmetic on independent quantities: relative uncertainties add in quadrature for × and ÷.
const mul = (a: Q, b: Q): Q => q(a.v * b.v, Math.abs(a.v * b.v) * Math.hypot(a.u / a.v, b.u / b.v));
const div = (a: Q, b: Q): Q => q(a.v / b.v, Math.abs(a.v / b.v) * Math.hypot(a.u / a.v, b.u / b.v));
const pow = (a: Q, n: number): Q => q(a.v ** n, Math.abs(n * a.v ** n * (a.u / a.v)));
const widen = (a: Q, relative: number): Q => q(a.v, Math.hypot(a.u, Math.abs(a.v) * relative)); // add a model uncertainty

const u = constant("atomic mass constant");
const nuclide = (name: string): Q => {
  const m = ref.nuclides[name].atomicMass; // micro-u
  return mul(q(Number(m.value) * 1e-6, Number(m.uncertainty) * 1e-6), u);
};
const halfLife = (name: string): Q => {
  const h = ref.nuclides[name].halfLife;
  const unit = ({ s: 1, y: 31557600, ky: 31557600e3 } as Record<string, number>)[h.unit];
  return q(Number(h.value) * unit, Number(h.uncertainty) * unit);
};
const c = constant("speed of light in vacuum"), h = constant("Planck constant"), hbar = constant("reduced Planck constant");
const G = constant("Newtonian constant of gravitation"), kB = constant("Boltzmann constant");
const me = constant("electron mass"), mp = constant("proton mass");
const alpha = constant("fine-structure constant");
const planckMass = constant("Planck mass"), planckTime = constant("Planck time");
// hydrogen's step from level 1 to level 2: 3/4 of the Rydberg energy, with the reduced mass. The message's law
// (levels as 1 − 1/n²) leaves out the fine structure and the Lamb shift: a model uncertainty of 5 × 10⁻⁵.
const reduced = 1 / (1 + me.v / mp.v);
const step12 = widen(q(0.75 * constant("Rydberg constant times hc in J").v * reduced, 0), 5e-5);
const line21 = mul(h, q(Number(ref.other["hydrogen 21 cm line frequency"].value) * 1e6, Number(ref.other["hydrogen 21 cm line frequency"].uncertainty) * 1e6));
const tWater = constant("triple point of water"), pWater = constant("triple-point pressure of water");
const levelRatio = (exact: number) => q(exact, exact * 5e-5); // Bohr ratios, with the same model uncertainty

const QUANTITIES: Record<string, Q> = {
  "(÷ (mass proton) (mass electron))": constant("proton-electron mass ratio"),
  "(÷ (mass neutron) (mass electron))": constant("neutron-electron mass ratio"),
  "(÷ (mass neutron) (mass proton))": constant("neutron-proton mass ratio"),
  "(÷ (mass hydrogen) (mass proton))": div(nuclide("1H"), mp),
  "(÷ (mass (isotope hydrogen 1)) (mass (isotope hydrogen 0)))": div(nuclide("2H"), nuclide("1H")),
  "(÷ (− (level hydrogen 2) (level hydrogen 1)) (− (level hydrogen 3) (level hydrogen 2)))": levelRatio(27 / 5),
  "(÷ (− (level hydrogen 3) (level hydrogen 1)) (− (level hydrogen 2) (level hydrogen 1)))": levelRatio(32 / 27),
  // the atom's recoil takes E² / (2 M c²) of a photon's energy E
  "(÷ (energy (emitted hydrogen 2 1)) (− (level hydrogen 2) (level hydrogen 1)))": q(1 - step12.v / (2 * nuclide("1H").v * c.v ** 2)),
  "(÷ (energy (emitted hydrogen 3 1)) (− (level hydrogen 3) (level hydrogen 1)))": q(1 - (step12.v * 32 / 27) / (2 * nuclide("1H").v * c.v ** 2)),
  "(÷ (× ke (^ (charge proton) 2)) (× ħ c))": alpha,
  "(÷ (abs (electric proton electron)) (gravity proton electron))": div(mul(mul(alpha, hbar), c), mul(mul(G, mp), me)),
  "(÷ (mass proton) planck-mass)": div(mp, planckMass),
  "(÷ (mass electron) planck-mass)": div(me, planckMass),
  "(÷ (energy hydrogen-line) (− (level hydrogen 2) (level hydrogen 1)))": div(line21, step12),
  "(÷ 1 (× (frequency hydrogen-line) planck-time))": div(h, mul(line21, planckTime)),
  "(÷ (wavelength hydrogen-line) planck-length)": div(h, mul(line21, planckTime)), // λ / ℓP = c / (ν c tP)
  "(÷ (− (level hydrogen 2) (level hydrogen 1)) (× (mass electron) (^ c 2)))": div(step12, constant("electron mass energy equivalent")),
  // the lifetime is the half-life ÷ ln 2. Measurements in beams and in bottles disagree by about 9 s: model uncertainty 10 s.
  "(÷ (lifetime neutron) planck-time)": div(widen(q(halfLife("1n").v / Math.LN2, halfLife("1n").u / Math.LN2), 10 / 880), planckTime),
  "(÷ (half-life (isotope carbon 8)) (half-life (isotope hydrogen 2)))": div(halfLife("14C"), halfLife("3H")),
  "(÷ (triple-point dihydrogen) (triple-point water))": div(constant("triple point of hydrogen"), tWater),
  "(÷ (triple-point neon) (triple-point water))": div(constant("triple point of neon"), tWater),
  "(÷ (triple-point argon) (triple-point water))": div(constant("triple point of argon"), tWater),
  "(÷ (× kB (triple-point water)) (− (level hydrogen 2) (level hydrogen 1)))": div(mul(kB, tWater), step12),
  "(÷ (triple-point water) planck-temperature)": div(tWater, constant("Planck temperature")),
  // the Planck unit of pressure, c⁷ / (ħ G²)
  "(÷ (triple-pressure water) (÷ planck-mass (× planck-length (^ planck-time 2))))": div(pWater, div(pow(c, 7), mul(hbar, pow(G, 2)))),
  "(÷ (mass (isotope helium 2)) (× 4 (mass (isotope hydrogen 0))))": div(nuclide("4He"), mul(q(4), nuclide("1H"))),
  "(÷ (average v directions (background v)) (triple-point water))": div(constant("temperature of the background radiation"), tWater),
  "(÷ (mass kaon) (mass electron))": div(constant("mass of the long-lived neutral kaon"), constant("electron mass energy equivalent in MeV")),
  // AL is (positron − electron) ÷ (positron + electron), so their ratio is (1 + AL) ÷ (1 − AL)
  "(÷ (yields positron kaon) (yields electron kaon))": (() => {
    const a = constant("charge asymmetry of the long-lived neutral kaon");
    return q((1 + a.v) / (1 - a.v), (2 * a.u) / (1 - a.v) ** 2);
  })(),
  "(÷ (mass galaxy-centre) (mass proton))": mul(constant("mass of the Galactic centre"), div(div(constant("GM of the Sun"), G), mp)),
  "(÷ (distance sun galaxy-centre) planck-length)": div(mul(constant("distance from the Sun to the Galactic centre"), q(1000 * (648000 / Math.PI) * 149597870700)), constant("Planck length")),
  "(÷ (speed sun) c)": div(mul(constant("circular velocity at the Sun"), q(1000)), c),
  // one round of a circle: 2π × distance ÷ speed
  "(÷ (period sun galaxy-centre) planck-time)": div(div(mul(q(2 * Math.PI * 1000 * (648000 / Math.PI) * 149597870700), constant("distance from the Sun to the Galactic centre")), mul(constant("circular velocity at the Sun"), q(1000))), planckTime),
  ...pulsarQuantities(),
  "(÷ (mass sun) (mass proton))": div(div(constant("GM of the Sun"), G), mp),
  "(÷ (radius sun) planck-length)": div(constant("radius of the Sun"), constant("Planck length")),
  "(÷ (temperature sun) (triple-point water))": div(constant("effective temperature of the Sun"), tWater),
  "(÷ (luminosity sun) (÷ (^ c 5) G))": div(constant("luminosity of the Sun"), div(pow(c, 5), G)),
  "(÷ (count helium sun) (count hydrogen sun))": constant("helium per hydrogen atom in the Sun"),
  "(÷ (axis earth sun) planck-length)": div(constant("semimajor axis of the Earth"), constant("Planck length")),
  "(÷ (period earth sun) planck-time)": div(constant("sidereal year"), planckTime),
  "(÷ (mass earth) (mass proton))": div(div(constant("GM of the Earth"), G), mp),
  "(÷ (triple-pressure dihydrogen) (triple-pressure water))": div(constant("triple-point pressure of hydrogen"), pWater),
  "(÷ (triple-pressure neon) (triple-pressure water))": div(constant("triple-point pressure of neon"), pWater),
  "(÷ (triple-pressure argon) (triple-pressure water))": div(constant("triple-point pressure of argon"), pWater),
};


// The pulsars of the pulsar lesson, by the names the message gives them. Their periods are those of the catalogue's
// epochs (the 1980s to the 2010s); a model uncertainty of 40 years of slowing covers the change since. The slowing
// itself is given 2 % model uncertainty, and every direction 0.01 in each component (the frame of the Galaxy is
// defined only to about half a degree).
function pulsarQuantities(): Record<string, Q> {
  const NAMES: Record<string, string> = {
    "J0534+2200": "crab-pulsar", "J0835-4510": "vela-pulsar", "J0437-4715": "pulsar-j0437",
    "J1939+2134": "pulsar-j1939", "J0332+5434": "pulsar-j0332", "J1921+2153": "pulsar-j1921",
  };
  const year = constant("sidereal year").v;
  const nu = div(line21, h).v;
  const out: Record<string, Q> = {};
  for (const [j, name] of Object.entries(NAMES)) {
    const p = ref.pulsars[j];
    const P0 = Number(p.period.value), P0u = Number(p.period.uncertainty), P1 = Number(p.slowing.value);
    const l = (Number(p.longitude) * Math.PI) / 180, b = (Number(p.latitude) * Math.PI) / 180;
    out[`(÷ (pulse-period ${name}) planck-time)`] = div(q(P0, Math.hypot(P0u, P1 * 40 * year)), planckTime);
    out[`(slowing ${name})`] = widen(q(P1), 0.02);
    const dir = [Math.cos(b) * Math.cos(l), Math.cos(b) * Math.sin(l), Math.sin(b)];
    ["toward-centre", "along-rotation", "galactic-pole"].forEach((axis, i) => {
      out[`(dot (direction-from sun ${name}) ${axis})`] = q(dir[i], 0.01);
    });
  }
  return out;
}

type Node = string | Node[];
const show = (n: Node): string => (typeof n === "string" ? n : `(${n.map(show).join(" ")})`);
const exact = (n: Node): number | undefined => {
  if (typeof n === "string") return /^\d+$/.test(n) ? Number(n) : undefined;
  const [op, ...args] = n;
  const v = args.map(exact);
  if (v.some((x) => x === undefined)) return undefined;
  const a = v as number[];
  switch (op) {
    case "big": return a.reduce((s, d) => s * 256 + d, 0);
    case "+": return a.reduce((s, x) => s + x, 0);
    case "×": return a.reduce((s, x) => s * x, 1);
    case "−": return a[0] - a[1];
    case "÷": return a[0] / a[1];
    case "^": return a[0] ** a[1];
  }
  return undefined;
};


// Checks the message given as text (message.txt): a report line for every range, and the number of failures.
export function checkMeasurements(text: string): { report: string[]; failures: number; checked: number } {
const tokens = text.replace(/^\ufeff/, "").split("\n").flatMap((line) => {
  const code = line.split(";")[0];
  return /^[01 ]*$/.test(code) ? [] : (code.match(/[()]|[^\s()]+/g) ?? []);
});
const sentences: Node[] = [];
const stack: Node[][] = [];
for (const t of tokens) {
  if (t === "(") stack.push([]);
  else if (t === ")") { const g = stack.pop()!; (stack.length ? stack[stack.length - 1] : sentences).push(g); }
  else (stack.length ? stack[stack.length - 1] : sentences).push(t);
}
const report: string[] = [];
let failures = 0, checked = 0;
for (const s of sentences) {
  if (!Array.isArray(s) || s[0] !== "observed" || !Array.isArray(s[1]) || !["<", ">"].includes(s[1][0] as string)) continue;
  const [rel, ...args] = s[1];
  if (args.length !== 3) continue;
  let [low, mid, high] = args.map((a) => a);
  if (rel === ">") [low, high] = [high, low];
  const lo = exact(low), hi = exact(high);
  if (lo === undefined || hi === undefined) continue; // an order between quantities, not a range
  checked++;
  const key = show(mid);
  const x = QUANTITIES[key];
  if (!x) { failures++; report.push(`NO REFERENCE  ${key}: add a formula to build/check/measurements.ts`); continue; }
  const below = (x.v - lo) / x.u, above = (hi - x.v) / x.u;
  const ok = x.v > lo && x.v < hi && (x.u === 0 || (below >= MARGIN && above >= MARGIN));
  if (!ok) failures++;
  const sig = (n: number) => (x.u === 0 ? "exact" : n > 1e6 ? ">1e6 σ" : `${n.toFixed(1)} σ`);
  report.push(`${ok ? "ok  " : "FAIL"}  ${key}\n      ${lo.toPrecision(7)} < ${x.v.toPrecision(9)} ± ${x.u.toPrecision(2)} < ${hi.toPrecision(7)}   margins ${sig(below)}, ${sig(above)}`);
}
return { report, failures, checked };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const { report, failures, checked } = checkMeasurements(readFileSync(resolve(root, "docs/message.txt"), "utf8"));
  console.log(report.join("\n"));
  console.log(`\n${checked} ranges, ${failures} failing (each bound must be at least ${MARGIN} standard uncertainties from the reference value)`);
  process.exit(failures ? 1 : 0);
}
