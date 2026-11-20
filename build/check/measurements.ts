// Checks every measured range in the message against the reference data (build/check/reference/generated/reference.json).
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
const ref = JSON.parse(readFileSync(resolve(root, "build/check/reference/generated/reference.json"), "utf8"));

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
  // the Sun's velocity relative to the centre: the circular speed plus the Sun's own motion (U, V, W)
  "(÷ (dot (velocity sun galaxy-centre) along-rotation) c)": (() => {
    const v0 = constant("circular velocity at the Sun"), V = constant("Sun's motion along the Galactic rotation (V)");
    return div(q((v0.v + V.v) * 1000, Math.hypot(v0.u, V.u) * 1000), c);
  })(),
  "(÷ (dot (velocity sun galaxy-centre) toward-centre) c)": div(mul(constant("Sun's motion toward the Galactic centre (U)"), q(1000)), c),
  "(÷ (dot (velocity sun galaxy-centre) galactic-pole) c)": div(mul(constant("Sun's motion toward the north Galactic pole (W)"), q(1000)), c),
  // one round of a circle: 2π × distance ÷ speed
  "(÷ (period sun galaxy-centre) planck-time)": div(div(mul(q(2 * Math.PI * 1000 * (648000 / Math.PI) * 149597870700), constant("distance from the Sun to the Galactic centre")), mul(constant("circular velocity at the Sun"), q(1000))), planckTime),
  // the period with the centre's mass alone, squared, over the actual one squared: 4π²R³ ÷ (G M T²) with
  // T = 2πR ÷ V, which is R V² ÷ (G M)
  "(÷ (× 4 (^ π 2) (^ (distance sun galaxy-centre) 3)) (× G (mass galaxy-centre) (^ (period sun galaxy-centre) 2)))": div(
    mul(mul(constant("distance from the Sun to the Galactic centre"), q(1000 * (648000 / Math.PI) * 149597870700)), pow(mul(constant("circular velocity at the Sun"), q(1000)), 2)),
    mul(constant("mass of the Galactic centre"), constant("GM of the Sun"))),
  ...pulsarQuantities(),
  ...cmbAxisQuantities(),
  "(÷ (mass sun) (mass proton))": div(div(constant("GM of the Sun"), G), mp),
  "(÷ (radius sun) planck-length)": div(constant("radius of the Sun"), constant("Planck length")),
  "(÷ (temperature sun) (triple-point water))": div(constant("effective temperature of the Sun"), tWater),
  "(÷ (luminosity sun) (÷ (^ c 5) G))": div(constant("luminosity of the Sun"), div(pow(c, 5), G)),
  "(÷ (count helium sun) (count hydrogen sun))": constant("helium per hydrogen atom in the Sun"),
  "(÷ (axis earth sun) planck-length)": div(constant("semimajor axis of the Earth"), constant("Planck length")),
  "(÷ (period earth sun) planck-time)": div(constant("sidereal year"), planckTime),
  "(÷ (mass earth) (mass proton))": div(div(constant("GM of the Earth"), G), mp),
  // Humans (averages over grown-ups). The world's average body mass (Walpole 2012, no uncertainty given): model
  // uncertainty 5 kg for the year and the averaging. Height: no world average is published; it lies between the
  // averages of the shortest (Guatemalan women) and the tallest (Dutch men) countries, so take their middle, ± 5 cm.
  "(÷ (average u humans (mass u)) (mass proton))": div(widen(constant("average adult body mass"), 5 / 62), mp),
  "(÷ (average u humans (height u)) planck-length)": div(
    q((constant("average height of the shortest adults").v + constant("average height of the tallest adults").v) / 200, 0.05),
    constant("Planck length"),
  ),
  "(÷ (average u humans (temperature u)) (triple-point water))": div(q(constant("human body temperature").v + 273.15, constant("human body temperature").u), tWater),
  // the complete genome has 24 chromosomes (X and Y); a set of 23 has one of them: model uncertainty 70 million (Y is 62 million)
  "(average u humans (apply + (sequence v (genome u) (length (item (strands v) 1)))))": q(Number(ref.other["human genome length"].value), 7e7),
  // DNA (B-form, Kellett 2019, no uncertainty given): base pairs per turn 360°/34.5°, ± 0.3 (10.4–10.6 in solution,
  // about 10 in crystals); rise 3.4 Å ± 0.1 Å.
  "(÷ (× 2 π) (average u dna (twist u)))": q(360 / constant("DNA twist per base pair").v, 0.3),
  "(÷ (average u dna (rise u)) planck-length)": div(q(constant("DNA axial rise per base pair").v * 1e-10, 1e-11), constant("Planck length")),
  "(÷ (× (average u dna (rise u)) (÷ (× 2 π) (average u dna (twist u)))) planck-length)": div(
    mul(q(constant("DNA axial rise per base pair").v * 1e-10, 1e-11), q(360 / constant("DNA twist per base pair").v, 0.3)),
    constant("Planck length"),
  ),
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

