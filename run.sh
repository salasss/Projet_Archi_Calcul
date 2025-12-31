#!/bin/bash
# QUICK START GUIDE - Projet Architecture & Modèles de Calcul

echo "=================================="
echo "PROJET: Architecture & Calcul"
echo "=================================="
echo ""

read -p "Quelle partie voulez-vous tester? (1=AVX-512, 2=MPI π, q=quitter): " choice

case $choice in
  1)
    echo ""
    echo "=== PARTIE 1: AVX-512 Matrix Multiplication ==="
    cd partie1_avx
    echo "Compilation..."
    make clean && make
    echo ""
    echo "Exécution..."
    ./matmul_avx
    cd ..
    ;;
  2)
    echo ""
    echo "=== PARTIE 2: MPI π Estimation ==="
    cd partie2_mpi
    
    echo "Installation des dépendances..."
    pip install -q -r requirements.txt
    
    read -p "Mode simple (s) ou benchmark complet (b)? " mode
    
    if [ "$mode" = "b" ]; then
      echo ""
      echo "Lancement du benchmark (teste 1, 2, 4, 8, 16 clients)..."
      python3 benchmark.py
      echo ""
      echo "Génération du rapport..."
      python3 report.py
      echo ""
      echo "Génération des graphiques..."
      python3 plot_results.py
      echo ""
      echo "Fichiers générés:"
      echo "  - benchmark_results.json"
      echo "  - benchmark_results.png"
    else
      echo ""
      echo "Lancement simple (5 processus: 1 serveur + 4 clients)..."
      mpirun --oversubscribe -np 5 python3 pi.py
    fi
    
    cd ..
    ;;
  q)
    echo "Au revoir!"
    exit 0
    ;;
  *)
    echo "Choix invalide"
    ;;
esac

echo ""
echo "=================================="
echo "Fin du test"
echo "=================================="
