---
tags:
  - tech
category: algorithms
---

# 算法：重复K次的最长子序列

#字符串 #深度优先搜索 #双指针 #回溯 #枚举

### 题目

> 给你一个长度为 `n` 的字符串 `s` ，和一个整数 `k` 。请你找出字符串 `s` 中**重复** `k` 次的**最长子序列**。
>
> **子序列**是由其他字符串删除某些（或不删除）字符派生而来的一个字符串。
>
> 如果 `seq * k` 是 `s` 的一个子序列，其中 `seq * k` 表示一个由 `seq` 串联 `k` 次构造的字符串，那么就称 `seq` 是字符串 `s` 中一个 **重复 `k` 次**的子序列。
>
> 举个例子，`"bba"` 是字符串 `"bababcba"` 中的一个重复 `2` 次的子序列，因为字符串 `"bbabba"` 是由 `"bba"` 串联 `2` 次构造的，而 `"bbabba"` 是字符串 `"bababcba"` 的一个子序列。
>
> 返回字符串 `s` 中**重复 k 次的最长子序列**。如果存在多个满足的子序列，则返回**字典序最大**的那个。如果不存在这样的子序列，返回一个**空**字符串。

示例 1：

![example 1](https://assets.leetcode.com/uploads/2021/08/30/longest-subsequence-repeat-k-times.png)

```
输入：s = "letsleetcode", k = 2
输出："let"
解释：存在两个最长子序列重复 2 次："let" 和 "ete" 。
"let" 是其中字典序最大的一个。
```

示例 2：

```
输入：s = "bb", k = 2
输出："b"
解释：重复 2 次的最长子序列是 "b" 。
```

示例 3：

```
输入：s = "ab", k = 2
输出：""
解释：不存在重复 2 次的最长子序列。返回空字符串。
```

### 思路

如果 `seq * k` 是 `s` 的子序列，则必须满足 `seq` 中的每个字母都在 `s` 中至少出现过 `k` 次。所以示例一中只有 l, e, t 这些至少出现了 `k` 次的字母，才有可能在 `seq` 中。

其中字母 e 出现了4次，这就意味着 `seq` 中可以有 $⌊\frac k 4​⌋=2$ 个 e。所以需要枚举 $a=[l,e,e,t]$ 的全排列。题目要求子序列尽量长，所以**优先枚举更长的排列**，此外把 `a` **从大到小排序**，这样长度相同时，字典序大的先枚举到。

之后再返回第一个符合枚举到的 `seq * k` 为 `s` 的子序列即可。

### 代码

```java
class Solution {
    private char[] ans;
    private int ansLen = 0;

    public String longestSubsequenceRepeatedK(String S, int k) {
        char[] s = S.toCharArray();

        // 392. 判断子序列（进阶做法）
        int n = s.length;
        int[] cnt = new int[26];
        int[][] nxt = new int[n + 1][];
        nxt[n] = new int[26];
        Arrays.fill(nxt[n], n);
        for (int i = n - 1; i >= 0; i--) {
            int c = s[i] - 'a';
            nxt[i] = nxt[i + 1].clone();
            nxt[i][c] = i;
            cnt[c]++;
        }

        StringBuilder tmp = new StringBuilder();
        // 倒序，这样我们可以优先枚举字典序大的排列
        for (int i = 25; i >= 0; i--) {
            String c = String.valueOf((char) ('a' + i));
            tmp.append(c.repeat(cnt[i] / k));
        }
        char[] a = tmp.toString().toCharArray();

        ans = new char[a.length];
        permute(a, k, nxt);

        return new String(ans, 0, ansLen);
    }

    // 47. 全排列 II
    // 枚举从 nums 中选任意个数的所有排列，处理枚举的排列
    private void permute(char[] nums, int k, int[][] nxt) {
        int n = nums.length;
        char[] path = new char[n];
        boolean[] onPath = new boolean[n]; // onPath[j] 表示 nums[j] 是否已经填入排列
        dfs(0, nums, path, onPath, k, nxt);
    }

    private void dfs(int i, char[] nums, char[] path, boolean[] onPath, int k, int[][] nxt) {
        // 处理当前排列 path
        process(path, i, k, nxt);

        if (i == nums.length) {
            return;
        }

        // 枚举 nums[j] 填入 path[pathLen]
        for (int j = 0; j < nums.length; j++) {
            // 如果 nums[j] 已填入排列，continue
            // 如果 nums[j] 和前一个数 nums[j-1] 相等，且 nums[j-1] 没填入排列，continue
            if (onPath[j] || j > 0 && nums[j] == nums[j - 1] && !onPath[j - 1]) {
                continue;
            }
            path[i] = nums[j]; // 填入排列
            onPath[j] = true; // nums[j] 已填入排列（注意标记的是下标，不是值）
            dfs(i + 1, nums, path, onPath, k, nxt); // 填排列的下一个数
            onPath[j] = false; // 恢复现场
            // 注意 path 无需恢复现场，直接覆盖 path[i] 就行
        }
    }

    private void process(char[] seq, int seqLen, int k, int[][] nxt) {
        // 先比大小（时间复杂度低），再判断是否为子序列（时间复杂度高）
        if (seqLen > ansLen || seqLen == ansLen && compare(seq, ans, ansLen) > 0) {
            if (isSubsequence(seq, seqLen, k, nxt)) {
                System.arraycopy(seq, 0, ans, 0, seqLen);
                ansLen = seqLen;
            }
        }
    }

    // 比较 a 和 b 的字典序大小
    private int compare(char[] a, char[] b, int n) {
        for (int i = 0; i < n; i++) {
            if (a[i] != b[i]) {
                return a[i] - b[i];
            }
        }
        return 0;
    }

    // 392. 判断子序列
    // 返回 seq*k 是否为 s 的子序列
    private boolean isSubsequence(char[] seq, int n, int k, int[][] nxt) {
        int i = -1;
        while (k-- > 0) {
            for (int j = 0; j < n; j++) {
                char c = seq[j];
                i = nxt[i + 1][c - 'a'];
                if (i + 1 == nxt.length) { // c 不在 s 中，说明 seq*k 不是 s 的子序列
                    return false;
                }
            }
        }
        return true;
    }
}
```

### 复杂度分析

- 时间复杂度：$O((\frac n k)!⋅n)$，其中 `n` 是 `s` 的长度。注意 $∑_{i=0}^{m}A_m^i$ 就是全排列搜索树的节点个数，全排列搜索树的节点个数为 $⌊e⋅m!⌋$，其中 $e=2.718⋯$ 为自然常数。比如 `m=7` 时，$∑_{i=0}^{7}A_7^i = 13700 = ⌊e⋅7!⌋$。当 `m=n/k` 时，遍历这棵搜索树需要 $O((\frac n k)!)$ 的时间，每个节点判断子序列需要 $O(n)$ 的时间。
- 空间复杂度：$O(n|Σ|)$。其中 $|Σ|=26$ 是字符集合的大小。
