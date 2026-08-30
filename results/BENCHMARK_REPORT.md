# SAH-BVH Ray Tracer: Benchmark Report

## Overview

This report documents the performance gains achieved by adding a Bounding Volume Hierarchy (BVH) acceleration structure with Surface Area Heuristics (SAH) to a CPU ray tracer. All benchmarks were run on Apple Silicon (ARM64) with `-O2` optimization.

---

## 1. Ray-Sphere Intersection Benchmark

**Setup:** 10,000 random rays tested against N spheres. Pure intersection time measured (no rendering overhead).

| Spheres | No BVH (s) | With BVH (s) | Speedup |
|---------|------------|--------------|---------|
| 1,000 | 0.0616 | 0.0043 | 14.3x |
| 5,000 | 0.3116 | 0.0105 | 29.6x |
| 10,000 | 0.8107 | 0.0155 | 52.1x |
| 50,000 | 3.5830 | 0.0338 | 106.1x |
| 100,000 | 6.5696 | 0.0903 | 72.8x |
| 500,000 | 34.7156 | 0.2032 | 170.8x |
| 1,000,000 | 81.0841 | 0.2982 | 272.0x |

**Complexity Analysis (log-log regression):**
- No BVH: O(n^1.02), R² = 0.9993: confirmed linear
- With BVH: O(n^0.63), R² = 0.9944: sublinear (logarithmic behavior)

**Key result:** At 1M spheres, BVH reduces intersection time from 81s to 0.3s: a **272x speedup**.

---

## 2. Full Rendering Benchmark (Offline)

**Setup:** Headless rendering of 200×150 image (30,000 rays/frame, 3 samples/pixel, max depth 5). No SDL, no display: pure CPU ray tracing.

| Spheres | No BVH (s) | With BVH (s) | Speedup |
|---------|------------|--------------|---------|
| 50 | 0.0331 | 0.0121 | 2.7x |
| 100 | 0.0746 | 0.0228 | 3.3x |
| 500 | 0.4013 | 0.0451 | 8.9x |
| 1,000 | 0.7823 | 0.0600 | 13.0x |
| 5,000 | 3.9080 | 0.1251 | 31.2x |

**Key result:** Full rendering (with reflections, shading) achieves **31x speedup** at 5K spheres.

---

## 3. Realtime Rendering Benchmark

**Setup:** SDL2 window at 200×150, 1000 spheres, max depth 5. BVH toggled with 'b' key.

| Mode | Trace/frame | Draw/frame | FPS |
|------|-------------|------------|-----|
| With BVH | ~0.053s | ~0.002s | ~15 |
| Without BVH | ~0.51s | ~0.002s | ~2 |

**Result:** **8x realtime FPS improvement** (2 → 15 FPS) at 1000 spheres.

**Why realtime speedup (8x) is lower than intersection benchmark (13x):**
- Realtime includes recursive reflections (depth 5), color blending, camera ray generation
- These costs are shared between BVH and non-BVH paths
- Draw calls are negligible (~0.002s): confirmed all-CPU, no GPU bottleneck

---

## 4. Summary for Resume

| Metric | Value |
|--------|-------|
| Algorithm | SAH-based BVH, top-down construction |
| Construction complexity | O(n log n) |
| Intersection complexity | O(n) → O(log n) per ray |
| Max intersection speedup | **272x** at 1M objects |
| Max rendering speedup | **31x** at 5K objects (offline) |
| Realtime FPS improvement | **8x** at 1K objects (2 → 15 FPS) |

**Resume bullet:**
> Implemented SAH-based BVH acceleration structure for CPU ray tracer, achieving 272x speedup in ray-sphere intersection tests (O(n) → O(log n)) and 8x improvement in realtime rendering FPS at 1000 objects.

---

## 5. How to Reproduce

```bash
# Build with optimizations
make clean && make

# Run intersection + rendering benchmarks
./raytracer 1

# Generate plots from benchmark data
python3 results/main.py

# Run realtime benchmark (low res, high sphere count)
./raytracer 2 200 150 1000

# Toggle BVH with 'b' key and observe FPS difference
```

---

## Files

| File | Description |
|------|-------------|
| `results/benchmark_data.txt` | Raw intersection benchmark data |
| `results/benchmark_render_data.txt` | Raw rendering benchmark data |
| `results/benchmark_plot.png` | 3-panel performance plot |
| `results/realtime_benchmark_log.txt` | Full realtime benchmark log |
| `results/main.py` | Python script to generate plots |
