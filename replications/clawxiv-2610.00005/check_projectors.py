# USCITA ATTESA:
# Verifica formula proiettori e casi specifici srg(99,14,1,2)
# Verifica mod-7 per caso order-3 no-fixed: T in {6,27} sono gli unici <=33 con T%3==0 e T%7==6
# Verifica mod-7 per caso order-3 fixed triangle: t=2 unico valore <=20 con t%21==2
# Verifica caso involuzione: e in {7,21,35,49}
# Verifica formula tr(P*E3) = (4*a0 + a1 - 18)/7 dove a1 = tr(P*A)
# Tutti MATCH

# --- DERIVAZIONE FORMULA PROIETTORE ---
# A = 14*E_14 + 3*E_3 + (-4)*E_{-4}  (spettrale)
# E_14 + E_3 + E_{-4} = I
# tr(P*I) = alpha_0
# tr(P*J) = v = 99 (permutation matrix, J=ones)
# tr(P*E_14) = tr(P*J/99) = 1
# Sistema:
#   tr(P*E_3) + tr(P*E_{-4}) = alpha_0 - 1
#   3*tr(P*E_3) - 4*tr(P*E_{-4}) = tr(P*A) - 14
# Da cui:
#   7*tr(P*E_3) = 4*(alpha_0-1) + tr(P*A) - 14 = 4*alpha_0 + tr(P*A) - 18
# i.e. tr(P*E_3) = (4*alpha_0 + tr_PA - 18) / 7
# where tr_PA = tr(P*A) = #{v : v ~ sigma(v)}

print("=== FORMULA PROIETTORE: derivazione ===")
print("tr(P*E3) = (4*alpha_0 + tr(P*A) - 18) / 7")
print("dove tr(P*A) = #{v : v ~ sigma(v)}")

# --- CASO ORDER-3, NO FIXED VERTEX ---
print("\n=== CASO 1: order-3, no fixed vertex ===")
print("alpha_0=0, ogni orbita contribuisce 3 a tr(P*A) se e' un triangolo (K3)")
print("tr(P*A) = 3*T (T = #orbite-triangolo)")
print("tr(P*E3) = (0 + 3T - 18)/7 = 3(T-6)/7")
print("Integralita': T ≡ 6 (mod 7)")
print("Mod 3: 231 = 3T + 3m (invariant tri = T, free orbits only), T ≡ 0 (mod 3)")
print("T <= 33 (33 orbite di taglia 3)")
T_cands = [x for x in range(34) if x % 3 == 0 and x % 7 == 6]
print(f"T in {{0..33, T%3==0, T%7==6}}: {T_cands}")
assert T_cands == [6, 27], "MISMATCH T candidates!"
print("MATCH: T in {6, 27}")

# Verifica m0, m1 interi non negativi per T=6,27:
for T in [6, 27]:
    tr_E3 = 3*(T-6)/7
    m0 = (2*tr_E3 + 54)/3  # from m0-m1=tr_E3, m0+2m1=54
    m1 = (54 - tr_E3)/3
    assert m0 >= 0 and m1 >= 0 and m0 == int(m0) and m1 == int(m1), f"m0,m1 non interi per T={T}"
    # m0 = (2T+114)/7 (formula del paper)
    paper_m0 = (2*T + 114)/7
    assert abs(m0 - paper_m0) < 1e-9, f"m0 mismatch per T={T}: got {m0}, paper {paper_m0}"
    print(f"  T={T}: tr_E3={tr_E3}, m0={m0}, m1={m1} -- integer non-neg: OK, paper m0 formula: MATCH")

# --- CASO ORDER-3, FIXED TRIANGLE (alpha_0=3) ---
print("\n=== CASO 2: order-3, fixed triangle (alpha_0=3) ===")
print("alpha_0=3, tr(P*A) = 3t (t = #triangle-orbits, tutti free)")
print("tr(P*E3) = (4*3 + 3t - 18)/7 = (12 + 3t - 18)/7 = 3(t-2)/7")
print("Integralita': t ≡ 2 (mod 7)")
print("Mod 3: N_sigma = 1 + t (fixed triangle + t triangle-orbits)")
print("231 = 1 + t + 3m => 230 = t + 3m => t ≡ 230 ≡ 2 (mod 3)")
print("CRT: t ≡ 2 (mod 21)")
print("t <= 20 (20 free orbits, ogni triangle-orbit è free)")
t_cands = [x for x in range(21) if x % 21 == 2]
print(f"t in {{0..20, t%21==2}}: {t_cands}")
assert t_cands == [2], "MISMATCH t candidates!"
print("MATCH: t = 2")

