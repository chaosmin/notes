---
tags:
  - tech
category: Java
---

# Java核心技术面试精讲

## 对Java的认识

1. 面向对象编程
2. Java虚拟机 和 GC
3. Write once，run anywhere
4. 丰富的生态

## Java 基础篇

### S.O.L.I.D 原则

- **单一职责 Single Responsibility**：类或者对象最好是只有单一职责
- **开关原则 Open-Close**：程序设计应保证平滑的扩展性，尽量避免因为新增同类功能而修改已有实现
- **里氏替换 Liskov Substitution**：进行继承关系抽象时，凡是可以用父类或基类的地方，都可以用子类替换
- **接口分离 Interface Segregation**：如果一个接口定义了太多方法，应该通过拆分成功能单一的多个接口，将行为进行解耦
- **依赖反转 Dependency Inversion**：实体应该依赖于抽象而不是实现

[[设计模式]]

## 并发篇

学习总结 [[Java：多线程和并发]]

## 类加载篇

### 双亲委派模型

- 加载 -> 链接 -> 初始化
- 加载阶段 Loading，将字节码数据从不同的数据源读取到 JVM 中，并映射为 JVM 认可的数据结构（Class 对象）
	- 启动类加载器 Bootstrap Class-Loader
	- 扩展类加载器 Extension or Ext Class-Loader -> 平台类加载器 Platform Class-Loader
	- 应用类加载器 Application or App Class-Loader
- 链接 Linking，把原始的类定义信息平滑地转化入 JVM 运行的过程中。
	1. 验证 Verification，核验字节信息是符合 Java 虚拟机规范的，否则就被认为是 VerifyError。
	2. 准备 Preparation，创建类或接口中的静态变量，并初始化静态变量的初始值。
	3. 解析 Resolution，将常量池中的符号引用（symbolic reference）替换为直接引用。
- 初始化 Initialization，执行类初始化的代码逻辑，包括静态字段赋值，执行类定义中的静态初始化块内的逻辑。
- **双亲委派模型 Parent-Delegation Model**：每个类加载器实例都有一个父类加载器，当需要加载一个类时，首先委派给父类加载器去尝试加载。可以避免重复加载 Java 类型。

## JVM 篇

### JVM 内存区域划分

- **程序计数器** Program Counter Register，每个线程都有自己的程序计数器，存储当前线程正在执行的 Java 方法的 JVM 指令地址。
- **Java 虚拟机栈** Java Virtual Machine Stack，每个线程在创建时都会创建一个虚拟机栈，其内部保存一个个的栈帧 Stack Frame，对应着一次次的 Java 方法调用。
- **本地方法栈** Native Method Stack，支持对本地方法的调用，每个线程都会创建一个。
- **堆** Heap，Java 内存管理的核心区域，用来放置 Java 对象实例，堆被所有的线程共享。
	- 新生代：Eden 区域、两个 Survivor 区域（from、to 区域）。
	- 老年代：放置长生命周期的对象。
	- 永久代：早期 Hotspot JVM 的方法区实现方式，JDK 8 之后移除。
- **方法区** Method Area，所有线程共享，用于存储元（Meta）数据，例如类结构信息，及对应的运行时常量池、字段、方法代码等。
- **运行时常量池** Run-Time Constant Pool，方法区的一部分，存放各种常量信息。

### 垃圾收集器

- **Serial GC**：单线程，进行垃圾收集时 Stop-The-World。`-XX:UseSerialGC`
- **ParNew GC**：Serial GC 的多线程版本，常配合老年代 CMS GC 工作。
- **CMS(Concurrent Mark Sweep) GC**：基于标记-清除算法，尽量减少停顿时间，但存在内存碎片化问题。
- **Parallel GC**：JDK 8 server 模式默认，新生代和老年代 GC 都是并行进行的。`-XX:UseParallelGC`
- **G1 GC**：Oracle JDK 9+ 默认，兼顾吞吐量和停顿时间，内存结构为一个个 region。
- **Epsilon GC**：不做垃圾收集，适用于性能测试场景。
- **ZGC**：支持 T bytes 级别的堆大小，超低延迟。

### 对象实例收集算法

- **引用计数法**：为对象添加引用计数，计数为 0 即可回收。需注意 **循环引用** 问题。Python 使用该算法。
- **可达性分析**：选定活动的对象作为 GC Roots，跟踪引用链条，不可达对象即可回收。Java 使用该算法。

### 垃圾收集算法

- **Minor GC**：复制算法，将 Eden 区及 From 区存活对象复制到 To 区域，拷贝过程中将对象顺序放置，避免内存碎片化。
- **Full GC**：
	- 标记-清除算法：标识出所有要回收的对象，然后进行清除。会有内存碎片化问题。
	- 标记-整理算法：类似于标记-清除，在清理过程中将对象移动，确保移动后的对象占用连续的内存空间。

## 数据库事务隔离级别

- Read uncommitted 读未提交，最低的隔离水平，允许脏读出现
- Read committed 读已提交，允许不重复读和幻读出现
- Repeatable reads 可重复读，InnoDB 引擎默认隔离级别
- Serializable 串行化，最高隔离级别，读取需要获取共享读锁，更新需要获取排他写锁

## 其他知识点

- Lambda 并不是语法糖，而是一种新的工作机制，在首次调用时，JVM 需要为其构建 CallSite 实例。
- ulid 的前48位为毫秒级时间戳，后80位为随机数，确保标识符按生成时间严格递增。采用 Crockford's Base32编码，仅需26位字符，比uuid的36字符缩短 28%，与 uuid 无缝替换。
