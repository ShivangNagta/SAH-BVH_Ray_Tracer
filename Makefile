# Compiler and flags
CC := gcc
CFLAGS := -Wall -Iinclude 

# Source and target
SRC := src/vec3.c src/camera.c src/sphere.c src/ray.c src/bvh.c src/hit.c src/renderer.c src/main.c src/benchmark.c src/bvh_visualiser.c
TARGET := raytracer

# OS-specific settings
ifeq ($(OS),Windows_NT)
    # Windows-specific settings
    SDL_INCLUDE := -Iinclude
    SDL_LIB := -Llib -lmingw32 -lSDL2main -lSDL2
    TARGET := $(TARGET).exe
    RM := del /Q
else
    # Unix-like systems (Linux/macOS)
    UNAME_S := $(shell uname -s)
    
    ifeq ($(UNAME_S),Darwin)
        SDL_INCLUDE := $(shell sdl2-config --cflags)
        SDL_LIB := $(shell sdl2-config --libs)
        CFLAGS += -arch arm64
    else
        SDL_INCLUDE := $(shell sdl2-config --cflags)
        SDL_LIB := $(shell sdl2-config --libs)
    endif
    RM := rm -f
endif

# Compile with debug information and optimizations
CFLAGS += -g -O2

# OpenMP support
# CFLAGS += -fopenmp
# LDFLAGS += -fopenmp

# Compile
all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SDL_INCLUDE) $(SRC) -o $(TARGET) $(SDL_LIB) $(LDFLAGS)

clean:
	$(RM) $(TARGET)
	$(RM) benchmark_data.txt

.PHONY: all clean
