import json
import matplotlib.pyplot as plt
import numpy as np
import math

with open('benchmark_results.json', 'r') as f:
    results = json.load(f)

clients = [r['num_clients'] for r in results]
errors = [r['error'] for r in results]
samples = [r['total_samples'] for r in results]
throughputs = [r['throughput'] for r in results]
times = [r['time'] for r in results]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('MPI π Estimation - Performance Analysis', fontsize=16, fontweight='bold')

ax = axes[0, 0]
ax.plot(clients, errors, 'o-', linewidth=2, markersize=8, color='#e74c3c')
ax.set_xlabel('Number of Clients', fontsize=11)
ax.set_ylabel('Error |π̂ - π|', fontsize=11)
ax.set_title('Error vs Number of Clients (Lower is Better)')
ax.grid(True, alpha=0.3)
ax.set_yscale('log')
theoretical_error = [errors[0] / math.sqrt(c / clients[0]) for c in clients]
ax.plot(clients, theoretical_error, '--', linewidth=2, alpha=0.7, color='#3498db', label='1/√N theory')
ax.legend()

ax = axes[0, 1]
ax.bar(clients, samples, color='#2ecc71', alpha=0.7, edgecolor='black', linewidth=1.5)
ax.set_xlabel('Number of Clients', fontsize=11)
ax.set_ylabel('Total Samples', fontsize=11)
ax.set_title('Total Samples Computed')
ax.grid(True, alpha=0.3, axis='y')
for i, (c, s) in enumerate(zip(clients, samples)):
    ax.text(c, s, f'{s//1e6:.0f}M', ha='center', va='bottom', fontweight='bold')

ax = axes[1, 0]
ax.plot(clients, throughputs, 's-', linewidth=2, markersize=8, color='#9b59b6')
ax.set_xlabel('Number of Clients', fontsize=11)
ax.set_ylabel('Throughput (samples/sec)', fontsize=11)
ax.set_title('Throughput Scaling')
ax.grid(True, alpha=0.3)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M'))

ax = axes[1, 1]
ax.plot(times, errors, 'D-', linewidth=2, markersize=8, color='#f39c12')
ax.set_xlabel('Execution Time (seconds)', fontsize=11)
ax.set_ylabel('Error |π̂ - π|', fontsize=11)
ax.set_title('Error Convergence Over Time')
ax.grid(True, alpha=0.3)
ax.set_yscale('log')
for i, (t, e, c) in enumerate(zip(times, errors, clients)):
    ax.annotate(f'{c}c', (t, e), textcoords="offset points", xytext=(5,5), fontsize=9)

plt.tight_layout()
plt.savefig('benchmark_results.png', dpi=150, bbox_inches='tight')
print("✓ Graph saved to benchmark_results.png")
plt.show()
