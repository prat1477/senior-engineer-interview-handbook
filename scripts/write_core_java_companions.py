"""Rewrite Core Java Interview Companion lessons with diagrams and scenarios."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs/books/02-interview-companion/core-java"

def page(mod, fname, num, title, definition, remember, traps, mermaid, scenario, decisions, explain, revision, hook):
    mastery = f"../../../01-engineering-mastery/core-java/{mod}/{fname}"
    bullets = "\n".join(f"- {b}" for b in remember)
    trap_lines = "\n".join(f"- {t}" for t in traps)
    dec = "\n".join(f"| {a} | {b} |" for a, b in decisions)
    exp = "\n".join(f"{i}. {e}" for i, e in enumerate(explain, 1))
    return f"""---
title: "Companion {num} — {title}"
description: Interview recall for {title}.
status: covered
audience: advanced
tags: [interview, companion, java]
updated: 2026-10-28
---

# Companion {num} — {title}

**Canonical source:** [Mastery lesson]({mastery}).

**Cheat sheet:** [Module visual quick reference](module-visual-quick-reference.md).

## Definition

{definition}

## Must remember

{bullets}

## Interview traps

{trap_lines}

## Interview flow

```mermaid
{mermaid}
```

## Scenario bite

{scenario}

## Decision table

| Situation | Prefer |
| --- | --- |
{dec}

## Explain aloud (whiteboard)

{exp}

## 30-second revision

- {revision}

## Memory hook

- {hook}

## Cross-links

- [Module visual quick reference](module-visual-quick-reference.md)
"""

# (mod, file, num, title, definition, remember, traps, mermaid, scenario, decisions, explain, revision, hook)
LESSONS = []

def add(*args):
    LESSONS.append(args)

add(
"module-08-exception-handling", "01-throwable-hierarchy-and-propagation.md", "1", "Throwable hierarchy",
"Java errors and exceptions form a hierarchy: Error, Exception, checked vs unchecked — propagation follows the call stack until caught or the thread dies.",
["Throwable → Error (JVM) vs Exception.", "Checked exceptions must be declared or caught; RuntimeException is unchecked.", "Catch the narrowest type you can handle; do not swallow.", "Use exceptions for exceptional paths, not control flow in hot loops."],
["Catching Exception hides bugs — catch specific types.", "Error is not for application catch-all (OutOfMemoryError)."],
"""flowchart TD
  throw[throw] --> stack[Unwind stack]
  stack --> caught{catch matches?}
  caught -->|yes| handle[Handle or wrap]
  caught -->|no| caller[Propagate to caller]
""",
"Payment API throws a checked validation failure at the controller boundary; a NullPointerException deeper in mapping should not be mapped to the same 400.",
[("Client mistake", "Unchecked or domain exception → 4xx"), ("Dependency down", "Wrap and retry policy, often 503"), ("Programmer bug", "Let unchecked fail fast, fix code")],
["Name checked vs unchecked.", "Show stack unwind until a handler.", "Say what you would not catch (Error, broad Exception)."],
"Checked must be handled; unchecked signals bugs or domain policy you choose to declare.",
"**CUE** — Checked, Unchecked, Error.",
)
add(
"module-08-exception-handling", "02-try-with-resources-and-wrapping.md", "2", "Try-with-resources and wrapping",
"try-with-resources closes AutoCloseable in reverse order and can suppress secondary exceptions; wrapping preserves the cause chain.",
["Resources close even when the body throws.", "Suppressed exceptions attach to the primary via getSuppressed().", "Wrap with cause: new ServiceException(msg, cause).", "Do not lose the original stack when translating to HTTP."],
["Empty catch after close — leaks the real failure.", "Wrapping without cause drops diagnostics."],
"""flowchart LR
  open[Open resource] --> body[Use]
  body --> close[Auto close]
  close --> primary[Primary exception]
  close --> suppressed[Suppressed on close failure]
""",
"Reading an order export file: if parsing throws and close also throws, the parse exception stays primary and close is suppressed.",
[("Need deterministic close", "try-with-resources"), ("Translate to API type", "Wrap with cause"), ("Log and continue", "Only if failure is truly optional")],
["Open, use, auto-close order.", "Primary vs suppressed.", "Always pass cause when wrapping."],
"try-with-resources closes reliably; wrapping must keep the cause.",
"**WRAP** — With cause, Reverse close, Attach suppressed, Primary wins.",
)
add(
"module-08-exception-handling", "03-production-spring-retries-idempotency.md", "3", "Retries and idempotency",
"Retries are safe only when the operation is idempotent or the failure happened before any side effect; payments need a stable idempotency key.",
["Separate retryable (timeout, 503) from fatal (400 validation).", "Bounded attempts and backoff with jitter.", "Idempotency key reused across retries — not a new UUID each click.", "DB transaction cannot roll back an external charge."],
["Retrying a non-idempotent POST doubles the charge.", "Infinite retry on a bug."],
"""flowchart TD
  call[Call provider] --> ok{Outcome}
  ok -->|success| store[Store SUCCEEDED]
  ok -->|timeout| same[Retry SAME idempotency key]
  same --> call
