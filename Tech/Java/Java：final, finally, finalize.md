---
tags:
  - tech
category: Java
---

# Java：final, finally, finalize

## 典型回答

### final

final 关键字是用来修饰类、方法、变量。表示不可继承扩展、不可修改、不可重写。

### finally

finally 关键字是 try-catch-finally 机制的一部分，主要用来保证重点代码一定被执行的机制，如关闭资源等。

### finalize

finalize 是基础类 java.lang.Object 的一个方法，用于保证对象在被GC前完成特定资源的回收。（该机制目前已不推荐使用，并在 JDK9 开始被标记为 deprecated）

## 考点分析

### final

- 被定义为 final 的参数或变量产生了某种程度的不可变（immutable）效果，用于保护只读数据，避免意外赋值导致的编程错误。尤其是在并发编程中，明确地不能再赋值的 final 变量，有利于减少额外的同步开销，也可以省去一些防御性拷贝的必要。
- 也许会有性能上的好处，利用 final 可能有助于 JVM 将方法进行内联，改善编译器进行条件编译的能力。

### finally

- 常用于关闭一些 IO/池 连接等资源，但是更推荐使用 JDK7 中添加的 try-with-resources 语句。

### finalize

- 业界实践一再证明不是一个好的解决方案，如果没有特别的原因不要指望利用该方法来进行资源回收。我们无法判断 finalize 什么时候执行，执行的是否符合预期。在使用不当的情况下甚至会影响性能，导致程序死锁，挂起等。

## 知识扩展

### final 并不等同于 immutable

被 final 修饰的 List 对象行为并不会被 final 影响，其只能约束这个引用不可以被赋值，添加元素等操作是完全正常的。

如果需要实现 immutable 类需要满足以下条件：
- 将 class 自身声明为 final，这样就无法通过扩展来绕开限制；
- 将所有成员变量定义为 private 和 final，并且不要实现 setter 方法；
- 通常构造对象时，成员变量使用深拷贝来初始化；
- 如果需要实现 getter 方法，使用 copy-on-write 原则，创建私有 copy 而不是直接返回引用。

### String类被定义为 final 的原因

- **安全性**：防止敏感数据被篡改、保证类加载机制（依赖字符串，如类名）的安全
- **性能优化**：支持字符串常量池、哈希码缓存、JVM内联
- **线程安全**：无锁共享、简化并发编程
- **哈希键可靠性**：确保Hash集合的稳定性和正确性

### finally 中的 return 语句

finally 代码块中的 return 语句会覆盖之前暂存的返回值，无论 try 或 catch 块中是否有返回值或异常，都会被其隐藏。强烈不推荐在 finally 中使用 return，会导致代码可读性变差、破坏异常处理机制、违背设计初衷等问题。

### finalize 的性能问题

finalize 被设计成在对象**被垃圾收集前**调用，意味着 JVM 需要对它进行额外处理，一旦实现了非空的 finalize 方法，会导致相应对象回收呈现数量级上的变慢，大概是 40～50 倍的下降。本质上成了快速回收的阻碍者，可能导致对象经过多个垃圾收集周期才能被回收。

### Cleaner 替代方案

Java 平台正逐步使用 java.lang.ref.Cleaner 来替换原来 finalize 实现。Cleaner 的实现利用了幻象引用（PhantomReference），这是一种常见的所谓 post-mortem 清理机制。利用幻象引用和引用队列，可以保证对象被彻底销毁前做一些类似资源回收的工作，比起 finalize 更加轻量和可靠。

### 实际应用案例

MySQL JDBC driver 之一的 mysql-connector-j，就采用了幻象引用机制，进行总量控制的场景，保证只有连接被关闭，相应资源被回收，连接池才能创建新的连接。
