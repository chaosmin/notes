---
tags:
  - tech
category: Java
---

# Java：多线程和并发

### 线程

- 从操作系统的角度，线程可以简单地认为是系统调度的最小单元，一个进程可以包含多个线程。作为任务的真正运行者，线程有自己的栈（Stack）、寄存器（Register）、本地存储（Thread Local）等，但是会和进程内其他线程共享文件描述符、虚拟地址空间等。
- 具体实现中，线程还分为 **内核线程**和**用户线程**。Java 的线程实现其实时与虚拟机相关的，现在的 JDK 模型是一对一映射到操作系统内核线程的。
- 【扩展】Java 在 Loom 项目中孕育新的类似轻量级用户线程 Fiber 等机制。
- 线程生命周期
	- **新建** NEW，表示线程被创建出来还没真正启动。
	- **就绪** RUNNABLE，表示线程已经在 JVM 中执行。它可能是正在运行，也可能在等待系统分配 CPU 时间片。
	- **运行** RUNNING，就绪状态的线程获得了 CPU 时间片。
	- **阻塞** BLOCKED，表示线程放弃了 CPU 的使用权，在等待 Monitor lock。
	- **等待** WAITING，表示正在等待其他线程采取某些操作。其他线程通过类似 notify 等动作通知消费线程可以继续工作。
	- **计时等待** TIMED_WAIT，其进入条件与等待状态类似，但是调用的是存在超时条件的方法。
	- **终止** TERMINATED，不管意外退出还是正常执行结束，线程已经完成使命，终止运行。
- 线程同步以及线程调度相关方法
	- wait() 使一个线程处于等待（阻塞）状态，并且释放所持有的对象的锁，是 Object 类的方法。
	- sleep() 使一个正在运行的线程处于睡眠状态，并不会释放锁，是 Thread 线程类的静态方法，调用此方法需要处理 InterruptedException 异常。
	- notify() 唤醒一个处于等待状态的线程，并不能确切地唤醒某一个等待状态的线程，而是由 JVM 确定。
	- notifyAll() 唤醒所有处于等待状态的线程，让它们竞争，只有获得锁的线程才能进入就绪状态。
- ThreadLocal
	- Java 提供的一种保存线程私有信息的机制。线程会在其内部维护一个 ThreadLocalMap 变量。
	- ```java
	  static class ThreadLocalMap {
	    static class Entry extends WeekReference<ThreadLocal<?>> {
	      Object value;
	      Entry(ThreadLocal<?> k, Object v) {
	        super(k);
	        value = v;
	      }
	    }
	    // ...
	  }
	  ```
	- ThreadLocal 废弃项目的回收**依赖于显式地触发**，否则就要等待**线程结束**，进而回收相应的 ThreadLocalMap。因此通常建议应用要自己负责 remove，并且不要和线程池配合，因为 worker 线程往往不会退出。

### 线程安全

- 按《Java并发编程实战》中的定义，线程安全是一个多线程环境下正确性的概念，也就是保证多线程环境下**共享的、可修改的**状态的正确性。进而可以得出保证线程安全的两个办法：
	- 封装：通过封装，可以将对象内部状态隐藏、保护起来。
	- 不可变：immutable
- 线程安全的基本特性
	- **原子性** 相关操作不会中途被其他线程干扰，一般通过同步机制实现
	- **可见性** 一个线程修改了某个共享变量，其状态能够立即被其他线程知晓
	- **有序性** 保证线程内串行语义，避免指令重排等

### 锁

- **synchronized** 是 Java 内建的同步机制，也可称为 Intrinsic Locking，它提供了互斥的语义和可见性，当一个线程已经获取当前锁时，其他试图获取的线程只能等待或者阻塞在那里。
	- synchronized 代码块是由一对 monitorenter / monitorexit 指令实现的。
	- 现代 JDK 对 Monitor 进行了改进，提供了三种实现：
		- 偏斜锁 Biased Locking：利用 CAS 操作在对象头的 Mark Word 部分设置线程 ID。
		- 轻量级锁：依赖 CAS 操作来试图获取锁，如果重试成功，就使用普通的轻量级锁。
		- 重量级锁：如果轻量级锁获取失败，则会升级为重量级锁。
	- synchronized 的三种使用方式：
		- 修饰实例方法：作用于当前对象实例加锁。
		- 修饰静态方法：给当前类加锁，会作用于类的所有对象实例。
		- 修饰代码块：指定加锁对象，对给定对象加锁。