""",
"Client double-submits Pay with a new UUID each time — unique constraint does not dedupe. Reuse Idempotency-Key or a payment intent id.",
[("Transient 503", "Retry with same key"), ("Validation 400", "Do not retry"), ("Unknown after timeout", "Query provider, do not new charge")],
["Classify the failure.", "Same business key on retry.", "Effectively-once, not magic exactly-once."],
"Retry only idempotent or keyed operations; persist outcome before assuming success.",
"**KEY** — Keep the same idempotency key.",
)

# Collections 13 lessons — abbreviated unique content
COLS = [
("01-collections-framework-overview.md", "1", "Collections framework",
 "The Collections Framework is interfaces (Collection, List, Set, Queue, Map) plus implementations with different complexity and ordering.",
 ["Program to interfaces.", "Map does not extend Collection.", "Choose by access pattern and thread-safety.", "Fail-fast iterators detect structural modification."],
 ["Interface Big-O equals every implementation — read the class javadoc."],
 """flowchart TD
  need{Need} --> list[List ordered index]
  need --> set[Set uniqueness]
  need --> map[Map key value]
  need --> q[Queue FIFO or priority]
""",
 "Payroll groups employees by department: Map, not a List scan, when lookup by key dominates.",
 [("Random access", "ArrayList"), ("Unique keys", "Set or Map"), ("FIFO tasks", "Queue")],
 ["Name the interface first.", "Then the implementation.", "State one complexity."],
 "Interfaces first; Map is separate; pick implementation by access.",
 "**LSMQ** — List, Set, Map, Queue."),
("02-arraylist-vs-linkedlist.md", "2", "ArrayList vs LinkedList",
 "ArrayList is a growable array; LinkedList is a doubly linked list — random access and cache behavior differ sharply.",
 ["ArrayList get(i) is O(1); LinkedList get(i) is O(n).", "Append amortized O(1) on ArrayList; occasional O(n) resize.", "LinkedList add/remove at a known node is O(1); finding the index is O(n).", "Prefer ArrayDeque over LinkedList for queues."],
 ["LinkedList is always faster for insert — index search dominates.", "ArrayList append is always O(1) — resize is O(n) occasionally."],
 """flowchart LR
  idx[Index access] --> arr[ArrayList O1]
  idx --> link[LinkedList On]
""",
 "Order history UI pages by index — ArrayList. A queue of pending payments — ArrayDeque, not LinkedList.",
 [("Index-heavy", "ArrayList"), ("True deque", "ArrayDeque"), ("Frequent mid-list edits by iterator", "Rare; still measure")],
 ["Contrast get(i).", "Mention resize amortization.", "Reject LinkedList as default queue."],
 "ArrayList for index; avoid LinkedList unless you hold the node.",
 "**AL** — Array for index, Link for node."),
("03-set-implementations.md", "3", "Set implementations",
 "Set forbids duplicates by equals; HashSet, LinkedHashSet, and TreeSet differ in order and cost.",
 ["HashSet: average O(1), no order.", "LinkedHashSet: insertion order.", "TreeSet: sorted, O(log n), needs Comparable or Comparator.", "Mutable elements that change hashCode corrupt the set."],
 ["TreeSet without a total order throws or mis-orders."],
 """flowchart TD
  uniq[Unique elements] --> hash[HashSet]
  uniq --> ins[LinkedHashSet order]
  uniq --> sort[TreeSet sorted]
""",
 "Dedupe SKUs in an order import: HashSet. Audit trail of first-seen SKUs: LinkedHashSet.",
 [("No order needed", "HashSet"), ("Insertion order", "LinkedHashSet"), ("Sorted range", "TreeSet")],
 ["Uniqueness via equals/hashCode.", "Name ordering.", "Warn on mutable keys."],
 "Hash unordered, linked insertion, tree sorted.",
 "**HLT** — Hash, Linked, Tree."),
("04-map-fundamentals-and-hashmap.md", "4", "Map and HashMap",
 "Map stores key-value pairs; HashMap uses hashing for average O(1) get/put and allows one null key.",
 ["equals and hashCode contract on keys.", "Load factor and resize.", "Not thread-safe.", "null key allowed; ConcurrentHashMap forbids nulls."],
 ["Using a mutable key after put.", "Assuming HashMap iteration order."],
 """flowchart LR
  key[Key] --> hash[hashCode spread]
  hash --> bucket[Bucket index]
  bucket --> eq[equals walk]
""",
 "Lookup Employee by id in a request-scoped cache: HashMap if single-threaded; ConcurrentHashMap if shared.",
 [("Single thread cache", "HashMap"), ("Shared counters", "ConcurrentHashMap"), ("Sorted keys", "TreeMap")],
 ["Hash then equals.", "Null key policy.", "Not safe for concurrent writers."],
 "HashMap is hashed buckets; contract on keys; not concurrent.",
 "**HEB** — Hash, Equals, Bucket."),
("05-hashmap-linkedhashmap-treemap.md", "5", "HashMap, LinkedHashMap, TreeMap",
 "These maps trade order and cost: hash speed, insertion/access order, or sorted keys.",
 ["LinkedHashMap accessOrder=true enables LRU.", "TreeMap navigable ranges.", "HashMap fastest average lookups.", "TreeMap forbids null keys."],
 ["Expecting HashMap to stay sorted."],
 """flowchart TD
  m{Order?}
  m -->|none| h[HashMap]
  m -->|insertion or access| l[LinkedHashMap]
  m -->|sorted| t[TreeMap]
