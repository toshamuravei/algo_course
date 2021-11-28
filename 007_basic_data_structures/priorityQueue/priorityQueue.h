#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct queueNode {
  int value;
  int priority;
  struct queueNode* next;
} PriorityQueueNode;


void printQueueFrom(PriorityQueueNode* fromNode) {
  PriorityQueueNode* currentNode = fromNode;

  while(currentNode != NULL) {
    printf("node value: %d | node priority: %d\n", currentNode->value, currentNode->priority);
    currentNode = currentNode->next;
  }

  printf("\n\n");
}


PriorityQueueNode* initQueueNode(int initValue, int initPriority) {
  PriorityQueueNode* node = (PriorityQueueNode*) malloc(sizeof(PriorityQueueNode));

  node->value = initValue;
  node->priority = initPriority;
  node->next = NULL;

  return node;
}


PriorityQueueNode* enqueue(PriorityQueueNode* head, int value, int priority) {
  PriorityQueueNode* currentNode = head;
  PriorityQueueNode* previousNode = NULL;
  PriorityQueueNode* newNode = initQueueNode(value, priority);

  // new node has highest priority
  if (newNode->priority >= head->priority) {
    newNode->next = head;
    return newNode;
  }

  // new node somewhere in the list
  while(currentNode != NULL) {
    previousNode = currentNode;
    currentNode = previousNode->next;
    if (newNode->priority >= currentNode->priority) {
      previousNode->next = newNode;
      newNode->next = currentNode;
      break;
    }
  }

  //new node in the end
  previousNode->next = newNode;
  return head;
}


PriorityQueueNode* dequeue(PriorityQueueNode** head) {
  PriorityQueueNode* highestPriorityNode = *head;

  (*head) = (*head)->next;

  return highestPriorityNode;
}


