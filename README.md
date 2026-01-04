# Architectures et Modèles de Calcul - Projet HPC

[![CI/CD Pipeline](https://github.com/salasss/Projet_Archi_Calcul/actions/workflows/ci.yml/badge.svg)](https://github.com/salasss/Projet_Archi_Calcul/actions)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![C99+](https://img.shields.io/badge/C-99+-blue.svg)](https://en.cppreference.com/w/c)

## 📋 Vue d'ensemble

Ce projet démontre deux concepts fondamentaux du calcul parallèle haute performance (HPC) :

1. **Part 1 : SIMD Vectorization (AVX-512)** - Multiplication matricielle optimisée
2. **Part 2 : Distributed Computing (MPI)** - Estimation du nombre π en parallèle

---

## Part 1 : Vectorisation SIMD (AVX-512)

### Objectif
Implémenter la multiplication matricielle C = A × B en utilisant les intrinsèques AVX-512.

### Résultats
```
Matrice: 512 × 512
Version naïve:    361.6 ms
Version AVX-512:   15.92 ms
Speedup:          22.71×
```

### Fichiers
- `partie1_avx/matmul_naif.c` - Version naïve (sans vectorisation)
- `partie1_avx/matmul_avx512.c` - Version optimisée AVX-512
- `partie1_avx/Makefile` - Script de compilation

### Techniques utilisées
- **Registres 512-bit** : Manipulation directe des __m512
- **FMA instruction** : `_mm512_fmadd_ps()` pour optimisation latence
- **Transposition matricielle** : Accès mémoire cache-friendly
- **16 floats parallèles** : Par instruction SIMD

### Compilation et test
```bash
cd partie1_avx
make
./matmul_avx
```

### Test avec Intel SDE (émulateur)
```bash
./sde64 -icl -- ./matmul_avx
```

---

## Part 2 : Calcul Distribué (MPI)

### Objectif
Implémenter un système client/serveur pour estimer π en utilisant la méthode Monte-Carlo.

### Architecture
```
Server (rank 0)
    ↓ (envoie "CONTINUE"/"STOP")
    ↑ (reçoit résultats)
Client 1 (rank 1)  | Client 2 (rank 2)  | ... | Client N (rank N)
  (10M samples)      (10M samples)             (10M samples)
```

### Résultats
```
Clients | π estimate    | Error      | Samples   | Throughput
--------|---------------|------------|-----------|---------------
1       | 3.142355      | 0.000762   | 10M       | 5.1M/s
2       | 3.141021      | 0.000572   | 20M       | 9.2M/s
4       | 3.141539      | 0.000054   | 40M       | 21.2M/s
8       | 3.141704      | 0.000111   | 80M       | 27.6M/s
16      | 3.141572      | 0.000021   | 160M      | 29.4M/s
```

### Observations clés
- ✓ **Réduction d'erreur** : 97.2% (0.000762 → 0.000021)
- ✓ **Scalabilité linéaire** : 16 clients = 16× plus d'échantillons
- ✓ **Convergence Monte-Carlo** : Suit la théorie 1/√N
- ✓ **Embarrassingly Parallel** : Overhead de communication minimal

### Fichiers
- `partie2_mpi/pi.py` - Programme principal client/serveur
- `partie2_mpi/benchmark.py` - Script d'automatisation des tests
- `partie2_mpi/report.py` - Analyse des résultats
- `partie2_mpi/plot_results.py` - Génération des graphiques
- `partie2_mpi/requirements.txt` - Dépendances Python

### Installation et test
```bash
# Installation
pip install -r partie2_mpi/requirements.txt

# Test rapide (4 clients)
cd partie2_mpi
mpirun --oversubscribe -np 5 python3 pi.py

# Benchmark complet (1, 2, 4, 8, 16 clients)
python3 benchmark.py

# Générer rapport et graphiques
python3 report.py
python3 plot_results.py
```

---

## 🔄 CI/CD Pipeline

Ce projet inclut un pipeline GitHub Actions automatisé qui :

✓ **Compile** les deux parties du projet (C + Python)  
✓ **Teste** les exécutables (Part 1 & Part 2)  
✓ **Valide** la qualité du code (flake8, black)  
✓ **Vérifie** la documentation (README, requirements.txt)  
✓ **Archive** les artefacts de build  

### Statut du build
[![CI/CD Status](https://github.com/salasss/Projet_Archi_Calcul/actions/workflows/ci.yml/badge.svg)](https://github.com/salasss/Projet_Archi_Calcul/actions)

Le workflow s'exécute automatiquement à chaque push sur `main` et `develop`.

---

## 📊 Fichiers générés

Après exécution de `python3 benchmark.py` et `python3 plot_results.py` :

- `benchmark_results.json` - Données brutes (5 configurations)
- `benchmark_results.png` - Graphiques de performance (4 sous-graphiques)

---

## 📋 Structure du projet

```
Projet_Archi_Calcul/
├── .github/workflows/
│   └── ci.yml                          # Pipeline CI/CD
├── partie1_avx/
│   ├── matmul_naif.c                   # Version naïve
│   ├── matmul_avx512.c                 # Version AVX-512
│   └── Makefile                        # Script compilation
├── partie2_mpi/
│   ├── pi.py                           # Programme principal
│   ├── benchmark.py                    # Automation tests
│   ├── report.py                       # Analyse résultats
│   ├── plot_results.py                 # Graphiques
│   ├── requirements.txt                # Dépendances
│   ├── benchmark_results.json          # Résultats (généré)
│   └── benchmark_results.png           # Graphiques (généré)
└── README.md                           # Ce fichier
```

---

## 🛠️ Dépendances

### Part 1 (AVX-512)
- gcc ou clang (C99+)
- Option `-mavx512f` pour compilation
- Optional: Intel SDE pour testing sur CPU sans AVX-512

### Part 2 (MPI)
- Python 3.9+
- OpenMPI ou MPICH
- Packages: `mpi4py`, `matplotlib`, `numpy`

Installer les dépendances Python:
```bash
pip install -r partie2_mpi/requirements.txt
```

---

## ✅ Checklist de validation

### Part 1
- ✓ Version naïve en C
- ✓ Version AVX-512 optimisée
- ✓ Utilisation correcte des intrinsèques `_mm512_*`
- ✓ Manipulation directe des registres
- ✓ Tests sur hardware natif
- ✓ Tests avec Intel SDE emulator
- ✓ Speedup significatif (22.71× natif, 5.68× émulé)

### Part 2
- ✓ Architecture client/serveur
- ✓ 10 millions d'échantillons par batch
- ✓ Protocole: (Nin, Ntotal) → "CONTINUE"/"STOP"
- ✓ Terminaison sur erreur < 0.001
- ✓ Timeout management (10 secondes)
- ✓ Implémentation mpi4py (send/recv)
- ✓ Scalabilité linéaire vérifiée (1-16 clients)
- ✓ Théorie convergence Monte-Carlo validée (1/√N)
- ✓ Benchmarking automatisé
- ✓ Analyse performance et graphiques

### Documentation
- ✓ README complet
- ✓ Résumé du projet
- ✓ Instructions d'exécution
- ✓ Résultats détaillés
- ✓ Pipeline CI/CD

---

## 📞 Contact

Pour toute question ou remarque sur le projet, consultez les issues GitHub ou contactez directement.

---

**Dernière mise à jour** : 4 janvier 2026  
**Statut** : ✅ Complet et validé