""",
 "LRU of recent Order ids: LinkedHashMap with access order and removeEldestEntry.",
 [("Plain cache", "HashMap"), ("LRU", "LinkedHashMap"), ("Range query on keys", "TreeMap")],
 ["State the order guarantee.", "LRU flag.", "log n vs amortized O(1)."],
 "Hash speed, linked order, tree sort.",
 "**HLT maps**."),
("06-comparable-and-comparator.md", "6", "Comparable and Comparator",
 "Comparable is the type's natural order; Comparator is an external order for a specific collection or sort.",
 ["TreeSet/TreeMap need a consistent order with equals for Set semantics.", "Comparator.comparing for streams and sorts.", "Inconsistent compareTo vs equals breaks SortedSet.", "Multiple comparators for different UI sorts."],
 ["compareTo returning 0 for unequal objects in a TreeSet drops entries."],
 """flowchart LR
  type[Type natural order] --> comp[Comparable]
  external[One-off sort] --> cmp[Comparator]
""",
 "Sort payments by amount for a report without changing Payment's natural id order — use Comparator.",
 [("Natural order in TreeSet", "Comparable"), ("Report sort", "Comparator"), ("Both", "Keep equals aligned with compareTo if used as set")],
 ["Natural vs external.", "Consistency with equals.", "Example: amount vs id."],
 "Comparable lives on the type; Comparator is external.",
 "**NC** — Natural Comparable, Custom Comparator."),
("07-iterators-and-modification.md", "7", "Iterators and modification",
 "Fail-fast iterators track structural modification and throw ConcurrentModificationException if the collection changes during iteration except via the iterator.",
 ["modCount increments on structural change.", "iterator.remove() is safe.", "Fail-fast is best-effort, not a concurrency guarantee.", "Concurrent collections use weakly consistent iterators."],
 ["CME means the map is thread-safe — it does not."],
 """flowchart TD
  it[Iterator] --> check{modCount changed?}
  check -->|yes| cme[ConcurrentModificationException]
  check -->|no| next[next element]
""",
 "Removing unpaid orders while looping a list: use iterator.remove or removeIf, not list.remove inside for-each.",
 [("Single thread filter", "removeIf"), ("Need iterator", "iterator.remove"), ("Concurrent map", "CHM, no CME contract")],
 ["modCount idea.", "Safe removal API.", "CME is not a lock."],
 "Don't structurally modify during fail-fast iteration except via the iterator.",
 "**MOD** — Modify only via iterator or removeIf."),
("08-queue-and-deque.md", "8", "Queue and Deque",
 "Queue is FIFO (or priority); Deque supports both ends. ArrayDeque is the usual non-thread-safe deque.",
 ["Offer/poll vs add/remove exception policy.", "ArrayDeque no nulls, faster than LinkedList.", "Do not use Stack class; use Deque.", "PriorityQueue is not FIFO."],
 ["LinkedList as the default queue."],
 """flowchart LR
  tail[offer tail] --> q[Deque]
  q --> head[poll head]
""",
 "Undo stack of order edits: ArrayDeque as stack (push/pop).",
 [("FIFO in one thread", "ArrayDeque"), ("Blocking producers", "BlockingQueue"), ("Priority", "PriorityQueue")],
 ["Ends of a deque.", "ArrayDeque over LinkedList.", "Exception vs null poll."],
 "ArrayDeque for stack and queue in one thread.",
 "**DEQ** — Double-ended queue."),
("09-priorityqueue-and-heaps.md", "9", "PriorityQueue and heaps",
 "PriorityQueue is a binary heap: peek/poll the extreme by comparator, not sorted iteration.",
 ["Offer/poll O(log n).", "No stable full sort until you drain.", "Top-K largest uses a size-K min-heap.", "Not thread-safe."],
 ["Iterating a heap yields sorted order — it does not."],
 """flowchart TD
  stream[Candidates] --> heap[Size K min-heap]
  heap --> top[K largest remain]
""",
 "Top 10 orders by amount in a stream: min-heap of size 10, evict smaller roots.",
 [("Top-K", "Bounded heap"), ("Full sort", "List sort or TreeSet"), ("Thread-safe priority", "PriorityBlockingQueue")],
 ["Heap property.", "Top-K min-heap trick.", "Iteration is not sorted."],
 "Heap gives the extreme fast; bound the size for Top-K.",
 "**TOPK** — Tiny min-heap keeps the biggest K."),
("10-blocking-queues-and-backpressure.md", "10", "Blocking queues and backpressure",
 "BlockingQueue blocks producers when full and consumers when empty — capacity is backpressure.",
 ["put/take vs offer/poll with timeout.", "ArrayBlockingQueue is bounded.", "Unbounded queue hides overload.", "Capacity is not consumer parallelism."],
 ["Unbounded LinkedBlockingQueue under spike — latency explodes."],
 """flowchart LR
  p[Producer put] --> full{full?}
  full -->|yes| block[Block backpressure]
  full -->|no| slot[Enqueue]
