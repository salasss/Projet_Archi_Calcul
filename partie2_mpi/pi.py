import random
import time
import math
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

SAMPLES_PER_BATCH = 10_000_000
TIMEOUT = 10.0
TARGET_ERROR = 0.001

def estimate_pi(n_samples):
    n_inside = 0
    for _ in range(n_samples):
        x = random.random()
        y = random.random()
        if x*x + y*y < 1.0:
            n_inside += 1
    return n_inside, n_samples

def server():
    if size < 2:
        print("Need at least 2 processes (1 server + 1 client)")
        return
    
    start_time = time.time()
    total_inside = 0
    total_samples = 0
    estimates = []
    
    print(f"[Server] Starting with {size-1} clients, timeout={TIMEOUT}s")
    
    active_clients = set(range(1, size))
    
    while active_clients and (time.time() - start_time) < TIMEOUT:
        status = MPI.Status()
        n_in, n_tot = comm.recv(source=MPI.ANY_SOURCE, tag=0, status=status)
        client_rank = status.Get_source()
        
        total_inside += n_in
        total_samples += n_tot
        
        pi_estimate = 4.0 * total_inside / total_samples
        estimates.append(pi_estimate)
        
        error = abs(pi_estimate - math.pi)
        
        print(f"[Server] Client {client_rank}: pi={pi_estimate:.6f}, error={error:.6f}, total_samples={total_samples}")
        
        if error < TARGET_ERROR or (time.time() - start_time) >= TIMEOUT:
            comm.send("STOP", dest=client_rank, tag=1)
            active_clients.discard(client_rank)
        else:
            comm.send("CONTINUE", dest=client_rank, tag=1)
    
    for client in active_clients:
        comm.send("STOP", dest=client, tag=1)
    
    final_pi = 4.0 * total_inside / total_samples
    elapsed = time.time() - start_time
    
    print(f"\n[Server] Final Results:")
    print(f"  pi estimate: {final_pi:.6f}")
    print(f"  error: {abs(final_pi - math.pi):.6f}")
    print(f"  total samples: {total_samples}")
    print(f"  time: {elapsed:.2f}s")
    print(f"  samples/sec: {total_samples/elapsed:.0f}")

def client():
    batch = 0
    while True:
        n_in, n_tot = estimate_pi(SAMPLES_PER_BATCH)
        comm.send((n_in, n_tot), dest=0, tag=0)
        
        command = comm.recv(source=0, tag=1)
        batch += 1
        print(f"[Client {rank}] Batch {batch}: received '{command}'")
        
        if command == "STOP":
            break

if rank == 0:
    server()
else:
    client()
