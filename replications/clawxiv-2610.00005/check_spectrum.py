# USCITA ATTESA:
# srg(99,14,1,2): eigenvalues from x^2=12-x => x=3 or x=-4
# A^2 equation: A^2 = 12I - A + 2J  CHECK: (k-mu)=12, (lam-mu)=-1, mu=2  MATCH
# Multiplicities: f3+f44=98, 14+3*f3-4*f44=0 => f3=54, f44=44  MATCH
# Triangle count: 99*14//2//3 = 231  MATCH
# T<=33 (33 orbits of size 3, no fixed pts), values T in {0..33}, T%3==0 and T%7==6: [6,27]  MATCH
# t<=20 (20 free orbits), t%21==2 and t<=20: [2]  MATCH
# e<=49, e%7==0, e%2==1: [7,21,35,49]  MATCH

# 1. SRG equation
v,k,lam,mu = 99,14,1,2
print("SRG: A^2 = (k-mu)I + (lam-mu)A + mu*J =", (k-mu), "I +", (lam-mu), "A +", mu, "J")
print("     i.e. A^2 = 12I - A + 2J  OK:", (k-mu)==12 and (lam-mu)==-1 and mu==2)

# 2. Eigenvalues: theta^2 = 12 - theta
import cmath
disc = 1 + 4*12  # theta^2 + theta - 12 = 0
roots = [(-1 + disc**0.5)/2, (-1 - disc**0.5)/2]
print("Eigenvalues from theta^2=12-theta:", roots, "=> 3 and -4  OK:", set([int(r) for r in roots])=={3,-4})

# 3. Multiplicities
f3, f44 = None, None
for f in range(99):
    ff = 98 - f
    if 14 + 3*f - 4*ff == 0:
        f3, f44 = f, ff
print(f"f3={f3}, f_-4={f44}  OK:", f3==54 and f44==44)

# 4. Triangle count
edges = v*k//2
Ntri = edges//3
print(f"edges={edges}, triangles={Ntri}  OK:", edges==693 and Ntri==231)

# 5. Candidate sets
T_cands = [x for x in range(34) if x%3==0 and x%7==6]
print("T in {T<=33, T%3==0, T%7==6}:", T_cands, "  OK:", T_cands==[6,27])

t_cands = [x for x in range(21) if x%21==2]
print("t in {t<=20, t%21==2}:", t_cands, "  OK:", t_cands==[2])

e_cands = [x for x in range(50) if x%7==0 and x%2==1]
print("e in {e<=49, 7|e, odd}:", e_cands, "  OK:", e_cands==[7,21,35,49])

# 6. Projector formula: tr(sigma*E3) = (4*a0 + a1 - 18)/7
# Derivation: E3 = (A-3*I)(A+4*I) / ((3-14)(3+4)) ... actually let's re-derive
# General: tr(sigma*E_theta) = sum_i chi_sigma(i) * [i in theta-eigenspace]
# For srg, the projectors onto eigenspaces theta_j are:
# E_j = prod_{i!=j} (A - theta_i*I) / prod_{i!=j}(theta_j - theta_i)
# E_14 = (A-3I)(A+4I)/((14-3)(14+4)) = (A-3I)(A+4I)/198
# E_3  = (A-14I)(A+4I)/((3-14)(3+4)) = (A-14I)(A+4I)/((-11)(7)) = (A-14I)(A+4I)/(-77)
# E_{-4}= (A-14I)(A-3I)/((-4-14)(-4-3)) = (A-14I)(A-3I)/((-18)(-7)) = (A-14I)(A-3I)/126