""",
 "Payment webhook workers: bounded ArrayBlockingQueue plus a fixed pool; reject or caller-runs when saturated.",
 [("Need bound", "ArrayBlockingQueue"), ("Handoff", "SynchronousQueue"), ("Priority plus block", "PriorityBlockingQueue")],
 ["Full queue blocks producer.", "Separate consumer count.", "Timeouts for shutdown."],
 "Bounded blocking queue is in-process backpressure.",
 "**PUT** — Producers unblock when consumers take."),
("11-linkedhashmap-lru-cache.md", "11", "LinkedHashMap LRU",
 "LinkedHashMap with accessOrder and removeEldestEntry implements a simple LRU cache.",
 ["Constructor accessOrder true.", "removeEldestEntry when size exceeds cap.", "Not thread-safe — wrap or use Caffeine for prod.", "Equals/hashCode of keys still apply."],
 ["Access-order map without a size cap is not an LRU cache."],
 """flowchart TD
  get[get promotes] --> eldest{size over cap?}
  eldest -->|yes| evict[removeEldestEntry]
""",
 "Cache last 1000 Order summaries per node: LinkedHashMap LRU; for multi-thread use a concurrent cache.",
 [("Single-thread LRU", "LinkedHashMap"), ("Concurrent prod cache", "Caffeine or CHM plus policy"), ("Sorted eviction", "Not LinkedHashMap")],
 ["accessOrder flag.", "Evict eldest.", "Not concurrent by itself."],
 "Access-order LinkedHashMap plus eldest removal is a teaching LRU.",
 "**LRU** — Least Recently Used eldest."),
("12-concurrent-collections-overview.md", "12", "Concurrent collections overview",
 "java.util.concurrent collections allow concurrent access with specific atomicity — not multi-key transactions.",
 ["CHM merge and computeIfAbsent are single-key atomic.", "containsKey plus put races.", "Weakly consistent iterators.", "CopyOnWrite for rare writes."],
 ["CHM makes every business workflow atomic."],
 """flowchart TD
  race[containsKey then put] --> bad[Lost update]
  merge[merge or computeIfAbsent] --> ok[Single key atomic]
""",
 "Count payments per status: CHM.merge(status, 1L, Long::sum), not get-plus-put.",
 [("Single-key update", "CHM atomic method"), ("Multi-key transfer", "Lock or DB transaction"), ("Snapshot reads", "Accept weak consistency or copy")],
 ["Name the race.", "Name the atomic API.", "Limit of single-key."],
 "Concurrent collections give specific atomic ops, not full transactions.",
 "**PCM** — putIfAbsent, compute, merge."),
("13-selecting-the-right-collection.md", "13", "Selecting a collection",
 "Selection is requirements first: uniqueness, order, concurrency, bounds, then the concrete class.",
 ["State access pattern before the class name.", "Thread-safety is a requirement, not a default.", "Bounds and eviction for caches.", "Don't default to LinkedList or Hashtable."],
 ["Picking ConcurrentHashMap for a local method variable."],
 """flowchart TD
  q1{Shared mutable?}
  q1 -->|no| local[HashMap or ArrayList]
  q1 -->|yes| q2{Single key atomic?}
  q2 -->|yes| chm[ConcurrentHashMap]
  q2 -->|no| lock[Lock or DB]
""",
 "Fraud rules need sorted ranges of amounts: TreeMap. Hot request cache: bounded concurrent cache, not an unbounded HashMap.",
 [("Local list", "ArrayList"), ("Shared map", "CHM"), ("Bounded queue", "ArrayBlockingQueue")],
 ["Requirements sentence.", "Then class.", "Name what you rejected."],
 "Requirements, then interface, then implementation.",
 "**RAT** — Requirements, Access, Threads."),
]
for row in COLS:
    add("module-04-collections", *row)

# M3
for row in [
("01-internal-table-and-hash-indexing.md", "1", "Hash indexing",
 "HashMap spreads hashCode and masks with table length minus one to pick a bucket.",
 ["index = (n - 1) & spread.", "spread mixes high bits of hashCode.", "Capacity is power of two.", "Poor hashCode clusters buckets."],
 ["Using raw hashCode as the index."],
 """flowchart LR
  h[hashCode] --> mix[spread]
  mix --> mask["and length-1"]
  mask --> b[bucket]
""",
 "Employee ids that differ only in high bits still need spread so small tables do not collide.",
 [("Need bucket", "Explain spread and mask"), ("Need collision story", "equals walk")],
 ["Write the index formula.", "Why XOR shift.", "Power-of-two mask."],
 "Spread then mask into a power-of-two table.",
 "**SIM** — Spread, Index, Mask."),
("02-put-get-flow-and-treeify.md", "2", "Put, get, treeify",
 "put hashes to a bin, walks equals, inserts or replaces; long chains treeify under JDK thresholds.",
 ["Treeify when chain is long and table is large enough (bin count and capacity thresholds).", "get uses same hash then equals.", "Existing key replaces value, size unchanged.", "Trees revert to lists when small (untreeify)."],
 ["Every bucket becomes a tree at length 8 regardless of capacity."],
 """flowchart TD
  put[put] --> bin[Find bin]
  bin --> found{equals key?}
  found -->|yes| repl[Replace value]
  found -->|no| ins[Insert]
  ins --> tree{chain too long?}
  tree -->|yes| t[Treeify]