- **ReentrantLock** 通常译为再入锁，语义和 synchronized 基本相同，通过代码直接调用 `lock()` 方法获取，能够实现很多 synchronized 无法做到的细节控制。必须明确调用 `unlock()` 方法释放。
	- 公平性 fairness：当公平性为真时，会倾向于将锁赋予等待时间最久的线程，减少"饥饿"。
	- **条件变量** `java.util.concurrent.Condition`：将 wait、notify、notifyAll 等操作转化为相应的对象。
- volatile 关键字
	- [[MESI协议]] 保证可见性及 **内存屏障** 禁止指令重排。volatile 提供 happens-before 的保证。
	- 从实践角度而言，volatile 的一个重要作用是**和 CAS 结合**来保证了原子性，如 AtomicInteger。
	- volatile 变量可以确保先行关系，即写操作会发生在后续的读操作之前，但它并不能保证原子性。

#### 死锁

- 死锁是一种特定的程序状态，由于循环依赖导致彼此一直处于等待之中，没有任何个体可以继续前进。
- 定位死锁最常见的方式是利用 jstack 等工具获取**线程栈**，然后定位相互之间的依赖关系。
- 死锁示例代码：

```java
public class DeadLockSample extends Thread {
  private String first;
  private String second;

  public void run() {
    synchronized (first) {
      try {
        Thread.sleep(1000L);
        synchronized (second) {
          System.out.println(this.getName() + " obtained: " + second);
        }
      } catch (InterruptedException e) { }
    }
  }

  public static void main(String[] args) throws InterruptedException {
    String lockA = "lockA";
    String lockB = "lockB";
    DeadLockSample t1 = new DeadLockSample("Thread1", lockA, lockB);
    DeadLockSample t2 = new DeadLockSample("Thread2", lockB, lockA);
    t1.start(); t2.start();
    t1.join(); t2.join();
  }
}
```

- 减少死锁出现的办法
	- 避免使用多个锁，并且只有需要时才持有锁
	- 设计好锁的获取顺序
	- 使用带超时的方法
- 无锁编程
	- AtomicStampedReference 解决 ABA 问题
	- LongAdder 替代 AtomicLong 高并发计数

### 并发包

- AbstractQueuedSynchronizer 实现各种同步结构和部分其他组成单元的基础
	- 一个 volatile 的整数成员 state 表征状态
	- 一个先入先出（FIFO）的等待线程队列
	- 各种基于[[CAS]]的基础操作方法
- 各种线程安全容器：`ConcurrentHashMap`、`ConcurrentSkipListMap`、`CopyOnWriteArrayList` 等。
- 各种并发队列：`ArrayBlockingQueue`、`SynchronousQueue`、`PriorityBlockingQueue` 等。
- 高级同步结构：`CountDownLatch`、`CyclicBarrier`、`Semaphore`、`Phaser`
- 原子操作类：`AtomicInteger`，基于[[CAS]]技术。

### 线程池

- Executors 提供的 5 种线程池创建配置：
	- newCachedThreadPool()：处理大量短时间工作任务，内部使用 SynchronousQueue。
	- newFixedThreadPool(int nThreads)：重用指定数目线程，使用无界工作队列。
	- newSingleThreadExecutor()：工作线程数目限制为1，保证任务顺序执行。
	- newScheduledThreadPool(int corePoolSize)：可进行定时或周期性工作调度。
	- newWorkStealingPool(int parallelism)：JDK 8，内部构建 ForkJoinPool，Work-Stealing 算法。
- 线程池核心参数：
	- **corePoolSize** 核心线程数
	- **maximumPoolSize** 最大线程数
	- **keepAliveTime + TimeUnit** 额外线程闲置时间
	- **workQueue** 工作队列（必须是 BlockingQueue）
	- **threadFactory** 用于创建 worker 线程
	- **rejectedExecutionHandler** 拒绝策略（AbortPolicy / CallerRunsPolicy / DiscardPolicy / DiscardOldestPolicy）
- 线程池大小选择策略
	- 计算密集型：CPU 核数 N 或 N+1
	- I/O 密集型：线程数 = CPU 核数 × 目标 CPU 利用率 × （1 + 平均等待时间 / 平均工作时间）
- 线程池关闭最佳实践：

```java
executor.shutdown();
try {
  if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
    List<Runnable> unfinished = executor.shutdownNow();
  }
} catch (InterruptedException e) {
  executor.shutdownNow();
}
```

### CAP 理论

- **一致性 [Consistency]**：所有节点在同一时刻数据完全一致。
- **可用性 [Availability]**：系统始终响应请求。
- **分区容错性 [Partition Tolerance]**：系统在网络分区时仍能运行。
- 现代分布式系统基本都要满足分区容错性，系统架构要么符合 AP，要么符合 CP。

#### 分布式数据一致性协议

- [[MESI协议]]
- Paxos / Raft / ZAB / 2PC / 虚拟同步