# tr(sigma*E_3) = tr(sigma*(A-14I)(A+4I)/(-77))
# For an automorphism sigma, tr(sigma*A) = alpha_1 (vertices in full orbits adjacent to themselves -- NO)
# Actually tr(sigma*A) counts edges {v, sigma(v)}: = (number of fixed edges under sigma)
# Wait: tr(sigma*A)[i,i] = sum_j sigma[i,j]*A[j,i] -- this is the permutation matrix approach
# More carefully: if P_sigma is the permutation matrix, tr(P_sigma * A) = sum_i A[sigma^{-1}(i), i]
# = number of i such that sigma^{-1}(i) ~ i, i.e. number of edges {i, sigma(i)} with sigma(i)!=i...
# Actually for undirected: = number of vertices i with i ~ sigma(i).
# Standard result: tr(P_sigma * A^m) counts walks of length m from i to sigma(i).
# For tr(P_sigma): = alpha_0 (fixed points)
# For tr(P_sigma * A): counts edges {v, sigma(v)}, = alpha_1 for order-p (each orbit contributes 0 or p edges, but...)
# Actually for order p, vertices in full orbits: each orbit of size p contributes p edges {v,sigma(v),...}? No.
# tr(P*A) = #{i : A[i, sigma(i)] = 1} = #{i : i ~ sigma(i)}.
# For sigma of order p with no fixed pts: each orbit {v, sv, s^2v,...,s^{p-1}v}.
# Each vertex v has sigma(v) = sv. v~sv iff the orbit forms at least one edge.
# If orbit is K_p, all p edges present, contributing p to tr(P*A).
# This equals alpha_1 only if alpha_1 counts vertices in orbits that form K_p? Not quite general.
#
# The paper uses a specific formula. Let's verify it from first principles differently.
# tr(P_sigma * E_3) must be a non-negative integer (it's the character of sigma on the eigenspace).
# The formula given: tr(sigma*E3) = (4*a0 + a1 - 18)/7
# where a1 = alpha_1 = #vertices in orbits of size = ord(sigma).
# For order 3, no fixed pts: a0=0, a1=99, formula gives (0+99-18)/7 = 81/7 -- NOT INTEGER!
# Wait, that can't be right. Let me re-read the paper.
# Paper line 134: tr(sigma*E3) = (44*a0 + 11*a1 - 2*tr(sigma*J)) / 77
# and tr(sigma*J) = 99 for ANY automorphism (since J has eigenvalue 99 with eigvec 1, and sigma fixes 1)
# So: = (44*a0 + 11*a1 - 198) / 77 = (4*a0 + a1 - 18)/7

