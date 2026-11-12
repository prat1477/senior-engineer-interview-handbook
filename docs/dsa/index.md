---
title: DSA and Coding Interview Practice
description: Tracker and links to external DSA handbook material.
status: planned
audience: advanced
tags: [dsa, coding]
created: 2026-10-15
updated: 2026-10-15
---

# DSA and Coding Interview Practice

## DSA Handbook

**Not found** under `D:\Github` during handbook setup. When your DSA repository is available, add links below — **do not duplicate** the full curriculum here.

```text
<!-- Example when available:
External repo: D:\Github\dsa-handbook
Day 1: arrays, hash maps → link to lesson
Day 2: two pointers, sliding window → link to lesson
-->
```

## 14-day alignment

| Day | DSA focus | Status |
| --- | --- | --- |
| 1 | Arrays, hash-map problems, complexity | Planned |
| 2 | Two pointers, sliding window | Planned |
| 13–14 | Timed coding problems | Planned |

## Practised coding patterns

### Best Time to Buy and Sell Stock — one transaction

Given `prices`, choose one buy day before one sell day. The brute-force answer tests every
buy/sell pair, so its nested scan is **O(n²)**. A single scan is enough: retain the cheapest
price seen so far and compare today's sale profit to the best profit seen so far.

```java
static int maxProfitOneTransaction(int[] prices) {
    int minPrice = Integer.MAX_VALUE;
    int maxProfit = 0;

    for (int price : prices) {
        minPrice = Math.min(minPrice, price);
        maxProfit = Math.max(maxProfit, price - minPrice);
    }
    return maxProfit;
}
```

For `[7, 1, 5, 3, 6, 4]` the result is `5` (buy at `1`, sell at `6`).

| Price | Cheapest buy so far | Candidate sale profit | Best profit |
| ---: | ---: | ---: | ---: |
| 7 | 7 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 5 | 1 | 4 | 4 |
| 3 | 1 | 2 | 4 |
| 6 | 1 | 5 | 5 |
| 4 | 1 | 3 | 5 |

**Invariant:** before processing each price, `minPrice` is the minimum of all earlier prices
and `maxProfit` is the best legal transaction ending on or before the earlier day. A profitable
sale never changes the buy price: it is a candidate outcome, not evidence of a cheaper buy.
Only a new minimum changes `minPrice`; never reset `maxProfit` merely because the market falls.
A continuously decreasing input returns `0`. Time **O(n)**, auxiliary space **O(1)**.

Practice record: the first proposal was a brute-force scan and there was initial uncertainty
about when the buying price changes. The single-pass minimum-price idea was identified after
guided questioning and the final optimized solution was then implemented independently.

### Stock trading — unlimited sequential transactions

Here we may make as many non-overlapping trades as needed, hold at most one stock, pay no fee,
and have no cooldown. Sell before the next purchase. Sum every positive adjacent rise:

```java
static int maxProfitUnlimitedTransactions(int[] prices) {
    int profit = 0;
    for (int day = 1; day < prices.length; day++) {
        if (prices[day] > prices[day - 1]) {
            profit += prices[day] - prices[day - 1];
        }
    }
    return profit;
}
```

For `[1, 3, 2, 5, 4, 7]`, the positive rises are `2 + 3 + 3 = 8`.
For any increasing run `a < b < c`, `(b - a) + (c - b) = c - a`; splitting a rise does
not create extra profit, but it is safe and naturally captures every valley-to-peak interval.
Decreasing inputs return zero. Do not skip the next day after a sale: a sale at one local peak
can be followed by a purchase on the next day, and skipping it can lose a later rise. Time
**O(n)**, space **O(1)**.

Practice record: after the greedy principle was understood, the final Java solution was
implemented independently.

## Coding practice tracker

| # | Problem area | Problem | Attempted | Notes |
| --- | --- | --- | --- | --- |
| — | _Add rows as you practice_ | | | |

Update after each session; leave assessment columns empty until you practice.
