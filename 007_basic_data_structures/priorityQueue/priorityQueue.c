#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "priorityQueue.h"


int main() {
  PriorityQueueNode* head;

  head = initQueueNode(1, 1);

  head = enqueue(head, 42, 2);
  head = enqueue(head, 3, 1);
  head = enqueue(head, 12, 999);

  printQueueFrom(head);

  PriorityQueueNode* dequeuedElement = dequeue(&head);
  printf("Dequeued element value is: %d\n", dequeuedElement->value);

  printQueueFrom(head);
}