""",
 "Duplicate order id put replaces the previous Order value; size stays the same.",
 [("New key", "Insert, maybe resize"), ("Same key", "Replace value")],
 ["Walk equals.", "Replace vs insert.", "Treeify conditions."],
 "Hash, then equals; treeify is conditional.",
 "**GET** — Go to bin, Equals, Tree if needed."),
("03-resize-load-factor-and-threshold.md", "3", "Resize and load factor",
 "Threshold is capacity times load factor; exceeding it doubles the table and rehashes entries.",
 ["Default load factor 0.75.", "Size is mappings, not occupied buckets.", "Resize is O(n) occasionally.", "Pre-size when you know cardinality."],
 ["Threshold equals number of non-empty buckets."],
 """flowchart TD
  add[size exceeds threshold] --> dbl[Double capacity]
  dbl --> re[Rehash bins]
""",
 "Bulk-loading 1e6 employees: new HashMap<>(expected) to avoid repeated resizes.",
 [("Known size", "Presize"), ("Unknown", "Default 0.75")],
 ["Define threshold.", "Double and rehash.", "Presize for bulk."],
 "Resize when size passes capacity times load factor.",
 "**075** — three quarters full, grow."),
("04-thread-safety-and-concurrent-patterns.md", "4", "HashMap thread safety",
 "HashMap is not safe for concurrent structural updates; ConcurrentHashMap provides single-key atomic operations.",
 ["Concurrent put can corrupt or lose updates.", "merge for counters.", "CHM is not a multi-key transaction.", "LongAdder for hot counters."],
 ["Synchronizing only the get."],
 """flowchart TD
  two[Two threads put] --> bad[HashMap race]
  chm[CHM merge] --> ok[Single key safe]
""",
 "Two requests increment an order status count with get/put — lost update. Use merge.",
 [("Local map", "HashMap"), ("Shared counters", "CHM or LongAdder")],
 ["Name the race.", "Name merge.", "Multi-key still needs a transaction."],
 "Do not share HashMap mutably; use CHM atomic single-key ops.",
 "**CHM** — Concurrent, one key, merge."),
]:
    add("module-03-hashmap-internals", *row)

# M2 M5 M6 M7 M9 — compact
MORE = [
("module-02-equals-and-hashcode", "01-equals-and-hashcode-contracts.md", "1", "equals and hashCode",
 "equals must be an equivalence relation; equal objects must share hashCode.",
 ["Reflexive, symmetric, transitive, consistent.", "Equal objects → same hashCode; not the reverse.", "Override both or neither.", "Use the same fields in both."],
 ["Unequal objects must have different hash codes — false."],
 """flowchart TD
  eq[equals true] --> hc[hashCode must match]
""",
 "Two Payment records with the same id compare equal and land in the same HashMap bucket.",
 [("Value object", "equals and hashCode on business key"), ("Entity identity", "id only, document it")],
 ["Contract in one sentence.", "Hash consequence.", "Fields included."],
 "Equality contract plus matching hashCode.",
 "**ESH** — Equals, Symmetric, Hash."),
("module-02-equals-and-hashcode", "02-inheritance-records-and-equality.md", "2", "Inheritance and records",
 "Equality across inheritance is fragile; records generate equals and hashCode from components.",
 ["Subclass adding fields breaks symmetry if superclass equals is used.", "Prefer composition.", "Records are shallow equals on components.", "Don't mix getClass and instanceof casually."],
 ["instanceof equals in a parent and child both ways."],
 """flowchart TD
  parent[Parent equals] --> child[Child extra field]
  child --> break[Symmetry breaks]
""",
 "Order subclass ExpressOrder with extra fee: don't use Order.equals that ignores fee if both types share a set.",
 [("Need subclass", "Composition or sealed types with care"), ("DTO", "record")],
 ["Show symmetry break.", "Recommend composition.", "Records are component equality."],
 "Inheritance plus equals is a trap; records fit simple values.",
 "**SYM** — Symmetry first."),
("module-05-generics", "01-generic-classes-and-methods.md", "1", "Generic classes and methods",
 "Generics parameterize types so the compiler checks element types before erasure.",
 ["class Box<T>, methods <T> T id(T x).", "Avoid raw types.", "Prefer generic methods when only the method needs T.", "Diamond operator infers."],
 ["Raw List stores anything and fails later at cast."],
 """flowchart LR
  src[List of Order] --> compiler[Compiler checks]
  compiler --> ok[No heap pollution]
""",
 "Repository method List<Order> findByEmployee — callers cannot add a Payment without a compile error.",
 [("API returns entities", "Generic type"), ("Legacy interop", "Isolate raw types at the edge")],
 ["Declare T.", "Show a compile error you want.", "No raw types."],
 "Generics move type errors to compile time.",
 "**GEN** — Generic, Early, No raw."),
("module-05-generics", "02-bounded-type-parameters-and-inference.md", "2", "Bounds and inference",
 "Bounds limit T (extends); inference picks type arguments from usage.",
 ["<T extends Comparable<T>> for natural order.", "Multiple bounds with &.", "Target type inference on assignment.", "Explicit type witness when inference fails."],
 ["extends means inheritance only — it also allows interfaces."],
 """flowchart TD
  t[T extends Number] --> call[sum numbers]
