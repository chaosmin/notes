---
tags:
  - tech
category: Java
---

# Java：引用

## 四种引用类型

不同的引用类型，主要体现的是**对象不同的可达性（reachable）状态会对垃圾收集的影响**。

- **强引用（Strong Reference）**：最常见的普通对象引用，只要有强引用指向一个对象，垃圾收集器就不会碰这个对象。
- **软引用（Soft Reference）**：是一种相对强引用弱化一些的引用，可以让对象豁免一些垃圾收集，只有当 JVM 认为内存不足时，才会去试图回收软引用指向的对象。JVM 会确保在抛出 OOM 之前清理软引用指向的对象，所以软引用通常用来实现内存敏感的缓存。
- **弱引用（Weak Reference）**：并不能使对象豁免垃圾收集，仅仅是提供一种访问在弱引用状态下对象的途径。用于构建一种没有特定约束的关系，如维护一种非强制性的映射关系，如果试图获取时对象还在，则使用，否则重新实例化。
- **幻象引用**：虚引用，不能通过它访问对象。该引用仅仅是提供了一种确保对象被 finalize 以后，做某些事情的机制，如 Post-Mortem 清理机制。

## 扩展知识

### 引用队列 Reference Queue

在创建各种引用并关联到相应对象时，可以选择是否需要关联引用队列。JVM 会在特定时机将引用 enqueue 到队列里，我们可以从队列里获取引用进行相关后续逻辑。

```java
Object counter = new Object();
ReferenceQueue refQueue = new ReferenceQueue<>();
PhantomReference<Object> p = new PhantomReference<>(counter, refQueue);
counter = null;
System.gc();

try {
  Reference<Object> ref = refQueue.remove(1000L);
  if (ref != null) {
    // do something
  }
} catch (InterruptedException e) {
  // Handle it
}
```

### 显式地影响软引用垃圾收集

软引用通常会在最后一次引用后，保持一段时间，其默认值是根据堆剩余空间计算的（以M bytes为单位）。从 Java 1.3.1 开始，JVM 提供了 `-XX:SoftRefLRUPolicyMSPerMB` 参数，可以以毫秒（ms）为单位进行设置。

### Reachability Fence

有些时候，对象本身并没有强引用，但是它的部分属性还在被使用，这样就会导致诡异的问题。Java 9 的 `java.lang.ref.Reference` 提供了新方法：`static void reachabilityFence(Object ref)`，可以在没有强引用的情况下通知 JVM 对象是在被使用的。
