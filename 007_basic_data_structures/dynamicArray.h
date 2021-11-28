#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARRAY_SCALE_FACTOR 2
#define ARRAY_SCALE_VECTOR 100

typedef struct {
  int* array;
  size_t used;
  size_t size;
  char* arrayType;
} DynamicArray;


void initArray(DynamicArray *a, size_t initialSize, char *arrayType){
  a->array = (int*)malloc(initialSize * sizeof(int));
  a->used = 0;
  a->size = initialSize;
  a->arrayType = arrayType;
}

int getNewSize(DynamicArray *a) {
  int newSize = 0;

  if (strcmp(a->arrayType, "FactorArray") == 0) {
    newSize = a->size * ARRAY_SCALE_FACTOR;
  } else if (strcmp(a->arrayType, "SingleArray") == 0) {
    newSize = a->size + 1;
  } else if (strcmp(a->arrayType, "VectorArray") == 0) {
    newSize = a->size + ARRAY_SCALE_VECTOR;
  } else {
    printf("\nERR: Can't assign new size for array %s\n", a->arrayType);
  }

  return newSize;
}

void resizeArray(DynamicArray *a){
  int i = 0;
  int new_size = 0;
  int* new_array_ptr = NULL;

  new_size = getNewSize(a);
  if (new_size == 0){
    exit(1);
  }

  new_array_ptr = (int*)malloc(new_size * sizeof(int));

  for (i = 0; i < a->size; i++){
    new_array_ptr[i] = a->array[i];
  }
  free(a->array);
  a->array = NULL;

  a->array = new_array_ptr;
  a->size = new_size;
}


void addElement(DynamicArray *a, int element){
  if (a->used == a->size){
    resizeArray(a);
  }
  a->array[a->used++] = element;
}


int getElement(DynamicArray *a, int elementIndex) {
  if (elementIndex >= a->used) {
    printf("Index %d is out of range\n", elementIndex);
    return 0;
  }
  return a->array[elementIndex];
}


void removeLast(DynamicArray *a) {
  if (a->used == 0) {
    printf("Nothing to remove at last position.\n");
    return;
  }
  a->array[a->used--] = 0;
}


void insertElement(DynamicArray *a, int element, int elementIndex) {
  int* moveTo;
  int* moveFrom;
  int nBytes;

  if (elementIndex >= a->used) {
    printf("Index %d is out of range\n", elementIndex);
    return;
  }

  if (a->used == a->size) {
    resizeArray(a);
  }

  moveTo = &a->array[elementIndex + 1];
  moveFrom = &a->array[elementIndex];
  nBytes = &a->array[a->used] - &a->array[elementIndex];

  memmove(moveTo, moveFrom, nBytes);
  a->array[elementIndex] = element;
}


void removeElementAtIndex(DynamicArray *a, int elementIndex) {
  int* moveTo;
  int* moveFrom;
  int nBytes;

  if (elementIndex >= a->used) {
    printf("Index %d is out of range\n", elementIndex);
  }

  moveTo = &a->array[elementIndex];
  moveFrom = &a->array[elementIndex + 1];
  nBytes = &a->array[a->used] - &a->array[elementIndex];

  memmove(moveTo, moveFrom, nBytes);
}

int countElements(DynamicArray *a) {
  return a->used;
}


void freeArray(DynamicArray *a){
  free(a->array);
  a->array = NULL;
  a->used = a->size = 0;
}

