/* verify.js — check a Lightning receipt without trusting anyone.
   bolt11 checksum, signer node recovered from the invoice signature (secp256k1),
   and sha256(preimage) == payment_hash. No network, no dependencies.
   Kept by vera-diade (Vera), theattempt.org. Public domain. */
(function (root) {
  "use strict";
  const B32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l";
  const P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2Fn;
  const N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141n;
  const G = [0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798n,
             0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8n];
  const mod = (a, m = P) => { const r = a % m; return r >= 0n ? r : r + m; };
  function inv(a, m) {
    let t = 0n, nt = 1n, r = m, nr = mod(a, m);
    while (nr !== 0n) { const q = r / nr; [t, nt] = [nt, t - q * nt]; [r, nr] = [nr, r - q * nr]; }
    if (r !== 1n) throw new Error("not invertible");
    return mod(t, m);
  }
  function powmod(b, e, m) { let r = 1n; b = mod(b, m); while (e > 0n) { if (e & 1n) r = r * b % m; b = b * b % m; e >>= 1n; } return r; }
  const INF = [0n, 1n, 0n];
  function dbl(p) {
    const [X, Y, Z] = p;
    if (Z === 0n || Y === 0n) return INF;
    const YY = mod(Y * Y), S = mod(4n * X * YY), M = mod(3n * X * X);
    const X3 = mod(M * M - 2n * S);
    return [X3, mod(M * (S - X3) - 8n * YY * YY), mod(2n * Y * Z)];
  }
  function add(p, q) {
    if (p[2] === 0n) return q;
    if (q[2] === 0n) return p;
    const [X1, Y1, Z1] = p, [X2, Y2, Z2] = q;
    const Z1Z1 = mod(Z1 * Z1), Z2Z2 = mod(Z2 * Z2);
    const U1 = mod(X1 * Z2Z2), U2 = mod(X2 * Z1Z1), S1 = mod(Y1 * Z2 * Z2Z2), S2 = mod(Y2 * Z1 * Z1Z1);
    if (U1 === U2) return S1 === S2 ? dbl(p) : INF;
    const H = mod(U2 - U1), R = mod(S2 - S1), HH = mod(H * H), HHH = mod(H * HH), V = mod(U1 * HH);
    const X3 = mod(R * R - HHH - 2n * V);
    return [X3, mod(R * (V - X3) - S1 * HHH), mod(H * Z1 * Z2)];
  }
  function twoMul(k1, a, k2, b) { // k1*a + k2*b (Shamir), affine in, affine out
    const A = [a[0], a[1], 1n], B = [b[0], b[1], 1n], AB = add(A, B);
    let R = INF;
    const n = Math.max(k1.toString(2).length, k2.toString(2).length);
    for (let i = n - 1; i >= 0; i--) {
      R = dbl(R);
      const x = (k1 >> BigInt(i)) & 1n, y = (k2 >> BigInt(i)) & 1n;
      if (x && y) R = add(R, AB); else if (x) R = add(R, A); else if (y) R = add(R, B);
    }
    if (R[2] === 0n) return null;
    const zi = inv(R[2], P), zi2 = mod(zi * zi);
    return [mod(R[0] * zi2), mod(R[1] * zi2 * zi)];
  }
  function polymod(values) {
    const GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3];
    let chk = 1;
    for (const v of values) {
      const b = chk >>> 25;
      chk = ((chk & 0x1ffffff) << 5) ^ v;
      for (let i = 0; i < 5; i++) if ((b >>> i) & 1) chk ^= GEN[i];
    }
    return chk;
  }
  function wordsToBytes(w, pad) {
    let acc = 0, bits = 0; const out = [];
    for (const v of w) { acc = ((acc << 5) | v) & 0xffff; bits += 5; while (bits >= 8) { bits -= 8; out.push((acc >> bits) & 0xff); } }
    if (pad && bits) out.push((acc << (8 - bits)) & 0xff);
    return Uint8Array.from(out);
  }
  const hex = (u8) => Array.from(u8, (b) => b.toString(16).padStart(2, "0")).join("");
  const big = (u8) => BigInt("0x" + (hex(u8) || "0"));
  async function sha256(u8) {
    const c = (root.crypto && root.crypto.subtle) ? root.crypto : (typeof require !== "undefined" ? require("crypto").webcrypto : null);
    return new Uint8Array(await c.subtle.digest("SHA-256", u8));
  }
  const MULT = { m: 100000000n, u: 100000n, n: 100n };

  async function decode(invoice) {
    const t = String(invoice || "").trim().toLowerCase().replace(/^lightning:/, "");
    const i = t.lastIndexOf("1");
    if (!t.startsWith("ln") || i < 3 || t.length - i - 1 < 7 + 104 + 6) return { error: "not a complete bolt11 invoice (the signature at the end is missing)" };
    const hrp = t.slice(0, i), data = t.slice(i + 1), w = [];
    for (const ch of data) { const v = B32.indexOf(ch); if (v < 0) return { error: "character outside the bech32 alphabet: " + ch }; w.push(v); }
    const exp = []; for (const ch of hrp) exp.push(ch.charCodeAt(0) >> 5); exp.push(0); for (const ch of hrp) exp.push(ch.charCodeAt(0) & 31);
    if (polymod(exp.concat(w)) !== 1) return { error: "bech32 checksum is wrong: the invoice was altered or cut" };
    const words = w.slice(0, -6), body = words.slice(0, -104), sig = wordsToBytes(words.slice(-104), false);
    const r = big(sig.slice(0, 32)), s = big(sig.slice(32, 64)), rec = sig[64];
    if (!(r > 0n && r < N && s > 0n && s < N) || rec > 3) return { error: "signature out of range" };
    const hrpBytes = new TextEncoder().encode(hrp), bodyBytes = wordsToBytes(body, true);
    const msg = new Uint8Array(hrpBytes.length + bodyBytes.length); msg.set(hrpBytes); msg.set(bodyBytes, hrpBytes.length);
    const z = big(await sha256(msg));
    const x = r + (rec >= 2 ? N : 0n);
    const c = mod(x * x * x + 7n), y0 = powmod(c, (P + 1n) / 4n, P);
    if (x >= P || mod(y0 * y0) !== c) return { error: "signature does not point to the curve" };
    const y = ((y0 & 1n) === BigInt(rec & 1)) ? y0 : P - y0;
    const ri = inv(r, N), q = twoMul(mod(s * ri, N), [x, y], mod(-z * ri, N), G);
    if (!q) return { error: "signature recovers to nothing" };
    const signer = ((q[1] & 1n) ? "03" : "02") + q[0].toString(16).padStart(64, "0");
    let j = 7, paymentHash = null, declared = null, expiry = 3600;
    let ts = 0; for (let k = 0; k < 7; k++) ts = ts * 32 + body[k];
    while (j + 3 <= body.length) {
      const type = B32[body[j]], len = (body[j + 1] << 5) | body[j + 2]; j += 3;
      const val = body.slice(j, j + len);
      if (type === "p" && len === 52) paymentHash = hex(wordsToBytes(val, false).slice(0, 32));
      if (type === "n" && len === 53) declared = hex(wordsToBytes(val, false).slice(0, 33));
      if (type === "x") { let e = 0; for (const v of val) e = e * 32 + v; expiry = e; }
      j += len;
    }
    if (declared && declared !== signer) return { error: "FORGED: the key declared in the invoice (" + declared.slice(0, 16) + "…) is not the key that signed it (" + signer.slice(0, 16) + "…)" };
    if (!paymentHash) return { error: "the invoice carries no payment hash" };
    const m = hrp.match(/^ln[a-z]+?(\d+)([munp]?)$/);
    let msat = null;
    if (m) { const d = BigInt(m[1]); msat = m[2] === "p" ? d / 10n : m[2] ? d * MULT[m[2]] : d * 100000000000n; }
    return { signer, paymentHash, sat: msat === null ? null : Number(msat / 1000n), created: ts, expiry, network: hrp.replace(/\d.*$/, "").replace(/[munp]$/, "") };
  }

  // verdict names match /receipts/receipts.json
  async function check(invoice, preimage, custodianNode) {
    const d = await decode(invoice);
    if (d.error) return { verdict: "UNREADABLE", why: d.error };
    const pre = String(preimage || "").trim().toLowerCase();
    const same = custodianNode ? d.signer === String(custodianNode).toLowerCase() : null;
    if (/^[0-9a-f]{64}$/.test(pre)) {
      const bytes = new Uint8Array(pre.match(/../g).map((h) => parseInt(h, 16)));
      const got = hex(await sha256(bytes));
      if (got === d.paymentHash) return Object.assign({ verdict: "RECEIPT", why: "sha256(preimage) equals the payment hash inside the invoice", sameCustodian: same }, d);
      return Object.assign({ verdict: "NO-MATCH", why: "these 64 characters do not open this invoice", sameCustodian: same }, d);
    }
    const what = !pre ? "nothing" : (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(pre) ? "a UUID" : pre.length + " characters that are not a preimage");
    if (same) return Object.assign({ verdict: "SAME-CUSTODIAN", why: "no preimage (" + what + "), and the invoice was signed by the payer's own custodian: an internal ledger entry, no witness outside the custodian", sameCustodian: true }, d);
    return Object.assign({ verdict: "NO-RECEIPT", why: "no preimage (" + what + ")", sameCustodian: same }, d);
  }

  const api = { decode, check };
  root.LNReceipt = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
