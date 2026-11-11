from collections import deque

# (nome, chegada, burst)
PROCESSOS = [("P1", 0, 6), ("P2", 0, 4), ("P3", 0, 2), ("P4", 3, 1)]


def fcfs(procs):
    t, gantt = 0, []
    for n, a, b in sorted(procs, key=lambda p: p[1]):
        t = max(t, a)
        gantt.append((n, t, t + b))
        t += b
    return gantt


def sjf(procs):
    """Não preemptivo: CPU livre -> escolhe o pronto com MENOR burst."""
    restantes, t, gantt = list(procs), 0, []
    while restantes:
        prontos = [p for p in restantes if p[1] <= t]
        if not prontos:                      # CPU ociosa até a próxima chegada
            t = min(p[1] for p in restantes)
            continue
        p = min(prontos, key=lambda x: (x[2], x[1]))   # desempate: chegada
        restantes.remove(p)
        gantt.append((p[0], t, t + p[2]))
        t += p[2]
    return gantt


def round_robin(procs, q):
    procs = sorted(procs, key=lambda p: p[1])
    rest = {n: b for n, a, b in procs}
    chegada = {n: a for n, a, b in procs}
    fila, t, gantt, i = deque(), 0, [], 0
    while i < len(procs) or fila:
        while i < len(procs) and procs[i][1] <= t:
            fila.append(procs[i][0]); i += 1
        if not fila:
            t = procs[i][1]; continue
        n = fila.popleft()
        fatia = min(q, rest[n])
        gantt.append((n, t, t + fatia))
        t += fatia
        rest[n] -= fatia
        while i < len(procs) and procs[i][1] <= t:   # chegadas durante a fatia
            fila.append(procs[i][0]); i += 1
        if rest[n] > 0:
            fila.append(n)                           # volta depois dos novos
    return gantt


def metricas(gantt, procs):
    fim = {}
    for n, ini, f in gantt:
        fim[n] = f
    res = {}
    for n, a, b in procs:
        ta = fim[n] - a
        res[n] = (fim[n], ta, ta - b)               # término, turnaround, espera
    return res


def gantt_txt(gantt):
    linha, marcas = "", ""
    for n, ini, f in gantt:
        w = (f - ini) * 3
        linha += "|" + n.center(w - 1) if w > 1 else "|" + n
        marcas += str(ini).ljust(len(("|" + n.center(w - 1)) if w > 1 else "|" + n))
    return linha + "|\n" + marcas + str(gantt[-1][2])


def mostrar(titulo, g):
    m = metricas(g, PROCESSOS)
    print(f"\n=== {titulo} ===")
    print(gantt_txt(g))
    for n, (fim, ta, esp) in m.items():
        print(f"  {n}: término={fim}  turnaround={ta}  espera={esp}")
    print(f"  Espera média = {sum(v[2] for v in m.values())/len(m):.2f}")


if __name__ == "__main__":
    mostrar("FCFS", fcfs(PROCESSOS))
    for q in (1, 2, 4):
        mostrar(f"Round Robin (q={q})", round_robin(PROCESSOS, q))
    mostrar("SJF (não preemptivo)", sjf(PROCESSOS))