# Verifica formula numerica per t=2:
t = 2
tr_E3_t = 3*(t-2)/7
print(f"  t=2: tr(P*E3) = {tr_E3_t}  (intero: {tr_E3_t == int(tr_E3_t)})")
# verifica alternativa formula paper line 236:
alt = (44*3 + 11*3*t - 2*99)/77
print(f"  verifica formula paper (44*3+11*3t-2*99)/77 = {alt}  MATCH: {abs(tr_E3_t - alt) < 1e-9}")

# --- CASO INVOLUZIONE (alpha_0=1, alpha_1=2e, da classificazione) ---
print("\n=== CASO 3: involuzione, alpha_0=1, tr(P*A)=2e ===")
print("Nota: tr(P*A) per involuzione: ciascun vertice v con tau(v)=v contribuisce solo se v~v (impossibile)")
print("Per un 2-orbit {x,tau(x)}: contribuisce 2 se x~tau(x), 0 altrimenti.")
print("Il paper definisce e = #2-orbits, e usa tr(P*A) ≡ 2e come 'alpha_1'.")
print("ATTENZIONE: questo è corretto SOLO se ogni 2-orbit è un arco (edge-orbit).")
print("In realta' e = #2-orbits totali (non solo edge-orbits). tr(P*A) = 2*(edge 2-orbits), non 2e.")
print("Il paper usa alpha_1 = 2e dove e = #2-orbits (vertici non fissi / 2 = 49 max).")
print("Ma dalla classificazione citata: 98 = 2e, e <=49.")
print("tr(P*E3) = (4*1 + 2e - 18)/7 = (2e - 14)/7 = 2(e-7)/7")
print("Integralita': e ≡ 0 (mod 7)")
print("Parita': paper argomenta e dispari (da conteggio archi), quindi e in {7,21,35,49}")
e_cands = [x for x in range(50) if x % 7 == 0 and x % 2 == 1]
print(f"e in {{1..49, 7|e, e dispari}}: {e_cands}")
assert e_cands == [7, 21, 35, 49]
print("MATCH: e in {7,21,35,49}")

# Verifica argomento parita':
# "The 693 edges split into the e edges inside 2-orbits and an even number between orbits"
# => e = #{edges {v, tau(v)}} che sono "inside" 2-orbits; e contribuisce con e archi fissi.
# Ma perche' e deve essere dispari?
# Paper: "so e is odd" - dal numero di triangoli fissati: 231 = n + 2m' => n dispari.
# n <= 7 (z ha grado 14, al piu' 7 edge-2-orbits adiacenti a z)
# n <= e (ogni triangolo fissato usa un edge-2-orbit adiacente a z)
# Ma la parita' di e non viene dall'argomento triangoli, bensì:
# Paper line 329: "The 693 edges split into the e edges inside 2-orbits and an even number
#                  of edges between orbits (no between-orbit edge is fixed by tau), so e is odd."
# Questo afferma: 693 = e + 2*(#between-orbit edges). 693 dispari, 2*(...) pari => e dispari. CORRETTO.
print("\nParita' di e: 693 = e + (pari) => e dispari. MATCH (693 dispari)")
assert 693 % 2 == 1, "693 must be odd"
print("MATCH: e dispari")

# Ma ATTENZIONE: tr(P*A) nella formula proiettore = #{v : v ~ tau(v)}.
# z e' il vertice fisso; tau(z)=z, z~z impossibile, contribuisce 0.
# Per un 2-orbit {x, tau(x)}: entrambi contribuiscono a tr(P*A) sse x~tau(x).
# Quindi tr(P*A) = 2*(numero di edge 2-orbits) = 2*n_e (dove n_e = #2-orbits che sono archi).
# Il paper usa alpha_1 = 2e dove e = #2-orbits TOTALI.
# Questi coincidono solo se tutti i 2-orbits sono archi, il che NON e' vero in generale.
# Quindi la formula del paper potrebbe avere un errore: usa 2e in luogo di 2*n_e.
print("\n=== POTENZIALE DIFETTO: alpha_1 nel caso involuzione ===")
print("Il paper usa tr(P*A) = 2e dove e = #2-orbits totali.")
print("Ma tr(P*A) = #{v : v ~ tau(v)} = 2*(#edge 2-orbits) ≠ 2e in generale.")
print("Questo e' un difetto: la formula del proiettore usa alpha_1 = tr(P*A),")
print("non alpha_1 = #vertices in full orbits.")
print("Il paper ottiene e ≡ 0 (mod 7), ma la condizione corretta sarebbe")
print("n_e ≡ 0 (mod 7) dove n_e = #edge-2-orbits, con n_e ≠ e in generale.")
print("SOSPETTO DIFETTO (non confermabile senza rete per ref originale MakhnevMinakova2004).")
