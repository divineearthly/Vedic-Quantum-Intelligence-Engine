
CXX = g++
CC = gcc

# Get pybind11 include flags dynamically
PYBIND11_CFLAGS = $(shell python3 -m pybind11 --includes)

CXXFLAGS = -O3 -Wall -std=c++17 -Iinclude $(PYBIND11_CFLAGS) -fPIC
LDFLAGS = -shared # Use -shared for shared library or adjust for executable

# Get all .cpp files in the current directory
CPP_SRCS = $(wildcard *.cpp)
# Get all .c files in the current directory
C_SRCS = $(wildcard *.c)

# Convert source files to object files
CPP_OBJS = $(CPP_SRCS:.cpp=.o)
C_OBJS = $(C_SRCS:.c=.o)

ALL_OBJS = $(CPP_OBJS) $(C_OBJS)

# Dynamically determine the shared library extension (e.g., .so for Linux)
SHARED_LIB_EXT = $(shell python3 -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")

TARGET_BASE = vedic_engine
TARGET = $(TARGET_BASE)$(SHARED_LIB_EXT)

.PHONY: all clean

all: $(TARGET)

# Rule to link the final executable or shared library
$(TARGET): $(ALL_OBJS)
	$(CXX) $(CXXFLAGS) $(ALL_OBJS) $(LDFLAGS) -o $@

# Rule to compile C++ files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Rule to compile C files
%.o: %.c
	$(CC) $(CXXFLAGS) -c $< -o $@

clean:
	$(RM) $(TARGET) $(ALL_OBJS)
	$(RM) *.o
	$(RM) $(TARGET_BASE)
