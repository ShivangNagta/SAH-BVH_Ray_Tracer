#include <time.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <stdbool.h>
#include "Custom/benchmark.h"
#include "Custom/hit.h"

#ifdef _WIN32
#define PRIu64 "I64u"
#include <windows.h>
#else
#include <inttypes.h>
#endif

//----------------------------------------------------------------------------------------------------

// Benchmark Testing
// Testing is done for the intersection of rays with the randomly generated spheres.
// It involves comparison between BVH and no BVH implementation.
// The bvh implementation might show constant time run, as the test cases are not enough.
// Result is plotted with gnuplot(c plotting library) and saved as png, which is further rendered
// with sdl2 (windowing library uses in this project). Plot data is saved in plot_benchmark.gnu

//----------------------------------------------------------------------------------------------------

void free_bvh(BVHNode *node)
{
    if (!node)
        return;
    free_bvh(node->left);
    free_bvh(node->right);
    free(node);
}

void save_benchmark_data(const char *filename, int sphere_count, double time_no_bvh, double time_with_bvh)
{
    FILE *file = fopen(filename, "a");
    if (file == NULL)
    {
        printf("Error opening file!\n");
        return;
    }
    fprintf(file, "%d %f %f\n", sphere_count, time_no_bvh, time_with_bvh);
    fclose(file);
}

double benchmark_no_bvh(Sphere *spheres, int num_spheres, int num_rays)
{
    clock_t start = clock();
    long long intersection_tests = 0;
    int intersections = 0;

    for (int i = 0; i < num_rays; i++)
    {
        Vec3 dir = {
            (float)rand() / RAND_MAX * 2 - 1,
            (float)rand() / RAND_MAX * 2 - 1,
            (float)rand() / RAND_MAX * 2 - 1};
        dir = vec3_normalize(dir);

        Ray ray = {
            {0, 0, 0},
            dir};

        // float closest_dist = INFINITY;
        bool hit_found = false;

        for (int j = 0; j < num_spheres; j++)
        {
            intersection_tests++;
            HitRecord hit = ray_sphere_intersect(ray, &spheres[j]);
            if (hit.hit_something)
            {
                // closest_dist = hit.t;
                hit_found = true;
            }
        }

        if (hit_found)
        {
            intersections++;
        }
    }

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("No BVH:\n");
    printf("Time: %f seconds\n", time_spent);
#ifdef _WIN32
    printf("Intersection tests: %" PRIu64 "\n", (uint64_t)intersection_tests);
#else
    printf("Intersection tests: %lld\n", intersection_tests);
#endif
    printf("Intersections found: %d\n\n", intersections);

    return time_spent;
}

double benchmark_with_bvh(BVHNode *root, int num_spheres, int num_rays)
{
    clock_t start = clock();
    int intersections = 0;

    for (int i = 0; i < num_rays; i++)
    {
        Vec3 dir = {
            (float)rand() / RAND_MAX * 2 - 1,
            (float)rand() / RAND_MAX * 2 - 1,
            (float)rand() / RAND_MAX * 2 - 1};
        dir = vec3_normalize(dir);

        Ray ray = {
            {0, 0, 0},
            dir};

        HitRecord hit = ray_bvh_intersect(ray, root);
        if (hit.hit_something)
            intersections++;
    }

    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("With BVH:\n");
    printf("Time: %f seconds\n", time_spent);
    printf("Intersections found: %d\n\n", intersections);

    return time_spent;
}

void print_sphere_info(Sphere *spheres, int num_spheres) {
    printf("\nSphere Distribution Info:\n");
    float min_x = INFINITY, max_x = -INFINITY;
    float min_y = INFINITY, max_y = -INFINITY;
    float min_z = INFINITY, max_z = -INFINITY;
    
    for (int i = 0; i < num_spheres; i++) {
        if (i < 5) { 
            printf("Sphere %d: center={%.2f,%.2f,%.2f}, radius=%.2f\n",
                   i, spheres[i].center.x, spheres[i].center.y, 
                   spheres[i].center.z, spheres[i].radius);
        }
        
        min_x = fmin(min_x, spheres[i].center.x);
        max_x = fmax(max_x, spheres[i].center.x);
        min_y = fmin(min_y, spheres[i].center.y);
        max_y = fmax(max_y, spheres[i].center.y);
        min_z = fmin(min_z, spheres[i].center.z);
        max_z = fmax(max_z, spheres[i].center.z);
    }
    
    printf("\nSphere bounds: X=[%.2f,%.2f], Y=[%.2f,%.2f], Z=[%.2f,%.2f]\n",
           min_x, max_x, min_y, max_y, min_z, max_z);
}


void run_benchmark()
{

    remove("benchmark_data.txt");
    srand(time(NULL));

    int sphere_counts[10];
    int s = 5000;
    for (int i = 0; i < 10; i++)
    {
        sphere_counts[i] = s;
        s += 5000;
    }
    int num_rays = 10000;
    float world_size = 1000.0f;

    for (int i = 0; i < sizeof(sphere_counts) / sizeof(sphere_counts[0]); i++)
    {
        int num_spheres = sphere_counts[i];
        printf("Testing with %d spheres:\n", num_spheres);
        

        Sphere *spheres = malloc(num_spheres * sizeof(Sphere));
        for (int j = 0; j < num_spheres; j++)
        {
            Vec3 center = {
                (float)rand() / RAND_MAX * world_size - world_size / 2,
                (float)rand() / RAND_MAX * world_size - world_size / 2,
                (float)rand() / RAND_MAX * world_size - world_size / 2};
            spheres[j] = create_benchmark_sphere(center);
        }

        BVHNode *root = build_bvh_node(spheres, 0, num_spheres - 1, 20);

        double time_no_bvh = benchmark_no_bvh(spheres, num_spheres, num_rays);
        double time_with_bvh = benchmark_with_bvh(root, num_spheres, num_rays);

        save_benchmark_data("benchmark_data.txt", num_spheres, time_no_bvh, time_with_bvh);
        free_bvh(root);
        free(spheres);

        printf("----------------------------------------\n");
    }

    printf("\nBenchmark data saved to 'benchmark_data.txt'\n");
    printf("To generate a plot, run: python3 results/main.py\n");
}