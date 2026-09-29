---
tags:
  - tech
category: algorithms
---

# 算法：LRU缓存

#哈希表 #链表

## 题目

请你设计并实现一个满足 LRU（最近最少使用）缓存约束的数据结构。

## 思路

## 代码

```java
class LRUCache {
    class Node {
        int key;
        int value;
        Node prev;
        Node next;

        public Node() {}

        public Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private Map<Integer, Node> map = new HashMap<>();
    private int size;
    private int capacity;
    private Node head, tail;

    public LRUCache(int capacity) {
        this.size = 0;
        this.capacity = capacity;
        head = new Node();
        tail = new Node();
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        moveToHead(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node == null) {
            Node newNode = new Node(key, value);
            map.put(key, newNode);
            addToHead(newNode);
            size++;
            if (size > capacity) {
                Node tail = removeTail();
                map.remove(tail.key);
                size--;
            }
        } else {
            node.value = value;
            moveToHead(node);
        }
    }

    private void addToHead(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void moveToHead(Node node) {
        removeNode(node);
        addToHead(node);
    }

    private Node removeTail() {
        Node res = tail.prev;
        removeNode(res);
        return res;
    }
}
```

## 复杂度分析

- 时间复杂度：对于 `put` 和 `get` 都是 $O(1)$。
- 空间复杂度：$O(capacity)$，因为哈希表和双向链表最多存储 capacity+1 个元素。