""",
 "Utility max of employee salaries uses <T extends Comparable<? super T>> style bounds.",
 [("Need a capability", "Bound T"), ("Inference fails", "Type witness")],
 ["Write a bound.", "Say why.", "Mention inference."],
 "Bounds express required methods on T.",
 "**EXT** — extends bound."),
("module-05-generics", "03-wildcards-pecs.md", "3", "Wildcards and PECS",
 "PECS: producer extends, consumer super — wildcards for flexible method parameters.",
 ["List<? extends Order> read-only producer.", "List<? super Order> can accept Order.", "Do not use wildcard as a return type casually.", "Invariant generics: List<Order> is not List<Object>."],
 ["List<Order> passed where List<Object> is required."],
 """flowchart LR
  prod["? extends T read"] --> get[get T]
  cons["? super T write"] --> add[add T]
""",
 "Copy orders into a list of Object: destination is List<? super Order>.",
 [("Read from source", "? extends"), ("Write into dest", "? super")],
 ["Say PECS.", "Give copy example.", "Invariance."],
 "Producer extends, consumer super.",
 "**PECS**."),
("module-05-generics", "04-type-erasure-raw-types-arrays.md", "4", "Erasure and arrays",
 "Generics erase to bounds at runtime; you cannot make a generic array of T directly.",
 ["No new T[n].", "Heap pollution via raw types and unchecked casts.", "instanceof List is not instanceof List<Order> at runtime.", "Prefer lists over generic arrays."],
 ["Reified T at runtime."],
 """flowchart TD
  compile[List of Order] --> erase[Erased to List]
""",
 "A reflective cache cannot new Order[n] from T; use ArrayList<Order> or Array.newInstance with a Class token.",
 [("Need runtime class", "Class<T> token"), ("Storage", "ArrayList")],
 ["What erasure removes.", "Why arrays clash.", "Class token."],
 "Erasure removes type arguments; arrays are reified.",
 "**ERA** — Erasure, Runtime arrays differ."),
("module-06-java-8-streams", "01-stream-pipeline-fundamentals.md", "1", "Stream pipelines",
 "Streams are lazy pipelines: intermediate ops build a recipe; a terminal op runs it.",
 ["filter/map/flatMap intermediate.", "collect/forEach/reduce terminal.", "Source is not mutated by map.", "One terminal per stream."],
 ["Stream runs at map time — it doesn't."],
 """flowchart LR
  src[Source] --> inter[Intermediate lazy]
  inter --> term[Terminal runs]
""",
 "Filter unpaid orders then map to ids — nothing runs until collect.",
 [("Transform", "map"), ("Flatten lists", "flatMap"), ("Need a list", "collect")],
 ["Lazy vs terminal.", "One pipeline.", "Don't reuse a consumed stream."],
 "Intermediate lazy, terminal executes.",
 "**LIT** — Lazy intermediate, Terminal."),
("module-06-java-8-streams", "02-aggregation-collectors.md", "2", "Collectors",
 "Collectors accumulate stream elements into lists, maps, groups, and summaries.",
 ["toList, groupingBy, partitioningBy.", "Downstream collectors (counting, summing).", "toMap needs a merge function on key clash.", "groupingBy is not thread-safe unless concurrent collector."],
 ["toMap without merge on duplicate keys."],
 """flowchart TD
  orders[Orders] --> grp[groupingBy department]
  grp --> map[Map of lists]
""",
 "Group orders by employee id for a payroll report: groupingBy(Order::employeeId).",
 [("List", "toList"), ("Group", "groupingBy"), ("Duplicate keys", "toMap merge")],
 ["Name the collector.", "Duplicate key policy.", "Downstream if needed."],
 "Collectors are the terminal accumulation strategy.",
 "**GRP** — Group, Reduce, Partition."),
("module-06-java-8-streams", "03-search-short-circuit-primitives.md", "3", "Search and primitives",
 "Short-circuit ops stop early; primitive streams avoid boxing on numeric pipelines.",
 ["findFirst, anyMatch, limit short-circuit.", "IntStream for primitive math.", "Boxing in mapToObj costs.", "Order of filter before map can cut work."],
 ["anyMatch scans everything always — not if it finds a match."],
 """flowchart LR
  f[filter] --> a[anyMatch stops]
""",
 "Stop when any payment is UNKNOWN: anyMatch on status.",
 [("Exists?", "anyMatch"), ("First match", "findFirst"), ("Sum of ints", "mapToInt.sum")],
 ["Short-circuit.", "Primitive stream.", "Filter early."],
 "Short-circuit saves work; primitives avoid boxing.",
 "**SHORT**."),
("module-06-java-8-streams", "04-correctness-parallel-performance.md", "4", "Parallel streams",
 "parallel() uses the common ForkJoinPool and requires stateless, non-interfering ops.",
 ["Don't block in parallel streams.", "Shared mutable ArrayList in forEach is wrong.", "Small data can be slower in parallel.", "Order is not free (forEachOrdered)."],
 ["parallel() always faster."],
 """flowchart TD
  par[parallel stream] --> fjp[Common pool]
  fjp --> block[Blocking IO starves pool]
