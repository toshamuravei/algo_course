#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dynamicArray.h"
#include "measurements.h"


void fillArrayForTests(DynamicArray *arr, int N) {
  int i;
  for (i = 0; i < N; i++) {
    addElement(arr, i);
  }
}

void runTests(DynamicArray *arr, Measurement *ms, int arraySize) {
  int randomIndex;
  clock_t begin, end;
  char fileNameBuffer[64];

  sprintf(fileNameBuffer, "%s-test.txt", arr->arrayType);

  // 1. add to end

  begin = clock();
  addElement(arr, 42);
  end = clock();
  ms->addTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 2. remove last

  begin = clock();
  removeLast(arr);
  end = clock();
  ms->removeLastTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 3. insert at zero

  begin = clock();
  insertElement(arr, 42, 0);
  end = clock();
  ms->insertAtZeroTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 4. remove at zero

  begin = clock();
  removeElementAtIndex(arr, 0);
  end = clock();
  ms->removeAtZeroTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 5. insert random

  begin = clock();
  randomIndex = peekRandomValue(arraySize - 1);
  insertElement(arr, 42, randomIndex);
  end = clock();
  ms->insertRandomTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 6. remove random

  begin = clock();
  randomIndex = peekRandomValue(arraySize - 1);
  removeElementAtIndex(arr, randomIndex);
  end = clock();
  ms->removeRandomTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 7. get random

  begin = clock();
  randomIndex = peekRandomValue(arraySize - 1);
  getElement(arr, randomIndex);
  end = clock();
  ms->getRandomTime = (double)(end - begin) / CLOCKS_PER_SEC;

  representMeasurement(ms);
  writeMeasurementsToFile(ms, fileNameBuffer);
}


void initAndRun(int arraySize, char *arrayType) {
  DynamicArray arr;
  Measurement ms;
  int initialSize = 100;

  initArray(&arr, initialSize, arrayType);
  fillArrayForTests(&arr, arraySize);

  ms.arrayType = arrayType;
  ms.testName = arraySize;

  runTests(&arr, &ms, arraySize);
  freeArray(&arr);
}


int main(int argc, char *argv[]){
  int i;
  int tests[5] = {1000, 10000, 100000, 1000000, 10000000};
  char* arrayTypeArg;

  if (argc >= 2) {
    arrayTypeArg = argv[1];
  } else {
    printf("\nArray Type name as argument expected\n");
    exit(1);
  }

  for (i = 0; i < 5; i++) {
    initAndRun(tests[i], arrayTypeArg);
  }
}