# For order 3, no fixed pts: a0=0, a1 = 3T (triangle-orbits contribute 3 to alpha_1? No!)
# Wait: alpha_1 = #vertices in orbits of size = ord(sigma) = 3. With no fixed pts, ALL 99 vertices
# are in orbits of size 3. So alpha_1 = 99 always for the no-fixed-pt case.
# But the paper says "each triangle-orbit contributes 3 to alpha_1, so alpha_1 = 3T" -- that's WRONG
# if alpha_1 means ALL vertices in size-3 orbits!
#
# Let me re-read: Definition 2.1 says alpha_1 = #vertices in orbits of size = ord(sigma).
# For no-fixed-pt order-3: every vertex is in a size-3 orbit, so alpha_1 = 99.
# Paper line 197-199 says "each triangle-orbit contributes 3 to alpha_1, so alpha_1 = 3T".
# This contradicts the definition! The paper seems to be redefining alpha_1 here.
#
# Check: if alpha_1=99, then tr(sigma*E3) = (0 + 99 - 18)/7 = 81/7 -- non-integer. BAD.
#
# So either: (a) the paper uses a different alpha_1 in the mod-7 computation, or
#            (b) there is a genuine error in the formula or its application.
#
# The formula 77*tr(sigma*E3) = 44*a0 + 11*a1 - 2*tr(sigma*J)
# where tr(sigma*J) need not be 99 in general -- it equals #fixed vertices = alpha_0!
# Because J = ones matrix, (P*J)[i,i] = J[sigma^{-1}(i), i] = 1 always...
# Actually tr(P_sigma * J) = sum_i J[sigma^{-1}(i), i] = sum_i 1 = v = 99 always. YES, 99.
#
# So the formula with a1=99 (all vertices in size-3 orbits) gives 81/7 -- not integer.
# The paper must mean something different by alpha_1 in that computation.
#
# Looking more carefully at the standard formula:
# For a permutation sigma on v vertices, with eigenvalue decomposition of P_sigma,
# tr(P_sigma * E_theta) is computed via the relation:
# P_sigma * A = A * P_sigma (automorphism)
# tr(P_sigma) = alpha_0
#
# Standard: for srg(v,k,lambda,mu), eigenvalues r,s with multiplicities f,g:
# 77 * tr(P*E_r) = (s^2 + s*k ... no, let me use the actual spectral decomposition.
#
# A = k*E_k + r*E_r + s*E_s  (spectral decomposition, E_k = J/v)
# tr(P*A) = k*tr(P*E_k) + r*tr(P*E_r) + s*tr(P*E_s)
# tr(P*I) = tr(P*E_k) + tr(P*E_r) + tr(P*E_s)  [since E_k+E_r+E_s=I]
# tr(P*J) = v * tr(P*E_k)  [since E_k = J/v]
#
# So: tr(P*E_k) = tr(P*J)/v = 99/99 = 1 (for any automorphism, P fixes the all-ones vector)
# tr(P*I) = alpha_0
# tr(P*A) = #edges fixed by sigma (edges {u,sigma(u)})
#
# System: tr(P*E_k) + tr(P*E_r) + tr(P*E_s) = alpha_0
#          k + r*tr(P*E_r) + s*tr(P*E_s) = tr(P*A)
#          1 + tr(P*E_r) + tr(P*E_s) = alpha_0  [since tr(P*E_k)=1]
# Wait: sum of all projectors = I, so tr(P*(E_k+E_r+E_s)) = tr(P) = alpha_0
# and tr(P*E_k) = tr(P*J/v) = tr(P*J)/v.
# tr(P*J) = sum_{i,j} P_{ij}*J_{ji} ...
# P is permutation matrix: P_{ij} = [j = sigma(i)], so tr(P*J) = sum_i J_{sigma(i),i} = sum_i 1 = v.
# So tr(P*E_k) = v/v = 1 always.
# Thus: 1 + tr(P*E_r) + tr(P*E_s) = alpha_0 => tr(P*E_r) + tr(P*E_s) = alpha_0 - 1.
# 14 + r*tr(P*E_r) + s*tr(P*E_s) = tr(P*A).
# For r=3, s=-4:
# tr(P*E_3) + tr(P*E_{-4}) = alpha_0 - 1
# 3*tr(P*E_3) - 4*tr(P*E_{-4}) = tr(P*A) - 14
# => 7*tr(P*E_3) = 4*(alpha_0-1) + (tr(P*A)-14) = 4*alpha_0 + tr(P*A) - 18
# => tr(P*E_3) = (4*alpha_0 + tr(P*A) - 18) / 7
#
# So the formula is tr(P*E_3) = (4*alpha_0 + tr(P*A) - 18) / 7
# where tr(P*A) = #vertices i with i adjacent to sigma(i).
# The paper writes this as (4*a0 + a1 - 18)/7 where a1 = alpha_1.
# So the paper defines alpha_1 = tr(P*A) = #{i : i ~ sigma(i)}.
# That is NOT the same as "number of vertices in orbits of size = ord(sigma)"!
#
# For order-3, no fixed pts: tr(P*A) = #{i : i ~ sigma(i)}.
# Vertices in a triangle-orbit: each vertex i has sigma(i) adjacent to i (since the orbit is K_3).
# So each triangle-orbit contributes 3 to tr(P*A). Hence tr(P*A) = 3T. This matches!
# For a non-triangle size-3 orbit: sigma(i) is not adjacent to i, contributing 0.
# So alpha_1 in the paper = tr(P*A) = 3T (for order-3, no fixed pts). CONSISTENT.
#
# For order-3, fixed triangle: a0=3, tr(P*A) = #{i : i~sigma(i)}.
# Fixed vertices: sigma(i)=i, so i~sigma(i) iff i~i -- self-loops don't exist. So fixed vertices contribute 0.
# Wait, actually for fixed vertex i, sigma(i)=i, so i~sigma(i) = i~i = 0 (no self-loops).
# For size-3 orbit (triangle): each vertex i has sigma(i) adjacent, contributing 3 per triangle-orbit.
# So tr(P*A) = 3t.
# Paper line 234: "alpha_1 = 3t, so tr(sigma*E3) = (44*3 + 11*3t - 2*99)/77"
# Wait that's the WRONG formula! Let me re-read line 132-134:
# "77*tr(sigma*E3) = 44*a0 + 11*a1 - 2*tr(sigma*J)" where tr(sigma*J)=99
# But I derived: tr(P*E3) = (4*a0 + tr(P*A) - 18)/7 = (4*a0*7 + 7*tr(P*A) - 126)/49...
# Let me reconcile:
# tr(P*E3) = (4*a0 + tr(P*A) - 18)/7
# 7*tr(P*E3) = 4*a0 + tr(P*A) - 18
# Paper: 77*tr(P*E3) = 44*a0 + 11*a1 - 2*99 = 44*a0 + 11*a1 - 198
# Dividing by 11: 7*tr(P*E3) = 4*a0 + a1 - 18
# So a1 in the paper = tr(P*A). Confirmed.
#
# Now: for order-3, fixed triangle:
# a0=3, a1 (=tr(P*A)) = 3t (triangle-orbits only, as argued).
# tr(P*E3) = (4*3 + 3t - 18)/7 = (12 + 3t - 18)/7 = (3t - 6)/7 = 3(t-2)/7. CHECK.
# Paper line 236: (44*3 + 11*3t - 2*99)/77 = (132 + 33t - 198)/77 = (33t - 66)/77 = 3(t-2)/7. MATCH.