""",
 "Pricing 50 orders with a blocking HTTP call inside parallel map saturates the common pool.",
 [("CPU split of large array", "parallel with care"), ("Blocking IO", "Virtual threads or own pool")],
 ["Which pool.", "No shared mutation.", "Measure."],
 "Parallel streams share the common pool; keep work CPU-bound and stateless.",
 "**FORK** — ForkJoin common pool."),
("module-07-optional", "01-optional-fundamentals.md", "1", "Optional fundamentals",
 "Optional is a return type for a value that may be absent — not a field or parameter default.",
 ["orElse vs orElseGet (eager vs lazy).", "Do not call get() without presence check.", "orElseThrow for required values.", "Empty means absent, not null inside."],
 ["Optional as a field in JPA entities."],
 """flowchart TD
  repo[find order] --> opt{present?}
  opt -->|yes| map[map]
  opt -->|no| empty[orElse default]
""",
 "Order lookup by id returns Optional; controller uses orElseThrow for 404.",
 [("Default cheap", "orElse"), ("Default expensive", "orElseGet"), ("Must exist", "orElseThrow")],
 ["Return type only.", "orElse vs orElseGet.", "No get()."],
 "Optional for absence at API boundaries.",
 "**OPT** — OrElse, Presence, Throw."),
("module-07-optional", "02-optional-composition-and-antipatterns.md", "2", "Optional composition",
 "map and flatMap chain Optional without nested null checks.",
 ["map when function returns a value.", "flatMap when function returns Optional.", "Don't use Optional.get in streams.", "filter on Optional for conditional presence."],
 ["optional.map(x -> optionalOf(x)) nests — use flatMap."],
 """flowchart LR
  o[Optional order] --> fm[flatMap customer]
  fm --> m[map name]
""",
 "Order to optional customer to email: flatMap then map, never get() in the middle.",
 [("Function returns T", "map"), ("Function returns Optional", "flatMap")],
 ["map vs flatMap.", "One chain.", "Avoid get."],
 "flatMap flattens nested Optional.",
 "**FLAT**."),
]
for row in MORE:
    add(*row)

JVM = [
("01-jvm-architecture-and-execution-lifecycle.md", "1", "JVM architecture",
 "The JVM loads bytecode, verifies, interprets or JIT-compiles, and runs threads on the host OS.",
 ["Class loaders, bytecode, JIT.", "java vs javac.", "Shutdown hooks are last resort.", "Platform threads map toward OS threads."],
 ["JIT means every method is native immediately."],
 """flowchart LR
  src[Bytecode] --> load[Class load]
  load --> exec[Interpret or JIT]
""",
 "A payment service cold start is slow until JIT warms hot methods.",
 [("Startup", "Class loading"), ("Steady state", "JIT")],
 ["Load then execute.", "JIT warms up.", "Not the same as OS."],
 "JVM loads and executes bytecode, optimizing hot paths.",
 "**JIT**."),
("02-jvm-runtime-memory-areas.md", "2", "Runtime memory areas",
 "Heap holds objects; stacks hold frames; metaspace holds class metadata.",
 ["Heap shared; stacks per thread.", "Metaspace is native, not the old perm gen.", "GC manages heap.", "Thread stacks size is configurable."],
 ["All memory is heap."],
 """flowchart TB
  heap[Heap objects]
  stack[Thread stacks]
  meta[Metaspace classes]
""",
 "Many virtual threads with deep stacks still use memory; large ThreadLocals sit on the heap.",
 [("Object leak", "Heap"), ("Class leak", "Metaspace")],
 ["Name three areas.", "What GC collects.", "Per-thread stack."],
 "Heap, stacks, metaspace — different leaks.",
 "**HSM** — Heap, Stack, Metaspace."),
("03-jvm-memory-configuration-and-options.md", "3", "JVM memory options",
 "Flags set heap, metaspace, and GC behavior; defaults differ by ergonomics.",
 ["-Xms/-Xmx heap.", "MetaspaceSize.", "Always set Xmx in containers.", "Container awareness matters."],
 ["Unlimited heap inside a small container."],
 """flowchart LR
  flag["-Xmx"] --> heap[Max heap]
  cgroup[Container limit] --> oom[Kill if over]
""",
 "Pod with 512Mi and -Xmx2g is killed by the cgroup, not a clean Java OOM.",
 [("Container", "Size heap under limit"), ("Batch", "Larger heap, measure GC")],
 ["Name Xmx.", "Container interaction.", "Don't guess."],
 "Set heap inside the container budget.",
 "**XMX**."),
("04-garbage-collection-fundamentals.md", "4", "GC fundamentals",
 "GC reclaims unreachable objects; pauses and throughput trade off.",
 ["Reachability from GC roots.", "Minor vs major collections depend on collector.", "Allocation rate drives GC.", "Finalizers are obsolete."],
 ["GC runs only when heap is 100% — it runs by policy."],
 """flowchart TD
  alloc[Allocate] --> unreachable[Unreachable]
  unreachable --> reclaim[GC reclaims]
