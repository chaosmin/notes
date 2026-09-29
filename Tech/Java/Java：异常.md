---
tags:
  - tech
category: Java
---

# Java：异常

## Exception vs Error

Exception 和 Error 都是继承自 Throwable 类，在 Java 中，只有 Throwable 类型的实例才可以被抛出或捕获，是异常处理机制的基本组成类型。

- **Exception** 是程序正常运行时，可以预料的意外情况，可能并且应该被捕获，进行相应处理。Exception 主要分为以下两类：
	- **可检查 Exception** 在源代码里必须显式地进行捕获处理，是编译期检查的一部分，比如 IOException。
	- **不检查 Exception** 就是所谓的运行时异常，类似 NullPointerException、ArrayIndexOutOfBoundsException 之类，通常是可以编码避免的逻辑错误，具体根据需要来判断是否需要捕获，并不会在编译期强制要求。
- **Error** 是指在正常情况下，不大可能出现的情况，绝大部分 Error 都会导致程序处于非正常的、不可恢复的状态。因此不便于也不需要捕获，如 OutOfMemoryError、StackOverflowError、NoClassDefFoundError、UnsatisfiedLinkError 等。

## NoClassDefFoundError vs ClassNotFoundException

- **NoClassDefFoundError** 产生的原因：如果 JVM 或者 ClassLoader 实例尝试加载类的时候却找不到类的定义。要查找的类在编译的时候是存在的，运行的时候却找不到类。造成该问题可能是打包过程漏掉了部分类，或 jar 包出现损坏或篡改。
- **ClassNotFoundException** 产生的原因：Java 支持使用反射的方式在运行时动态加载类，例如使用 Class.forName 方法来动态地加载类到 JVM 内存中。如果传递给上述方法的类在类路径中没有找到，那么就会抛出该异常。

## 最佳实践

**Throw early, catch late 原则**