// The Galaxy's axes in the axes of the background radiation, from cmb-quadrupole.json (three maps, each with
// three treatments of the Doppler quadrupole): the value is the middle of the nine results, the standard
// uncertainty half their spread.
function cmbAxisQuantities(): Record<string, Q> {
  const cmb = JSON.parse(readFileSync(resolve(root, "build/check/reference/generated/cmb-quadrupole.json"), "utf8"));
  const cases = cmb.maps.flatMap((m: { cases: Record<string, number[]>[] }) => m.cases);
  const out: Record<string, Q> = {};
  ["toward-centre", "along-rotation", "galactic-pole"].forEach((galactic, i) => {
    for (const axis of ["first-axis", "second-axis", "third-axis"]) {
      const v = cases.map((c: Record<string, number[]>) => c[axis][i]);
      const lo = Math.min(...v), hi = Math.max(...v);
      out[`(dot ${galactic} ${axis})`] = q((lo + hi) / 2, (hi - lo) / 2);
    }
  });
  return out;
}

// The decoy version (docs/decoy.html): the Sun, the Galaxy and the pulsar lessons are replaced by lessons about
// Kepler-1647, a pair of stars 1.2 kpc away. The same names then stand for other quantities: `sun` is star A, the
// companion is the star u that orbits it, `earth` is the planet Kepler-1647 b, and the Galaxy and the pulsars are seen
// from there. Uncertainties of the geometry are carried through numerically (one input at a time).
const AU = 149597870700, PC = AU * 648000 / Math.PI, YEAR = 31557600;
const EARTH_RADIUS = 6.3781e6; // IAU 2015 nominal equatorial radius of the Earth, the archive's unit
// a quantity computed by f from independent inputs: the change in f when each input moves by its uncertainty
const propagate = (f: (...x: number[]) => number, ...inputs: Q[]): Q => {
  const x = inputs.map((i) => i.v), v = f(...x);
  return q(v, Math.hypot(...inputs.map((input, i) => f(...x.map((xj, j) => (j === i ? xj + input.u : xj))) - v)));
};
type V3 = [number, number, number];
const dotV = (a: V3, b: V3) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const subV = (a: V3, b: V3): V3 => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const scaleV = (k: number, a: V3): V3 => [k * a[0], k * a[1], k * a[2]];
const unitV = (a: V3): V3 => scaleV(1 / Math.sqrt(dotV(a, a)), a);
const crossV = (a: V3, b: V3): V3 => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const lb = (l: number, b: number): V3 => {
  const [lr, br] = [(l * Math.PI) / 180, (b * Math.PI) / 180];
  return [Math.cos(br) * Math.cos(lr), Math.cos(br) * Math.sin(lr), Math.sin(br)];
};
// equatorial (ICRS) to Galactic directions (the Hipparcos matrix)
const ICRS_TO_GALACTIC: V3[] = [
  [-0.0548755604162154, -0.873437090234885, -0.4838350155487132],
  [0.4941094278755837, -0.4448296299600112, 0.7469822444972189],
  [-0.8676661490190047, -0.1980763734312015, 0.4559837761750669],
];
const toGalactic = (v: V3): V3 => ICRS_TO_GALACTIC.map((row) => dotV(row, v)) as V3;