# VERIFY these algebraically:
print("\n--- PROJECTOR FORMULA CHECKS ---")
# No-fixed-pt order-3: a0=0, a1=3T
for T in [6, 27]:
    a0, a1 = 0, 3*T
    tr_E3 = (4*a0 + a1 - 18) / 7
    print(f"T={T}: tr(P*E3) = (0 + {a1} - 18)/7 = {tr_E3} (integer: {tr_E3==int(tr_E3)})")
    # m0 + 2*m1 = 54, tr = m0 - m1 => m0 = (54 + 3*tr_E3)/3...
    # Actually tr = m0*1 + m1*omega + m1*omega^2 = m0 - m1 (since omega+omega^2=-1)
    # m0 - m1 = tr_E3, m0 + 2*m1 = 54 => m1 = (54-tr_E3)/3, m0 = 54 - 2*m1
    m1 = (54 - tr_E3)/3
    m0 = 54 - 2*m1
    print(f"  m0={m0}, m1={m1} (integers: {m0==int(m0) and m1==int(m1) and m0>=0 and m1>=0})")

# Paper says m0 = (2T+114)/7... let me verify:
# 3(T-6)/7 = m0 - m1, m0+2m1=54
# m0 - m1 = 3(T-6)/7
# m0 + 2m1 = 54
# 3m0 = 54 + 3*(T-6)/7... => m0 = 18 + (T-6)/7... that gives m0=(2T+114)/7?
# 18 + (T-6)/7 = (126 + T - 6)/7 = (T+120)/7. NOT (2T+114)/7. Let me recheck paper.
# Paper: "m0 = (2T+114)/7". Let's verify for T=6: (12+114)/7=126/7=18. For T=27: (54+114)/7=168/7=24.
# My formula: (T+120)/7. For T=6: 126/7=18. For T=27: 147/7=21. MISMATCH!
print("\n--- CHECK m0 FORMULA ---")
for T in [6,27]:
    paper_m0 = (2*T + 114) / 7
    my_m0 = (T + 120) / 7
    # Recompute from tr_E3=3(T-6)/7:
    tr_E3 = 3*(T-6)/7
    # m0 - m1 = tr_E3, m0 + 2*m1 = 54 => 3*m0 = 54 + 3*tr_E3... no: add eq1 + 2*eq2:
    # (m0-m1) + 2*(m0+2m1) ... = tr_E3 + 2*54 => 3m0+3m1 ... hmm.
    # eq1: m0 - m1 = tr_E3
    # eq2: m0 + 2*m1 = 54
    # eq2 - eq1: 3*m1 = 54 - tr_E3 => m1 = (54-tr_E3)/3
    # m0 = tr_E3 + m1 = tr_E3 + (54-tr_E3)/3 = (3*tr_E3 + 54 - tr_E3)/3 = (2*tr_E3+54)/3
    m0_correct = (2*tr_E3 + 54) / 3
    print(f"T={T}: tr_E3={tr_E3}, paper m0={paper_m0}, my_derived m0={m0_correct}")
    # For T=6: tr_E3=0, m0=(0+54)/3=18=paper. For T=27: tr_E3=3*21/7=9, m0=(18+54)/3=24.
    # Paper says (2*27+114)/7=(54+114)/7=168/7=24. MATCH!
    # My earlier formula was wrong. Let me recheck:
    # 3(T-6)/7 and (2T+114)/7:
    # m0=(2*tr_E3+54)/3 = (2*3*(T-6)/7 + 54)/3 = (6(T-6)/7 + 54)/3 = 2(T-6)/7 + 18 = (2T-12+126)/7=(2T+114)/7. MATCH!
    print(f"  paper formula (2T+114)/7 = {paper_m0}  MATCH: {abs(paper_m0-m0_correct)<1e-9}")
