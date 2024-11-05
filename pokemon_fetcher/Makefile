CC=gcc
CFLAGS=-Wall -Wextra \
       -I./include \
       $(shell pkg-config --cflags cairo) \
       -I/opt/homebrew/include/freetype2 \
       -I/opt/homebrew/Cellar/curl/7.79.1/include

LDFLAGS=$(shell pkg-config --libs cairo) \
        -L/opt/homebrew/lib \
        -lcurl \
        -lfreetype

SRC_DIR=src
BUILD_DIR=build

SRCS=$(SRC_DIR)/pokemon.c \
     $(SRC_DIR)/network.c \
     $(SRC_DIR)/pokemon_image.c \
     $(SRC_DIR)/main.c

OBJS=$(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)
TARGET=pokemon_fetcher

.PHONY: all clean directories

all: directories $(TARGET)

directories:
	@mkdir -p $(BUILD_DIR)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET) pokemon_*.png *.bmp *.png
CC=gcc
CFLAGS=-Wall -Wextra \
       -I./include \
       $(shell pkg-config --cflags cairo) \
       -I/opt/homebrew/include/freetype2 \
       -I/opt/homebrew/Cellar/curl/7.79.1/include

LDFLAGS=$(shell pkg-config --libs cairo) \
        -L/opt/homebrew/lib \
        -lcurl \
        -lfreetype

SRC_DIR=src
BUILD_DIR=build

SRCS=$(SRC_DIR)/pokemon.c \
     $(SRC_DIR)/network.c \
     $(SRC_DIR)/pokemon_image.c \
     $(SRC_DIR)/main.c

OBJS=$(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)
TARGET=pokemon_fetcher

.PHONY: all clean directories

all: directories $(TARGET)

directories:
	@mkdir -p $(BUILD_DIR)

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET) $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET) pokemon_*.png *.bmp *.png
