#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>


typedef struct {
  double addTime;
  double removeLastTime;
  double insertAtZeroTime;
  double removeAtZeroTime;
  double insertRandomTime;
  double removeRandomTime;
  double getRandomTime;
  int testName;
  char *arrayType;
} Measurement;


int peekRandomValue(int upper) {
  int number = (rand() % upper + 1);
  return number;
}


void representMeasurement(Measurement *ms) {
  printf("Testing %s at %d:\n", ms->arrayType, ms->testName);

  printf("Add element: %f s.\n", ms->addTime);
  printf("Remove last element: %f s.\n", ms->removeLastTime);
  printf("Insert at zero index: %f s.\n", ms->insertAtZeroTime);
  printf("Remove at zero index: %f s.\n", ms->removeAtZeroTime);
  printf("Insert at random index: %f s.\n", ms->insertRandomTime);
  printf("Remove at random index: %f s.\n", ms->removeRandomTime);
  printf("Getting at random index: %f s.\n\n", ms->getRandomTime);
}


void writeMeasurementsToFile(Measurement *ms, char *filename) {
  FILE *filep;

  if (access(filename, F_OK) == 0) {
    filep = fopen(filename, "a");
  } else {
    filep = fopen(filename, "w");
  }

  if (filep == NULL) {
    printf("ERROR: Can't open file");
    exit(1);
  }

  fprintf(filep, "\n\n Testing %s on %d\n", ms->arrayType, ms->testName);
  fprintf(filep, "Add last, Remove last, Insert at 0, Remove at 0, Insert at rnd, Remove at rnd, Get rnd\n");
  fprintf(filep, "%f, ", ms->addTime);
  fprintf(filep, "%f, ", ms->removeLastTime);
  fprintf(filep, "%f, ", ms->insertAtZeroTime);
  fprintf(filep, "%f, ", ms->removeAtZeroTime);
  fprintf(filep, "%f, ", ms->insertRandomTime);
  fprintf(filep, "%f, ", ms->removeRandomTime);
  fprintf(filep, "%f", ms->getRandomTime);
  fclose(filep);
}
