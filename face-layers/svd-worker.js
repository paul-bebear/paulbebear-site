/* Your face in 10 layers: SVD worker.
   Runs the full singular value decomposition off the main thread so the page never freezes.

   The algorithm is the Golub-Kahan-Reinsch SVD as written in JAMA, the public-domain Java matrix
   package from NIST and The MathWorks (https://math.nist.gov/javanumerics/jama/, version 1.0.3).
   Ported to JavaScript for this page, with every matrix stored column by column (A[j][i] is row i,
   column j) so the inner loops run over contiguous memory. JAMA needs rows >= columns, so a wide
   matrix is transposed first and U and V swapped back at the end.

   In:  { id, m, n, channels: [{ name, data: Float32Array(m*n), row-major }] }
   Out: { id, type: 'channel', name, m, n, r, s: Float64Array(r),
          u: Float32Array(r*m) layer-major (u[i*m + row]), v: Float32Array(r*n) layer-major }
        then { id, type: 'done' }. Errors come back as { id, type: 'error', message }. */
'use strict';
const TINY = Math.pow(2, -966);

function hypot(a, b){
  // Overflow-safe sqrt(a^2 + b^2), as in JAMA's Maths.hypot
  const x = Math.abs(a), y = Math.abs(b);
  if (x > y){ const r = y / x; return x * Math.sqrt(1 + r * r); }
  if (y !== 0){ const r = x / y; return y * Math.sqrt(1 + r * r); }
  return 0;
}

/* Full SVD of an m x n matrix with m >= n. cols[j] is column j (Float64Array of length m), and is overwritten.
   Returns { s (n), U: n columns of length m, V: n columns of length n }, singular values in decreasing order. */
