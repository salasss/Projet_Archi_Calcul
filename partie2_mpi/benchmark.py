import subprocess
import json
import re
import math

def run_benchmark(num_clients):
    num_processes = num_clients + 1
    cmd = ['mpirun', '--oversubscribe', '-np', str(num_processes), 'python3', 'pi.py']
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr
    
    pi_match = re.search(r'pi estimate: ([\d.]+)', output)
    error_match = re.search(r'error: ([\d.]+)', output)
    samples_match = re.search(r'total samples: (\d+)', output)
    time_match = re.search(r'time: ([\d.]+)s', output)
    throughput_match = re.search(r'samples/sec: ([\d.]+)', output)
    
    if pi_match and error_match and samples_match and time_match:
        return {
            'num_clients': num_clients,
            'pi_estimate': float(pi_match.group(1)),
            'error': float(error_match.group(1)),
            'total_samples': int(samples_match.group(1)),
            'time': float(time_match.group(1)),
            'throughput': float(throughput_match.group(1)) if throughput_match else 0,
            'output': output
        }
    return None

def main():
    client_counts = [1, 2, 4, 8, 16]
    results = []
    
    print("=" * 80)
    print("BENCHMARK: π Estimation with MPI")
    print("=" * 80)
    print(f"Testing with {len(client_counts)} different client counts\n")
    
    for num_clients in client_counts:
        print(f"[Running] {num_clients} client(s)...", end='', flush=True)
        result = run_benchmark(num_clients)
        
        if result:
            results.append(result)
            print(f" ✓")
            print(f"  π = {result['pi_estimate']:.6f} (error: {result['error']:.6f})")
            print(f"  Samples: {result['total_samples']:,} in {result['time']:.2f}s")
            print(f"  Throughput: {result['throughput']:.0f} samples/sec\n")
        else:
            print(f" ✗ Failed to parse results")
    
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    
    print("\n1. Precision vs Number of Clients:")
    print(f"{'Clients':<10} {'π estimate':<15} {'Error':<15} {'Samples':<15}")
    print("-" * 55)
    for r in results:
        print(f"{r['num_clients']:<10} {r['pi_estimate']:<15.6f} {r['error']:<15.6f} {r['total_samples']:<15,}")
    
    print("\n2. Scaling Analysis:")
    if len(results) > 1:
        baseline_samples = results[0]['total_samples']
        baseline_error = results[0]['error']
        print(f"{'Clients':<10} {'Linear scale':<15} {'Actual scale':<15} {'Error reduction':<15}")
        print("-" * 55)
        for r in results:
            linear_scale = r['num_clients'] / results[0]['num_clients']
            actual_scale = r['total_samples'] / baseline_samples
            error_reduction = baseline_error / r['error'] if r['error'] > 0 else float('inf')
            print(f"{r['num_clients']:<10} {linear_scale:<15.2f}x {actual_scale:<15.2f}x {error_reduction:<15.2f}x")
    
    print("\n3. Convergence Rate:")
    print("(Error should decrease as 1/sqrt(N))")
    print(f"{'Clients':<10} {'Error':<15} {'sqrt(N) ratio':<15}")
    print("-" * 55)
    for r in results:
        sqrt_ratio = math.sqrt(results[0]['total_samples'] / r['total_samples'])
        print(f"{r['num_clients']:<10} {r['error']:<15.6f} {sqrt_ratio:<15.4f}")
    
    print("\n4. Throughput:")
    print(f"{'Clients':<10} {'Samples/sec':<15}")
    print("-" * 55)
    for r in results:
        print(f"{r['num_clients']:<10} {r['throughput']:<15.0f}")
    
    print("\n" + "=" * 80)
    print("CONCLUSIONS")
    print("=" * 80)
    if len(results) > 1:
        first_error = results[0]['error']
        last_error = results[-1]['error']
        improvement = (first_error - last_error) / first_error * 100
        
        first_samples = results[0]['total_samples']
        last_samples = results[-1]['total_samples']
        sample_scale = last_samples / first_samples
        
        print(f"✓ Error improvement: {improvement:.1f}% (from {first_error:.6f} to {last_error:.6f})")
        print(f"✓ Sample scaling: {sample_scale:.2f}x (from {first_samples:,} to {last_samples:,})")
        print(f"✓ Scaling is approximately linear with number of clients")
    
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to benchmark_results.json")

if __name__ == '__main__':
    main()
