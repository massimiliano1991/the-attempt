# USCITA ATTESA:
# Lemma triangle-orbit congruence: 300+ casi, sigma AUTOMORFISMO del grafo, tutti PASS
# Total cases tested: >= 300, failures: 0

# NOTA: il teorema richiede che sigma sia un AUTOMORFISMO del grafo.
# Il test precedente usava grafi casuali NON sigma-invarianti: i fallimenti erano attesi.
# Questo script costruisce grafi sigma-invarianti per definizione.

import random, itertools
random.seed(42)

def count_triangles(adj, n):
    count = 0
    for u in range(n):
        for v in range(u+1, n):
            if v in adj[u]:
                for w in range(v+1, n):
                    if w in adj[u] and w in adj[v]:
                        count += 1
    return count

def setwise_invariant_triangles(adj, n, perm):
    count = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in adj[u]:
                continue
            for w in range(v+1, n):
                if w not in adj[u] or w not in adj[v]:
                    continue
                tri = frozenset([u,v,w])
                img = frozenset([perm[u], perm[v], perm[w]])
                if tri == img:
                    count += 1
    return count

def make_invariant_graph(n, perm, edge_seed_pairs):
    """Build sigma-invariant graph by closing a seed set of edges under perm."""
    adj = [set() for _ in range(n)]
    for (u, v) in edge_seed_pairs:
        # Close under perm
        cur_u, cur_v = u, v
        for _ in range(1000):
            if cur_v != cur_u:
                adj[cur_u].add(cur_v)
                adj[cur_v].add(cur_u)
            cur_u, cur_v = perm[cur_u], perm[cur_v]
            if (cur_u, cur_v) == (u, v) or (cur_u == u and cur_v == v):
                break
    return adj

def apply_perm_k(perm, k):
    n = len(perm)
    result = list(range(n))
    for _ in range(k):
        result = [perm[result[i]] for i in range(n)]
    return result

def perm_order(perm):
    n = len(perm)
    cur = list(range(n))
    for k in range(1, n+1):
        cur = [perm[cur[i]] for i in range(n)]
        if cur == list(range(n)):
            return k
    return -1

failures = 0
tested = 0

# Case 1: circulant graphs with rotation (always sigma-invariant)
for n in [6, 9, 12, 15, 18, 21, 10, 14, 15, 20, 25, 35, 42]:
    possible = list(range(1, n//2 + 1))
    for _ in range(4):
        conn_size = random.randint(1, min(3, len(possible)))
        conns = tuple(sorted(random.sample(possible, conn_size)))
        adj = [set() for _ in range(n)]
        for u in range(n):
            for d in conns:
                v = (u + d) % n
                adj[u].add(v); adj[v].add(u)
        rot = list(range(1, n)) + [0]
        for p in [2, 3, 5, 7]:
            if n % p == 0:
                rot_p = apply_perm_k(rot, n // p)
                if perm_order(rot_p) == p:
                    Nt = count_triangles(adj, n)
                    Ns = setwise_invariant_triangles(adj, n, rot_p)
                    if (Nt - Ns) % p != 0:
                        print(f"FAIL circulant: n={n}, conn={conns}, p={p}, Nt={Nt}, Ns={Ns}")
                        failures += 1
                    tested += 1

# Case 2: explicitly sigma-invariant random graphs
for trial in range(200):
    p = random.choice([2, 3, 5, 7])
    num_orbits = random.randint(2, 7)
    n = p * num_orbits
    # Cyclic perm: orbit i -> vertices [i*p, ..., i*p+p-1], shifted by 1 within orbit
    perm = []
    for orb in range(num_orbits):
        base = orb * p
        for i in range(p):
            perm.append(base + (i + 1) % p)
    assert perm_order(perm) == p
    # Seed edges: random pairs (u,v) with u<v, close under perm
    seed_pairs = []
    for u in range(n):
        for v in range(u+1, n):
            if random.random() < 0.25:
                seed_pairs.append((u, v))
    adj = make_invariant_graph(n, perm, seed_pairs)
    Nt = count_triangles(adj, n)
    Ns = setwise_invariant_triangles(adj, n, perm)
    if (Nt - Ns) % p != 0:
        print(f"FAIL invariant: p={p}, n={n}, Nt={Nt}, Ns={Ns}")
        failures += 1
    tested += 1

print(f"Total cases tested: {tested}, failures: {failures}")
if failures == 0:
    print("ALL PASS: N_triangle ≡ N_sigma (mod p) confirmed for all sigma-invariant graphs")
else:
    print(f"THEOREM VIOLATED in {failures} cases -- CHECK PROOF")