function svdTall(cols, m, n){
  const A = cols;
  const nu = Math.min(m, n);
  const s = new Float64Array(Math.min(m + 1, n));
  const U = Array.from({ length: nu }, () => new Float64Array(m));
  const V = Array.from({ length: n }, () => new Float64Array(n));
  const e = new Float64Array(n);
  const work = new Float64Array(m);
  let i, j, k, t;

  // Reduce A to bidiagonal form, storing the diagonal in s and the super-diagonal in e.
  const nct = Math.min(m - 1, n);
  const nrt = Math.max(0, Math.min(n - 2, m));
  for (k = 0; k < Math.max(nct, nrt); k++){
    const Ak = A[k];
    if (k < nct){
      // Householder transformation for the k-th column.
      s[k] = 0;
      for (i = k; i < m; i++) s[k] = hypot(s[k], Ak[i]);
      if (Math.abs(s[k]) < TINY) s[k] = 0;   // not in JAMA: a denormal norm would wreck the division below
      if (s[k] !== 0){
        if (Ak[k] < 0) s[k] = -s[k];
        for (i = k; i < m; i++) Ak[i] /= s[k];
        Ak[k] += 1;
      }
      s[k] = -s[k];
    }
    for (j = k + 1; j < n; j++){
      const Aj = A[j];
      if (k < nct && s[k] !== 0){
        t = 0;
        for (i = k; i < m; i++) t += Ak[i] * Aj[i];
        t = -t / Ak[k];
        for (i = k; i < m; i++) Aj[i] += t * Ak[i];
      }
      e[j] = Aj[k];
    }
    if (k < nct){
      const Uk = U[k];
      for (i = k; i < m; i++) Uk[i] = Ak[i];
    }
    if (k < nrt){
      // Householder transformation for the k-th row.
      e[k] = 0;
      for (i = k + 1; i < n; i++) e[k] = hypot(e[k], e[i]);
      if (Math.abs(e[k]) < TINY) e[k] = 0;   // same guard for the row step
      if (e[k] !== 0){
        if (e[k + 1] < 0) e[k] = -e[k];
        for (i = k + 1; i < n; i++) e[i] /= e[k];
        e[k + 1] += 1;
      }
      e[k] = -e[k];
      if (k + 1 < m && e[k] !== 0){
        for (i = k + 1; i < m; i++) work[i] = 0;
        for (j = k + 1; j < n; j++){ const Aj = A[j], ej = e[j]; for (i = k + 1; i < m; i++) work[i] += ej * Aj[i]; }
        for (j = k + 1; j < n; j++){
          const Aj = A[j]; t = -e[j] / e[k + 1];
          for (i = k + 1; i < m; i++) Aj[i] += t * work[i];
        }
      }
      for (i = k + 1; i < n; i++) V[k][i] = e[i];
    }
  }

  // Set up the final bidiagonal matrix of order p.
  let p = Math.min(n, m + 1);
  if (nct < n) s[nct] = A[nct][nct];
  if (m < p) s[p - 1] = 0;
  if (nrt + 1 < p) e[nrt] = A[p - 1][nrt];
  e[p - 1] = 0;

  // Generate U.
  for (j = nct; j < nu; j++){
    U[j].fill(0);
    U[j][j] = 1;
  }
  for (k = nct - 1; k >= 0; k--){
    const Uk = U[k];
    if (s[k] !== 0){
      for (j = k + 1; j < nu; j++){
        const Uj = U[j];
        t = 0;
        for (i = k; i < m; i++) t += Uk[i] * Uj[i];
        t = -t / Uk[k];
        for (i = k; i < m; i++) Uj[i] += t * Uk[i];
      }
      for (i = k; i < m; i++) Uk[i] = -Uk[i];
      Uk[k] = 1 + Uk[k];
      for (i = 0; i < k - 1; i++) Uk[i] = 0;
    } else {
      Uk.fill(0);
      Uk[k] = 1;
    }
  }

  // Generate V.
  for (k = n - 1; k >= 0; k--){
    const Vk = V[k];
    if (k < nrt && e[k] !== 0){
      for (j = k + 1; j < nu; j++){
        const Vj = V[j];
        t = 0;
        for (i = k + 1; i < n; i++) t += Vk[i] * Vj[i];
        t = -t / Vk[k + 1];
        for (i = k + 1; i < n; i++) Vj[i] += t * Vk[i];
      }
    }
    Vk.fill(0);
    Vk[k] = 1;
  }

  // Main iteration loop for the singular values.
  const pp = p - 1;
  const eps = Math.pow(2, -52), tiny = TINY;
  let guard = 0;
  while (p > 0){
    if (++guard > 75 * n + 1000) throw new Error('SVD did not converge');
    let kase;
    // Inspect for negligible elements in the s and e arrays.
    for (k = p - 2; k >= -1; k--){
      if (k === -1) break;
      if (Math.abs(e[k]) <= tiny + eps * (Math.abs(s[k]) + Math.abs(s[k + 1]))){ e[k] = 0; break; }
    }
    if (k === p - 2){
      kase = 4;
    } else {
      let ks;
      for (ks = p - 1; ks >= k; ks--){
        if (ks === k) break;
        t = (ks !== p ? Math.abs(e[ks]) : 0) + (ks !== k + 1 ? Math.abs(e[ks - 1]) : 0);
        if (Math.abs(s[ks]) <= tiny + eps * t){ s[ks] = 0; break; }
      }
      if (ks === k) kase = 3;
      else if (ks === p - 1) kase = 1;
      else { kase = 2; k = ks; }
    }
    k++;

    if (kase === 1){
      // Deflate negligible s(p).
      let f = e[p - 2];
      e[p - 2] = 0;
      for (j = p - 2; j >= k; j--){
        t = hypot(s[j], f);
        const cs = s[j] / t, sn = f / t;
        s[j] = t;
        if (j !== k){ f = -sn * e[j - 1]; e[j - 1] = cs * e[j - 1]; }
        const Vj = V[j], Vp = V[p - 1];
        for (i = 0; i < n; i++){ t = cs * Vj[i] + sn * Vp[i]; Vp[i] = -sn * Vj[i] + cs * Vp[i]; Vj[i] = t; }
      }
    } else if (kase === 2){
      // Split at negligible s(k).
      let f = e[k - 1];
      e[k - 1] = 0;
      for (j = k; j < p; j++){
        t = hypot(s[j], f);
        const cs = s[j] / t, sn = f / t;
        s[j] = t;
        f = -sn * e[j];
        e[j] = cs * e[j];
        const Uj = U[j], Uk1 = U[k - 1];
        for (i = 0; i < m; i++){ t = cs * Uj[i] + sn * Uk1[i]; Uk1[i] = -sn * Uj[i] + cs * Uk1[i]; Uj[i] = t; }
      }
    } else if (kase === 3){
      // One QR step.
      const scale = Math.max(Math.abs(s[p - 1]), Math.abs(s[p - 2]), Math.abs(e[p - 2]), Math.abs(s[k]), Math.abs(e[k]));
      const sp = s[p - 1] / scale, spm1 = s[p - 2] / scale, epm1 = e[p - 2] / scale;
      const sk = s[k] / scale, ek = e[k] / scale;
      const b = ((spm1 + sp) * (spm1 - sp) + epm1 * epm1) / 2;
      const c = (sp * epm1) * (sp * epm1);
      let shift = 0;
      if (b !== 0 || c !== 0){
        shift = Math.sqrt(b * b + c);
        if (b < 0) shift = -shift;
        shift = c / (b + shift);
      }
      let f = (sk + sp) * (sk - sp) + shift;
      let g = sk * ek;
      for (j = k; j < p - 1; j++){
        t = hypot(f, g);
        let cs = f / t, sn = g / t;
        if (j !== k) e[j - 1] = t;
        f = cs * s[j] + sn * e[j];
        e[j] = cs * e[j] - sn * s[j];
        g = sn * s[j + 1];
        s[j + 1] = cs * s[j + 1];
        const Vj = V[j], Vj1 = V[j + 1];
        for (i = 0; i < n; i++){ t = cs * Vj[i] + sn * Vj1[i]; Vj1[i] = -sn * Vj[i] + cs * Vj1[i]; Vj[i] = t; }
        t = hypot(f, g);
        cs = f / t; sn = g / t;
        s[j] = t;
        f = cs * e[j] + sn * s[j + 1];
        s[j + 1] = -sn * e[j] + cs * s[j + 1];
        g = sn * e[j + 1];
        e[j + 1] = cs * e[j + 1];
        if (j < m - 1){
          const Uj = U[j], Uj1 = U[j + 1];
          for (i = 0; i < m; i++){ t = cs * Uj[i] + sn * Uj1[i]; Uj1[i] = -sn * Uj[i] + cs * Uj1[i]; Uj[i] = t; }
        }
      }
      e[p - 2] = f;
    } else {
      // Convergence: make the singular value positive, then sort.
      if (s[k] <= 0){
        s[k] = s[k] < 0 ? -s[k] : 0;
        const Vk = V[k];
        for (i = 0; i <= pp; i++) Vk[i] = -Vk[i];
      }
      while (k < pp){
        if (s[k] >= s[k + 1]) break;
        t = s[k]; s[k] = s[k + 1]; s[k + 1] = t;
        if (k < n - 1){ const x = V[k]; V[k] = V[k + 1]; V[k + 1] = x; }
        if (k < m - 1){ const x = U[k]; U[k] = U[k + 1]; U[k + 1] = x; }
        k++;
      }
      p--;
      guard = 0;
    }
  }
  return { s: s.subarray(0, nu), U, V };
}