function decoyQuantities(): Record<string, Q> {
  const k = ref.decoy["Kepler-1647"];
  const n = (x: { value: string; uncertainty: string }) => q(Number(x.value), Number(x.uncertainty));
  const sys = k.system, A = k.starA, B = k.starB;
  const solarMass = div(constant("GM of the Sun"), G), solarRadius = constant("radius of the Sun");
  const planckLength = constant("Planck length"), sigma = constant("Stefan-Boltzmann constant");
  const day = q(86400);
  // the luminosity of a black body: 4π R² σ T⁴, over the Planck power c⁵ ÷ G
  const luminosity = (R: Q, T: Q) => propagate((r, t, s) => 4 * Math.PI * r * r * s * t ** 4, mul(R, solarRadius), T, sigma);
  const out: Record<string, Q> = {
    "(÷ (mass sun) (mass proton))": div(mul(n(A.mass), solarMass), mp),
    "(÷ (radius sun) planck-length)": div(mul(n(A.radius), solarRadius), planckLength),
    "(÷ (temperature sun) (triple-point water))": div(n(A.temperature), tWater),
    "(÷ (luminosity sun) (÷ (^ c 5) G))": div(luminosity(n(A.radius), n(A.temperature)), div(pow(c, 5), G)),
    // the companion, star B: the star u that orbits star A
    "(÷ (mass u) (mass proton))": div(mul(n(B.mass), solarMass), mp),
    "(÷ (radius u) planck-length)": div(mul(n(B.radius), solarRadius), planckLength),
    "(÷ (temperature u) (triple-point water))": div(n(B.temperature), tWater),
    "(÷ (axis u sun) planck-length)": div(mul(n(k.binary.axis), q(AU)), planckLength),
    "(÷ (period u sun) planck-time)": div(mul(n(k.binary.period), day), planckTime),
    // the planet, which goes round both
    "(÷ (axis earth sun) planck-length)": div(mul(n(k.planet.axis), q(AU)), planckLength),
    "(÷ (period earth sun) planck-time)": div(mul(n(k.planet.period), day), planckTime),
    "(÷ (radius earth) planck-length)": div(mul(n(k.planet.radius), q(EARTH_RADIUS)), planckLength),
    // the senders, invented for the decoy (not measured; described on the decoy page): beings of a moon of the
    // planet, tall and slender in its weaker pull (160 ± 5 kg, 3.1 ± 0.05 m), cooler in its dimmer light
    // (298 ± 1 K), with a genome of 19 DNA molecules (6.4 ± 0.07 thousand million base pairs)
    "(÷ (average u humans (mass u)) (mass proton))": div(q(160, 5), mp),
    "(÷ (average u humans (height u)) planck-length)": div(q(3.1, 0.05), planckLength),
    "(÷ (average u humans (temperature u)) (triple-point water))": div(q(298, 1), tWater),
    "(average u humans (apply + (sequence v (genome u) (length (item (strands v) 1)))))": q(6.4e9, 7e7),
  };

  // The Galaxy seen from Kepler-1647. Positions in pc and velocities in km/s, in the Sun's Galactic axes; the
  // decoy's own axes are the direction to the centre, the direction of a circular orbit there, and their cross.
  const R0 = constant("distance from the Sun to the Galactic centre"), Vc = constant("circular velocity at the Sun");
  const U = constant("Sun's motion toward the Galactic centre (U)"), Vs = constant("Sun's motion along the Galactic rotation (V)");
  const W = constant("Sun's motion toward the north Galactic pole (W)");
  const dist = n(sys.distance), pmRA = n(sys.properMotionRA), pmDec = n(sys.properMotionDec), rv = n(sys.radialVelocity);
  const [ra, dec] = [(Number(sys.rightAscension) * Math.PI) / 180, (Number(sys.declination) * Math.PI) / 180];
  const here = (d: number): V3 => scaleV(d, lb(Number(sys.longitude), Number(sys.latitude)));
  const axes = (r0kpc: number, d: number) => {
    const t = unitV(subV([r0kpc * 1000, 0, 0], here(d)));
    const r = unitV(crossV([0, 0, 1], t));
    return { t, r, p: crossV(t, r) };
  };
  // the star's velocity relative to the centre: its own (from the proper motion and the radial velocity) plus the Sun's
  const velocity = (d: number, a: number, b: number, v: number, vc: number, u: number, vs: number, w: number): V3 => {
    const k = 4.740470446e-3 * d; // km/s per mas/yr at d pc
    const eq: V3 = [
      v * Math.cos(dec) * Math.cos(ra) - k * a * Math.sin(ra) - k * b * Math.sin(dec) * Math.cos(ra),
      v * Math.cos(dec) * Math.sin(ra) + k * a * Math.cos(ra) - k * b * Math.sin(dec) * Math.sin(ra),
      v * Math.sin(dec) + k * b * Math.cos(dec),
    ];
    const g = toGalactic(eq);
    return [g[0] + u, g[1] + vc + vs, g[2] + w];
  };
  const fromCentre = (r0: number, d: number) => Math.sqrt(dotV(subV([r0 * 1000, 0, 0], here(d)), subV([r0 * 1000, 0, 0], here(d))));
  const rc = propagate(fromCentre, R0, dist);
  out["(÷ (distance sun galaxy-centre) planck-length)"] = div(mul(rc, q(PC)), planckLength);
  // one round of a circle at the circular speed (the rotation curve is flat here)
  out["(÷ (period sun galaxy-centre) planck-time)"] = div(div(mul(q(2 * Math.PI * PC), rc), mul(Vc, q(1000))), planckTime);
  out["(÷ (× 4 (^ π 2) (^ (distance sun galaxy-centre) 3)) (× G (mass galaxy-centre) (^ (period sun galaxy-centre) 2)))"] = div(
    mul(mul(rc, q(PC)), pow(mul(Vc, q(1000)), 2)), mul(constant("mass of the Galactic centre"), constant("GM of the Sun")));
  const component = (axis: "t" | "r" | "p") => propagate(
    (r0, d, a, b, v, vc, u, vs, w) => dotV(velocity(d, a, b, v, vc, u, vs, w), axes(r0, d)[axis]) * 1000 / c.v,
    R0, dist, pmRA, pmDec, rv, Vc, U, Vs, W);
  out["(÷ (dot (velocity sun galaxy-centre) along-rotation) c)"] = component("r");
  out["(÷ (dot (velocity sun galaxy-centre) toward-centre) c)"] = component("t");
  out["(÷ (dot (velocity sun galaxy-centre) galactic-pole) c)"] = component("p");
  // the decoy's axes in the axes of the background radiation: as for the Sun, the middle and half the spread of the
  // nine results, with the change from R0's uncertainty added
  const cmb = JSON.parse(readFileSync(resolve(root, "build/check/reference/generated/cmb-quadrupole.json"), "utf8"));
  const cases = cmb.maps.flatMap((m: { cases: Record<string, V3>[] }) => m.cases);
  const decoyAxes = axes(R0.v, dist.v), shifted = axes(R0.v + R0.u, dist.v);
  ([["toward-centre", "t"], ["along-rotation", "r"], ["galactic-pole", "p"]] as const).forEach(([galactic, key]) => {
    for (const axis of ["first-axis", "second-axis", "third-axis"]) {
      const values = cases.map((cc: Record<string, V3>) => dotV(decoyAxes[key], cc[axis]));
      const lo = Math.min(...values), hi = Math.max(...values);
      const shift = Math.abs(dotV(shifted[key], cases[0][axis]) - dotV(decoyAxes[key], cases[0][axis]));
      out[`(dot ${galactic} ${axis})`] = q((lo + hi) / 2, Math.hypot((hi - lo) / 2, shift));
    }
  });

  // The pulsars seen from Kepler-1647: their directions in its axes, and their periods as they were when the light
  // that reaches it left them (earlier or later than the light that reaches the Sun). A pulsar's distance is uncertain
  // by the difference between the catalogue's distance and the one from its dispersion measure; the period's change is
  // extrapolated linearly from the slowing, with a model uncertainty of a quarter of the change (the slowing itself
  // changes with time), and the slowing is given a model uncertainty as large as the relative change of the period.
  // From Kepler-1647 the Crab has not yet been seen to explode, so `crab-pulsar` names PSR B1951+32 there.
  const NAMES: Record<string, string> = {
    "J1952+3252": "crab-pulsar", "J0835-4510": "vela-pulsar", "J0437-4715": "pulsar-j0437",
    "J1939+2134": "pulsar-j1939", "J0332+5434": "pulsar-j0332", "J1921+2153": "pulsar-j1921",
  };
  const year = constant("sidereal year").v;
  const { t, r, p } = decoyAxes;
  for (const [j, name] of Object.entries(NAMES)) {
    const ps = ref.pulsars[j] ?? ref.decoy.pulsars[j];
    const P0 = Number(ps.period.value), P0u = Number(ps.period.uncertainty), P1 = Number(ps.slowing.value);
    const toward = lb(Number(ps.longitude), Number(ps.latitude));
    const [d1, d2] = [Number(ps.distance.value) * 1000, Number(ps.distanceFromDispersion.value) * 1000];
    const seen = (d: number) => {
      const from = subV(scaleV(d, toward), here(dist.v));
      const delay = ((Math.sqrt(dotV(from, from)) - d) * PC) / c.v; // seconds by which the light here is older
      const u = unitV(from);
      return { dir: [dotV(u, t), dotV(u, r), dotV(u, p)], period: P0 - P1 * delay };
    };
    const [a, b] = [seen(d1), seen(d2)];
    const change = P0 - a.period;
    out[`(÷ (pulse-period ${name}) planck-time)`] = div(q(a.period, Math.hypot(P0u, P1 * 40 * year, a.period - b.period, change / 4)), planckTime);
    out[`(slowing ${name})`] = widen(q(P1), Math.hypot(0.02, change / P0));
    ["toward-centre", "along-rotation", "galactic-pole"].forEach((axis, i) => {
      out[`(dot (direction-from sun ${name}) ${axis})`] = q(a.dir[i], Math.hypot(0.01, a.dir[i] - b.dir[i]));
    });
  }
  return out;
}
export const DECOY: Record<string, Q> = { ...QUANTITIES, ...decoyQuantities() };

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
    case "neg": return -a[0];
    case "÷": return a[0] / a[1];
    case "^": return a[0] ** a[1];
  }
  return undefined;
};


