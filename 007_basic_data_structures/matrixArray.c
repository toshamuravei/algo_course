#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "measurements.h"
#include "matrixArray.h"

#define DEFAULT_CHUNK_LENGTH 10
#define DEFAULT_CHUNKS_COUNT 10


void fillArrayForTests(MatrixArray *ma, int N) {
  int i;
  for (i = 0; i < N; i++) {
    addElement(ma, i);
  }
}

void runTests(MatrixArray *arr, Measurement *ms, int arraySize) {
  int randomIndex;
  clock_t begin, end;

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
  removeAtIndex(arr, 0);
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
  removeAtIndex(arr, randomIndex);
  end = clock();
  ms->removeRandomTime = (double)(end - begin) / CLOCKS_PER_SEC;

  // 7. get random

  begin = clock();
  randomIndex = peekRandomValue(arraySize - 1);
  getElement(arr, randomIndex);
  end = clock();
  ms->getRandomTime = (double)(end - begin) / CLOCKS_PER_SEC;

  representMeasurement(ms);
  writeMeasurementsToFile(ms, "matrixArrayTests.txt");
}

void initAndRun(int arraySize) {
  MatrixArray ma;
  Measurement ms;

  initMatrixArray(&ma);
  fillArrayForTests(&ma, arraySize);

  ms.arrayType = "Matrix Array";
  ms.testName = arraySize;

  runTests(&ma, &ms, arraySize);
  freeMatrixArray(&ma);
}

int main(void) {
  int i;
  int tests[5] = {1000, 10000, 100000, 1000000, 10000000};

  //init array
  for (i = 0; i < 5; i++) {
    initAndRun(tests[i]);
  }
  // begining tests
  // 1. add
  // TODO: investigate why on large chunk length corruption top size is got

}

/*
Создать динамический массив двумя способами:
+1 байт - SingleArray
+1 байт - VectorArray
+1 байт - FactorArray
+1 байт - MatrixArray

Реализовать в каждом классе следующие методы:
int count(); // вернуть количество элементов в массиве
void add(T item);  // добавить элемент в конец массива
void removeLast(); //  удалить элемент в конце массива
T get(int index);  //  вернуть элемент по указанному индексу

УРОВЕНЬ MIDDLE

Дополнительно реализовать в каждом классе следующие методы:
+1 байт - void insert(T item, int index); // вставить элемент в указанную позицию
+1 байт - void remove(int index); // удалить элемент из указанной позиции со сдвигом

+2 байта - вычислить суммарное время выполнения каждого метода:
add(T)
removeLast()
insert(T, 0)
remove(T, 0)
insert(T, random)
remove(T, random)
get(random)

для реализованных динамических массивов для указанного количества элементов:
10^3, 10^4, 10^5, 10^6, 10^7.

+1 байт - занести замеры в таблицу, сравнить их, сделать выводы и сформулировать их в нескольких предложениях.
 */
