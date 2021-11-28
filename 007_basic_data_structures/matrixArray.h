#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_CHUNK_LENGTH 10
#define DEFAULT_CHUNKS_COUNT 10

typedef struct {
  int dataArr[10];
  size_t used;
} Chunk;

typedef Chunk* pChunk;

typedef struct {
  pChunk *array;
  size_t totalElements;
  size_t storedElements;
  size_t chunksAmount;
} MatrixArray;


void initMatrixArray(MatrixArray *ma) {
  int i;

  ma->array = malloc(sizeof(pChunk) * DEFAULT_CHUNKS_COUNT + 1);
  ma->totalElements = DEFAULT_CHUNK_LENGTH * DEFAULT_CHUNKS_COUNT;
  ma->storedElements = 0;
  ma->chunksAmount = DEFAULT_CHUNKS_COUNT;

  for (i = 0; i < ma->chunksAmount; i++) {
    ma->array[i] = malloc(sizeof(Chunk));
    ma->array[i]->used = 0;
  }
}


void resizeMatrixArray(MatrixArray *ma) {
  int i;
  pChunk *new_array = malloc(sizeof(pChunk) * ma->chunksAmount + 2);
  ma->chunksAmount += 1;

  for (i = 0; i < ma->chunksAmount - 1; i++) {
    new_array[i] = ma->array[i];
  }

  new_array[ma->chunksAmount - 1] = malloc(sizeof(Chunk));
  new_array[ma->chunksAmount - 1]->used = 0;

  free(ma->array);
  ma->array = NULL;
  ma->array = new_array;
  ma->totalElements += DEFAULT_CHUNK_LENGTH;
}


void addElement(MatrixArray *ma, int element) {
  int internal_idx, chunk_idx;

  if (ma->storedElements == ma->totalElements) {
    resizeMatrixArray(ma);
  }

  chunk_idx = ma->storedElements / DEFAULT_CHUNK_LENGTH;
  internal_idx = ma->storedElements % DEFAULT_CHUNK_LENGTH;
  ma->array[chunk_idx]->dataArr[internal_idx] = element;
  ma->storedElements++;
}


int getElement(MatrixArray *ma, int elementIndex) {
  int quotient, remainder;

  if (elementIndex >= ma->storedElements) {
    printf("Index %d is out of range\n", elementIndex);
    return 0;
  }

  quotient = elementIndex / DEFAULT_CHUNK_LENGTH;
  remainder = elementIndex % DEFAULT_CHUNK_LENGTH;

  return ma->array[quotient]->dataArr[remainder];
}


void removeLast(MatrixArray *ma) {
  int last_stored_chunk_idx, last_stored_element_idx;

  if (ma->storedElements == 0) {
    printf("Nothing to remove at last position.\n");
    return;
  }

  last_stored_chunk_idx = (ma->storedElements - 1) / DEFAULT_CHUNK_LENGTH;
  last_stored_element_idx = (ma->storedElements - 1) % DEFAULT_CHUNK_LENGTH;
  ma->array[last_stored_chunk_idx]->dataArr[last_stored_element_idx] = 0;
  ma->storedElements--;
}


int countElements(MatrixArray *ma) {
  return ma->storedElements;
}


void insertElement(MatrixArray *ma, int element, int elementIndex) {
  int internal_idx, chunk_idx, temp, i, j;

  if (elementIndex >= ma->storedElements) {
    printf("\ninsert: Index %d is out of range\n", elementIndex);
    return;
  }

  if (ma->storedElements == ma->totalElements) {
    resizeMatrixArray(ma);
  }

  chunk_idx = elementIndex / DEFAULT_CHUNK_LENGTH;
  internal_idx = elementIndex % DEFAULT_CHUNK_LENGTH;

  for (i = ma->chunksAmount - 1; i > chunk_idx; i--) {
    temp = ma->array[i - 1]->dataArr[DEFAULT_CHUNK_LENGTH - 1];

    for (j = DEFAULT_CHUNK_LENGTH - 1; j > 0; j--) {
      ma->array[i]->dataArr[j] = ma->array[i]->dataArr[j - 1];
    }

    ma->array[i]->dataArr[0] = temp;
  }

  for (j = DEFAULT_CHUNK_LENGTH - 1; j > internal_idx; j--) {
    ma->array[chunk_idx]->dataArr[j] = ma->array[chunk_idx]->dataArr[j - 1];
  }

  ma->array[chunk_idx]->dataArr[internal_idx] = element;
}


void removeAtIndex(MatrixArray *ma, int elementIndex) {
  int internal_idx, chunk_idx, temp, i, j;

  if (elementIndex >= ma->storedElements) {
    printf("\nremove: Index %d is out of range\n", elementIndex);
  }

  chunk_idx = elementIndex / DEFAULT_CHUNK_LENGTH;
  internal_idx = elementIndex % DEFAULT_CHUNK_LENGTH;

  for (j = internal_idx; j < DEFAULT_CHUNK_LENGTH - 1; j++) {
    ma->array[chunk_idx]->dataArr[j] = ma->array[chunk_idx]->dataArr[j + 1];
  }

  if (chunk_idx < ma->chunksAmount - 1) {
    for (i = chunk_idx + 1; i < DEFAULT_CHUNK_LENGTH; i++) {
      if (i != DEFAULT_CHUNK_LENGTH - 1) {
        ma->array[i - 1]->dataArr[DEFAULT_CHUNK_LENGTH - 1] = ma->array[i]->dataArr[0];
      }

      for (j = 0; j < DEFAULT_CHUNK_LENGTH - 1; j++) {
        ma->array[i]->dataArr[j] = ma->array[i]->dataArr[j + 1];
      }
    }
  }

  ma->storedElements--;
}


void freeMatrixArray(MatrixArray *ma) {
  int i;

  for (i = 0; i < ma->chunksAmount; i++) {
    free(ma->array[i]);
    ma->array[i] = NULL;
  }

  free(ma->array);
  ma->array = NULL;
  ma->totalElements = ma->storedElements = ma->chunksAmount = 0;
}