// Checks the message given as text (message.txt): a report line for every range, and the number of failures.
// version: "full" (the reference values of the Sun, the Galaxy seen from it …) or "decoy" (those of Kepler-1647).
export function checkMeasurements(text: string, version: "full" | "decoy" = "full"): { report: string[]; failures: number; checked: number } {
const QUANTITY = version === "decoy" ? DECOY : QUANTITIES;
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
// the ranges of an observed sentence: the sentence itself, or ranges inside ∃ and `and` (the decoy's companion star)
const ranges = (n: Node): Node[][] => {
  if (!Array.isArray(n)) return [];
  if (n[0] === "<" || n[0] === ">") return [n];
  if (n[0] === "∃") return ranges(n[3]);
  if (n[0] === "and") return n.slice(1).flatMap(ranges);
  return [];
};
for (const range of sentences.flatMap((s) => (Array.isArray(s) && s[0] === "observed" ? ranges(s[1]) : []))) {
  const [rel, ...args] = range;
  if (args.length !== 3) continue;
  let [low, mid, high] = args.map((a) => a);
  if (rel === ">") [low, high] = [high, low];
  const lo = exact(low), hi = exact(high);
  if (lo === undefined || hi === undefined) continue; // an order between quantities, not a range
  checked++;
  const key = show(mid);
  const x = QUANTITY[key];
  if (!x) { failures++; report.push(`NO REFERENCE  ${key}: add a formula to build/check/measurements.ts`); continue; }
  // a dot of two directions lies between −1 and 1: a bound at that limit cannot fail
  const limit = key.startsWith("(dot ") ? 1 : Infinity;
  const below = lo <= -limit ? Infinity : (x.v - lo) / x.u, above = hi >= limit ? Infinity : (hi - x.v) / x.u;
  const ok = x.v > lo && x.v < hi && (x.u === 0 || (below >= MARGIN && above >= MARGIN));
  if (!ok) failures++;
  const sig = (n: number) => (x.u === 0 ? "exact" : n === Infinity ? "limit" : n > 1e6 ? ">1e6 σ" : `${n.toFixed(1)} σ`);
  report.push(`${ok ? "ok  " : "FAIL"}  ${key}\n      ${lo.toPrecision(7)} < ${x.v.toPrecision(9)} ± ${x.u.toPrecision(2)} < ${hi.toPrecision(7)}   margins ${sig(below)}, ${sig(above)}`);
}
return { report, failures, checked };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  let failing = 0;
  for (const [version, file] of [["full", "docs/message.txt"], ["decoy", "docs/decoy/message.txt"]] as const) {
    const { report, failures, checked } = checkMeasurements(readFileSync(resolve(root, file), "utf8"), version);
    console.log(`${version}:\n${report.join("\n")}`);
    console.log(`\n${version}: ${checked} ranges, ${failures} failing (each bound must be at least ${MARGIN} standard uncertainties from the reference value)\n`);
    failing += failures;
  }
  process.exit(failing ? 1 : 0);
}
