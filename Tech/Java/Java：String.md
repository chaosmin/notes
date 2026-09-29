---
tags:
  - tech
category: Java
---

# Java：String

## String

**String** 是 Java 中非常基础和重要的类，它被声明为 final class，所有的属性也都是 final 的，是典型的 Immutable 类。因此类似拼接、裁剪等动作都会产生新的 String 对象。

## StringBuffer

**StringBuffer** 是为了解决拼接产生太多中间对象的问题而提供的类，其本质上是一个**线程安全**的可修改字符序列。

## StringBuilder

**StringBuilder** 是 Java 1.5 中新增的类，在能力上与 StringBuffer 没有本质区别，但是它去掉了线程安全的部分，有效减少了开销。
