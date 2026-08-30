import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# === Load intersection benchmark data ===
with open(os.path.join(project_dir, 'benchmark_data.txt'), 'r') as f:
    lines = f.readlines()
n_spheres = np.array([int(line.split()[0]) for line in lines])
time_no_bvh = np.array([float(line.split()[1]) for line in lines])
time_bvh = np.array([float(line.split()[2]) for line in lines])

# === Load rendering benchmark data ===
render_path = os.path.join(project_dir, 'benchmark_render_data.txt')
has_render_data = os.path.exists(render_path)
if has_render_data:
    with open(render_path, 'r') as f:
        rlines = f.readlines()
    rn_spheres = np.array([int(l.split()[0]) for l in rlines])
    r_speedup = np.array([float(l.split()[1]) for l in rlines])

# === Complexity fits ===
slope_no, intercept_no, r_no, _, _ = stats.linregress(n_spheres, time_no_bvh)
slope_bvh, intercept_bvh, r_bvh, _, _ = stats.linregress(np.log(n_spheres), time_bvh)
slope_ll_no, _, r_ll_no, _, _ = stats.linregress(np.log(n_spheres), np.log(time_no_bvh))
slope_ll_bvh, _, r_ll_bvh, _, _ = stats.linregress(np.log(n_spheres), np.log(time_bvh))

speedup_intersection = time_no_bvh / time_bvh

# === Plotting ===
c_no = '#2563eb'
c_bvh = '#dc2626'
c_speedup = '#059669'

if has_render_data:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
else:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    axes = [ax1, ax2]

# === Plot 1: Linear scale (intersection time) ===
ax1 = axes[0]
x_fit = np.linspace(min(n_spheres) * 0.5, max(n_spheres) * 1.1, 200)

ax1.scatter(n_spheres, time_no_bvh, color=c_no, zorder=5, s=50, edgecolors='white', linewidths=0.5, label='No BVH (measured)')
ax1.scatter(n_spheres, time_bvh, color=c_bvh, zorder=5, s=50, edgecolors='white', linewidths=0.5, label='With BVH (measured)')
ax1.plot(x_fit, slope_no * x_fit + intercept_no, '--', color=c_no, alpha=0.7,
         label=f'No BVH: O(n), R\u00b2={r_no:.4f}')
ax1.plot(x_fit, slope_bvh * np.log(x_fit) + intercept_bvh, '--', color=c_bvh, alpha=0.7,
         label=f'With BVH: O(log n), R\u00b2={r_bvh:.4f}')
ax1.set_xlabel('Number of Spheres', fontsize=11)
ax1.set_ylabel('Intersection Time (seconds)', fontsize=11)
ax1.set_title('Ray-Sphere Intersection Time', fontsize=12, fontweight='bold')
ax1.legend(fontsize=8, loc='upper left')
ax1.grid(True, alpha=0.3)

# === Plot 2: Log-log scale ===
ax2 = axes[1]
ax2.scatter(np.log10(n_spheres), np.log10(time_no_bvh), color=c_no, zorder=5, s=50,
            edgecolors='white', linewidths=0.5, label='No BVH (measured)')
ax2.scatter(np.log10(n_spheres), np.log10(time_bvh), color=c_bvh, zorder=5, s=50,
            edgecolors='white', linewidths=0.5, label='With BVH (measured)')
x_log = np.linspace(np.log10(min(n_spheres)) - 0.2, np.log10(max(n_spheres)) + 0.2, 200)
ax2.plot(x_log, slope_ll_no * x_log + (np.log10(time_no_bvh[0]) - slope_ll_no * np.log10(n_spheres[0])),
         '--', color=c_no, alpha=0.7, label=f'No BVH: slope={slope_ll_no:.2f}')
ax2.plot(x_log, slope_ll_bvh * x_log + (np.log10(time_bvh[0]) - slope_ll_bvh * np.log10(n_spheres[0])),
         '--', color=c_bvh, alpha=0.7, label=f'With BVH: slope={slope_ll_bvh:.2f}')
ax2.set_xlabel('log\u2081\u2080(Spheres)', fontsize=11)
ax2.set_ylabel('log\u2081\u2080(Time)', fontsize=11)
ax2.set_title('Complexity Analysis (Log-Log)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=8, loc='upper left')
ax2.grid(True, alpha=0.3, which='both')

# === Plot 3: Speedup chart ===
if has_render_data:
    ax3 = axes[2]
    ax3.plot(n_spheres, speedup_intersection, '-o', color=c_speedup, linewidth=2, markersize=6,
             label='Intersection tests', zorder=5)
    ax3.plot(rn_spheres, r_speedup, '-s', color='#d97706', linewidth=2, markersize=6,
             label='Full rendering (200\u00d7150, 3 spp)', zorder=5)
    ax3.set_xlabel('Number of Spheres', fontsize=11)
    ax3.set_ylabel('Speedup (x)', fontsize=11)
    ax3.set_title('BVH Speedup Factor', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9, loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')

fig.suptitle(f'BVH Acceleration Structure: Performance Analysis',
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
out_path = os.path.join(script_dir, 'benchmark_plot.png')
plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
print(f"Plot saved to: {out_path}")

# === Print summary ===
print(f"""
{'='*60}
  INTERSECTION BENCHMARK SUMMARY
{'='*60}

  Spheres      No BVH (s)    With BVH (s)    Speedup
  {'─'*60}""")
for n, t1, t2 in zip(n_spheres, time_no_bvh, time_bvh):
    print(f"  {n:>10,}    {t1:>10.4f}    {t2:>10.4f}    {t1/t2:>6.1f}x")
print(f"  {'─'*60}")

if has_render_data:
    print(f"""
{'='*60}
  RENDERING BENCHMARK SUMMARY (200x150, 3 samples/pixel)
{'='*60}

  Spheres      Speedup
  {'─'*60}""")
    for n, s in zip(rn_spheres, r_speedup):
        print(f"  {n:>10,}    {s:>6.1f}x")
    print(f"  {'─'*60}")

print(f"""
  Complexity Analysis:
    No BVH:  O(n^{slope_ll_no:.2f})  R\u00b2 = {r_ll_no:.4f}
    With BVH: O(n^{slope_ll_bvh:.2f})  R\u00b2 = {r_ll_bvh:.4f}

  Key findings:
    - Intersection tests scale as O(n) without BVH, O(log n) with BVH
    - At 1M spheres, BVH is {speedup_intersection[-1]:.0f}x faster (pure intersection)
    - Rendering speedup is lower because overhead is shared (ray generation,
      shading, recursion) but still reaches {r_speedup[-1]:.0f}x at {rn_spheres[-1]:,} spheres
{'='*60}
""")