/* SVD of a row-major m x n Float32Array. Returns r = min(m, n) layers, layer-major, ready for rebuilding. */
function svd(data, m, n){
  const wide = n > m;
  const R = wide ? n : m, C = wide ? m : n;   // the tall matrix we actually decompose
  const cols = Array.from({ length: C }, () => new Float64Array(R));
  if (!wide){ for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) cols[j][i] = data[i * n + j]; }
  else { for (let i = 0; i < m; i++) for (let j = 0; j < n; j++) cols[i][j] = data[i * n + j]; }
  const { s, U, V } = svdTall(cols, R, C);
  const r = C;
  const u = new Float32Array(r * m), v = new Float32Array(r * n);
  for (let l = 0; l < r; l++){
    const left = wide ? V[l] : U[l], right = wide ? U[l] : V[l];
    for (let i = 0; i < m; i++) u[l * m + i] = left[i];
    for (let j = 0; j < n; j++) v[l * n + j] = right[j];
  }
  return { s: Float64Array.from(s), u, v, r };
}

if (typeof self !== 'undefined' && typeof self.postMessage === 'function' && typeof module === 'undefined'){
  self.onmessage = ev => {
    const { id, m, n, channels } = ev.data;
    try {
      for (const ch of channels){
        const t0 = performance.now();
        const { s, u, v, r } = svd(ch.data, m, n);
        self.postMessage({ id, type: 'channel', name: ch.name, m, n, r, s, u, v, ms: performance.now() - t0 }, [s.buffer, u.buffer, v.buffer]);
      }
      self.postMessage({ id, type: 'done' });
    } catch (err){
      self.postMessage({ id, type: 'error', message: String(err && err.message || err) });
    }
  };
}
if (typeof module !== 'undefined') module.exports = { svd };
