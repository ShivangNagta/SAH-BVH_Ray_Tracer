# SAH-BVH Ray Tracer

A CPU ray tracer with Bounding Volume Hierarchy (BVH) acceleration using Surface Area Heuristics (SAH). Achieves **272x speedup** in ray-sphere intersection tests and **8x improvement** in realtime rendering FPS.

## Features

- SAH-based BVH construction (O(n log n))
- Realtime CPU ray tracing with camera controls
- Recursive reflections with microfacet model
- BVH debug visualization
- Comprehensive benchmarking suite

## Dependencies

- **SDL2**: Cross-platform multimedia library for rendering and event handling
- **Python 3 + matplotlib** (optional): For generating benchmark plots

## Setup

### macOS

```bash
brew install sdl2
git clone https://github.com/ShivangNagta/CS201_SAH-BVH_Ray_Tracer.git
cd CS201_SAH-BVH_Ray_Tracer
make
```

### Windows

SDL2 headers and DLLs are included. Install MinGW, then:

```bash
make
```

## Usage

```bash
# Interactive menu
./raytracer

# Run benchmarks directly
./raytracer 1

# Realtime rendering with custom resolution and sphere count
./raytracer 2 [width] [height] [num_spheres]

# Examples
./raytracer 2 200 150 1000    # Low res, 1000 spheres — see BVH speedup
./raytracer 2 1000 800 10     # Full res, 10 spheres — default scene
```

### Controls (Realtime Mode)

| Key | Action |
|-----|--------|
| W/A/S/D | Move camera |
| Space/Shift | Move up/down |
| B | Toggle BVH on/off |
| O | Toggle BVH visualization |
| Mouse (left-click drag) | Rotate camera |
| ESC | Quit |

## Benchmark Results

### Intersection Speedup

| Spheres | No BVH | With BVH | Speedup |
|---------|--------|----------|---------|
| 1,000 | 0.062s | 0.004s | 14x |
| 10,000 | 0.811s | 0.016s | 52x |
| 100,000 | 6.570s | 0.090s | 73x |
| 1,000,000 | 81.084s | 0.298s | **272x** |

### Realtime FPS (1000 spheres, 200x150)

| Mode | FPS |
|------|-----|
| With BVH | ~15 |
| Without BVH | ~2 |
| **Speedup** | **8x** |

### Generate Plots

```bash
./raytracer 1                    # Run benchmarks
python3 results/main.py          # Generate plots
# Output: results/benchmark_plot.png
```

See `results/BENCHMARK_REPORT.md` for full analysis.

## Screenshots

<p align="center">
  <img width="796" alt="Ray Tracer Output" src="https://github.com/user-attachments/assets/65a276f8-f0ca-49e8-b37c-e9b7317ee6b4">
</p>

<p align="center">
  <img width="987" alt="Complexity Analysis" src="https://github.com/user-attachments/assets/76585d93-f58d-4939-9c68-02093f8adb07">
</p>

<p align="center">
  <img width="987" alt="BVH Intersection Test" src="https://github.com/user-attachments/assets/9351f1c2-5951-4e6f-b4a1-96ed9a8cdf4a">
</p>

<p align="center">
  <img width="796" alt="Additional Result 1" src="https://github.com/user-attachments/assets/9e7bf9f7-b1ce-4c90-a051-772a6d6651e2">
</p>

<p align="center">
  <img width="793" alt="Additional Result 2" src="https://github.com/user-attachments/assets/cf9e8c17-80bf-4319-9279-8720fa968389">
</p>

## Project Structure

```
src/
  main.c           — Entry point, main loop, FPS calculation
  bvh.c            — SAH-based BVH construction
  hit.c            — Ray-AABB, ray-sphere, ray-BVH intersection
  renderer.c       — Recursive ray tracing
  benchmark.c      — Benchmarking engine
  camera.c         — Camera controls
  ray.c            — Ray generation
  sphere.c         — Sphere utilities
  vec3.c           — 3D vector math
results/
  main.py                        — Python plot generation
  BENCHMARK_REPORT.md            — Full benchmark analysis
  benchmark_plot.png             — Performance visualization
  benchmark_data.txt             — Intersection benchmark data
  benchmark_render_data.txt      — Rendering benchmark data
  realtime_benchmark_log.txt     — Realtime benchmark log
```
