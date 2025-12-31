CC = clang

CFLAGS = -O3 -mavx512f -Wall -Wextra

TARGET = matmul_avx
SRC = matmul_avx512.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET)