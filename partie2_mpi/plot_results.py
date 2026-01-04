import json
import matplotlib.pyplot as plt
import math

# Read results from JSON file
with open('benchmark_results.json', 'r') as f:
    results = json.load(f)

# Extract data
clients = [r['num_clients'] for r in results]
errors = [r['error'] for r in results]
samples = [r['total_samples'] for r in results]
throughputs = [r['throughput'] for r in results]

# Create 4 graphs
fig, axes = plt.subplots(2, 2, figsize=(12, 9))
fig.suptitle('π Estimation with MPI - Performance Analysis', fontsize=14, fontweight='bold')

# Graph 1: Error vs Number of clients
ax = axes[0, 0]
ax.plot(clients, errors, 'o-', linewidth=2, markersize=8, color='red')
ax.set_xlabel('Number of Clients')
ax.set_ylabel('Error |π̂ - π|')
ax.set_title('Error Decreases with More Clients')
ax.grid(True, alpha=0.3)
ax.set_yscale('log')

# Graph 2: Total samples
ax = axes[0, 1]
ax.bar(clients, samples, color='green', alpha=0.7)
ax.set_xlabel('Number of Clients')
ax.set_ylabel('Total Samples (M)')
ax.set_title('Total Samples Computed')
ax.grid(True, alpha=0.3, axis='y')

# Graph 3: Throughput
ax = axes[1, 0]
ax.plot(clients, throughputs, 's-', linewidth=2, markersize=8, color='blue')
ax.set_xlabel('Number of Clients')
ax.set_ylabel('Throughput (samples/sec)')
ax.set_title('Throughput Scales Linearly')
ax.grid(True, alpha=0.3)

# Graph 4: Verify 1/√N theory
ax = axes[1, 1]
ax.plot(clients, errors, 'D-', linewidth=2, markersize=8, color='purple', label='Actual Error')

# Plot theoretical 1/√N curve
theoretical_error = [errors[0] / math.sqrt(c / clients[0]) for c in clients]
ax.plot(clients, theoretical_error, '--', linewidth=2, color='orange', label='1/√N Theory')

ax.set_xlabel('Number of Clients')
ax.set_ylabel('Error |π̂ - π|')
ax.set_title('Verification of 1/√N Theory')
ax.grid(True, alpha=0.3)
ax.set_yscale('log')
ax.legend()

# Save the figure
plt.tight_layout()
plt.savefig('benchmark_results.png', dpi=150)
print("✓ Graphs saved to benchmark_results.png")
plt.show()