""",
 "Caching every Order forever removes reachability — GC cannot help; bound the cache.",
 [("High alloc", "Reduce garbage"), ("Long pause", "Collector and heap tuning")],
 ["Roots and reachability.", "Bound caches.", "Pause vs throughput."],
 "Unreachable objects are collected; leaks stay reachable.",
 "**ROOT**."),
("05-garbage-collectors-and-g1.md", "5", "Collectors and G1",
 "G1 is a regional collector aimed at pause goals; other collectors optimize throughput or latency differently.",
 ["G1 uses regions and a pause target.", "Know your JDK default.", "Don't tune blindly.", "ZGC/Shenandoah are low-pause options on newer JDKs."],
 ["One collector is best for every service."],
 """flowchart LR
  regions[G1 regions] --> evac[Evacuate]
  evac --> pause[Pause goal]
""",
 "Latency-sensitive payment API: measure p99 pause; consider G1 pause target or a low-latency collector if the JDK supports it.",
 [("Throughput batch", "Measure, maybe throughput collector"), ("Tight p99", "Low-pause collector")],
 ["Name G1 idea.", "Measure first.", "JDK version matters."],
 "Pick a collector from pause and throughput goals, then measure.",
 "**G1** — regions and pause goals."),
("06-java-reference-types-and-memory-retention.md", "6", "Reference types",
 "Strong refs keep objects; soft, weak, and phantom refs allow earlier collection or post-mortem cleanup.",
 ["Strong is the default.", "WeakHashMap drops entries when keys are weakly reachable.", "Soft refs are cache-ish but not a size cap.", "Don't build caches only from soft refs."],
 ["WeakHashMap as an LRU."],
 """flowchart TD
  strong[Strong ref] --> live[Stays]
  weak[Weak ref] --> gone[Collectable]
""",
 "A metadata cache keyed by Class should not pin class loaders; weak keys can help, but still cap size.",
 [("Must stay", "Strong"), ("Optional cache", "Bounded strong cache, not only soft")],
 ["Four reference strengths briefly.", "WeakHashMap caveat.", "Prefer explicit eviction."],
 "Strong refs retain; weak refs do not replace a capacity policy.",
 "**SWE** — Strong, Weak, Evict explicitly."),
("07-diagnosing-outofmemoryerror-in-production.md", "7", "Diagnosing OOM",
 "OutOfMemoryError names the area: heap, metaspace, or unable to create thread.",
 ["Read the message subtype.", "Heap dump on heap OOM if policy allows.", "Thread OOM is often native memory or thread count.", "Correlate deploy and traffic."],
 ["Every OOM is heap."],
 """flowchart TD
  oom[OOM] --> kind{Message}
  kind -->|Java heap| dump[Heap dump]
  kind -->|Metaspace| cls[Class loaders]
  kind -->|thread| native[Native stacks]
""",
 "After a deploy, metaspace OOM points at classloader leaks, not a bigger order cache.",
 [("Java heap space", "Dump and dominators"), ("Metaspace", "Class loaders"), ("Unable to create native thread", "Thread count")],
 ["Read the subtype.", "Pick the tool.", "Don't just raise Xmx."],
 "The OOM message selects the investigation.",
 "**MSG** — Message guides the tool."),
("08-heap-dump-analysis.md", "8", "Heap dump analysis",
 "A heap dump shows retained sets and dominators — who keeps objects alive.",
 ["Capture with jcmd or on OOM.", "Look at dominator tree.", "Shallow vs retained size.", "Redact secrets in dumps."],
 ["Largest shallow object is always the leak."],
 """flowchart TD
  dump[Heap dump] --> dom[Dominators]
  dom --> fix[Drop the retainer]
""",
 "Order cache map dominates the heap after a bug removed eviction.",
 [("Leak", "Dominator path"), ("One-off spike", "Compare two dumps")],
 ["Retained size.", "Dominator.", "Fix the retainer."],
 "Follow dominators to the retainer.",
 "**DOM**."),
("09-production-oom-case-study-spark-sql-optimizer.md", "9", "OOM case study",
 "Large query plans can exhaust memory during optimization — a production pattern of unbounded in-memory structures.",
 ["Symptom, evidence, cause, fix.", "Bound plan complexity or memory.", "Don't only raise heap.", "Separate this story from generic leaks."],
 ["The only fix is a bigger cluster."],
 """flowchart LR
  query[Huge SQL] --> opt[Optimizer structures]
  opt --> oom[Heap OOM]
""",
 "A generated query with huge IN lists builds a giant plan; bound inputs and simplify SQL.",
 [("Unbounded structure", "Cap input"), ("Need capacity", "Size after the cap")],
 ["Tell symptom then cause.", "Bound the input.", "Heap increase is secondary."],
 "OOM case studies need a retainer and a bound.",
 "**CAP** — Cap the input."),
]
for row in JVM:
    add("module-09-jvm-basics", *row)

def main():
    for lesson in LESSONS:
        mod, fname = lesson[0], lesson[1]
        text = page(*lesson)
        path = ROOT / mod / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(path.relative_to(ROOT))
    print("wrote", len(LESSONS))

if __name__ == "__main__":
    main()
