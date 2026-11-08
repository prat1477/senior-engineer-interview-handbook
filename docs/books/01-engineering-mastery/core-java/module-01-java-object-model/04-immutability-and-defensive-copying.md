---
title: "Lesson 4 — Immutability and Defensive Copying"
description: Immutable class design, shallow versus deep copy, List.copyOf, and safe publication limits.
status: covered
audience: practitioner
tags: [java, immutability, defensive-copy, module-1, lesson-4]
created: 2026-11-07
updated: 2026-11-07
---

# Lesson 4 — Immutability and Defensive Copying

## Overview

An immutable object does not change its observable state after construction finishes. Callers may share it. They may not alter what other callers already observed. Immutability supports encapsulation and removes a class of races. It does not, by itself, coordinate updates to a shared variable that points at the object.

## A. Mutable versus immutable

A mutable `Employee` can change name, id, or roles after other services have stored the reference. An immutable `Employee` returns a new object when a role is added. The original reference still denotes the original employee.

Benefits in a backend service:

- A downstream component cannot silently change what an upstream component validated.
- Equality and hash-based keys stay stable if equality depends on that state.
- Readers do not need locks to protect the object's fields from concurrent writes, provided the object was safely constructed (section D).

Encapsulation is the mechanism (private state). Immutability is a stronger policy: after the constructor, even the class's own methods do not change that state.

## B. Design practices

These are practices for a type you intend to be immutable. They are not a rule that every immutable type in the JDK is written identically.

1. Make the class `final` when subclasses must not add mutable state or override methods to expose it.
2. Make fields `private final`.
3. Do not provide setters or other methods that mutate fields.
4. Initialize every field in the constructor (or instance initializer) before the constructor completes.
5. Defensively copy mutable constructor arguments.
6. Do not return internal mutable objects from getters.
7. Apply the same rules to nested objects that are part of the observable state. A copied list of mutable elements is only shallowly protected.

A class can be immutable without being `final` if its state is private, its methods are not overridable in a way that mutates or leaks that state, and construction still establishes the invariant. `final` is the straightforward way to close the subclass hole. Prefer it unless you have a reason to allow extension.

## C. Shared PaymentRequest

Suppose one `PaymentRequest` instance is passed to `ValidationService`, `FraudCheckService`, `PaymentProcessor`, and `AuditService`.

If the request is mutable, fraud checking can change the amount after validation has approved a different amount. The processor then charges the mutated amount. Audit logs whichever state it happens to read. The bug is aliasing: four components hold one object, and a write in one is a read surprise in the others.

An immutable request makes that write a compile-time or API problem. A correction is a new request object. Each stage either accepts the original or explicitly receives the replacement. There is no hidden mutation of the validated instance.

## D. Concurrency

A properly constructed immutable object can be shared across threads without synchronization for reads of its state. Threads cannot race on writes to that state because the class does not write it after publication.

For `final` fields, the Java Memory Model guarantees that a thread which sees a reference to an object only after that object's constructor has finished will see the initialized values of those `final` fields. That is the freeze at the end of construction (JLS 17.5). It is why immutable objects rely on `final` fields rather than on “we remember not to change them.”

The guarantee assumes the reference is not published before construction finishes. If the constructor stores `this` in a static field, passes `this` to another method that publishes it, or starts a thread that reads `this`, another thread can observe the object before finals are frozen. That is **`this` escape**. Do not publish `this` from the constructor.

Immutability does not solve every shared-memory problem:

- A non-final field, even if you never change it in practice, does not get the final-field freeze.
- Two threads can still race on a **shared reference variable** (`Employee current`) when they each compute a new employee and assign it back. One assignment can be lost. The objects are immutable; the variable that points at the current one is not. Use an atomic reference, a lock, or a single writer when the authoritative reference must move.
- Immutable objects do not coordinate external effects (two charges, two database rows).

## E. Final reference versus immutable object

```java
private final List<String> roles;
```

`final` stops a later assignment to `roles`. It does not freeze the list. If `roles` is an `ArrayList`, `roles.add("admin")` still mutates the object. The reference is fixed. The object is mutable.

## F. Aliasing and defensive copies

**Leak through the constructor argument.** The caller keeps the list it passed in and adds a role after construction. If the constructor stored that same list, the employee's roles change.

**Leak through the getter.** The constructor copied into a private `ArrayList`, but `getRoles()` returns that list. The caller adds a role on the returned list and mutates the employee.

Aliasing means two references denote one mutable object. Defensive copying breaks the alias:

- In the constructor, copy the input before storing it.
- In the getter, either return an unmodifiable view of an already unmodifiable internal list, or return a fresh mutable copy if the caller is allowed to change its own list.

Copying only one boundary leaves the other open.

## G. Collection copies

| Approach | What the caller can do afterward | Notes |
| --- | --- | --- |
| `new ArrayList<>(input)` | Mutate the new list; cannot affect a different list | Shallow. New mutable list. Null elements are allowed. Does not copy nested mutable objects |
| `List.copyOf(input)` | Cannot add, remove, or `set` | Unmodifiable list. Rejects a null list and null elements. Shallow. May reuse an existing unmodifiable list instance that already qualifies, so it is not a promise of a new physical copy every time |
| Return the internal unmodifiable list | Cannot mutate the list structure | Safe when elements are immutable |
| Return `new ArrayList<>(internal)` | Mutate only the returned copy | Use when the caller needs a mutable list and must not touch the employee's list |

`List.copyOf` copies the collection structure (the sequence of references). It is not a deep copy. An unmodifiable list of mutable `Address` objects is not a deeply immutable employee.

## H. Shallow copy versus deep copy

`Address` starts mutable. `Employee` copies the list only.

```java
public final class Employee {
    private final List<Address> addresses;

    public Employee(List<Address> addresses) {
        this.addresses = List.copyOf(addresses);
    }

    public List<Address> getAddresses() {
        return addresses;
    }
}
```

```java
Address address = new Address("Pune");
List<Address> addresses = new ArrayList<>();
addresses.add(address);

Employee employee = new Employee(addresses);
address.setCity("Mumbai");

System.out.println(employee.getAddresses().get(0).getCity());
```

Output: `Mumbai`.

`List.copyOf` stored a new unmodifiable list that still points at the same `Address`. `setCity` mutates that shared object. Adding to the original `addresses` list does **not** change the employee, because the list structure was copied. Changing the city does, because the element was not.

Two sound approaches:

1. Make `Address` immutable and share the reference. Shallow copy is then enough, because there is no setter that can change the city.
2. Deep-copy nested mutable objects at the boundary where the employee takes input and at the boundary where it returns them, so callers cannot reach the instances stored inside.

Deep copying is required when the nested objects stay mutable and are part of the state you promised not to share. It is not required when those objects are already immutable. Copying a large graph on every read also costs allocation. Prefer immutable nested types, and deep-copy only at the edges where mutable third-party objects cross into your model.

A deep copy of a graph of nested mutable objects was not implemented in this session.

## I. Immutable Employee

```java
public final class Employee {
    private final String name;
    private final int id;
    private final List<String> roles;

    public Employee(String name, int id, List<String> roles) {
        this.name = name;
        this.id = id;
        this.roles = List.copyOf(roles);
    }

    public String getName() {
        return name;
    }

    public int getId() {
        return id;
    }

    public List<String> getRoles() {
        return roles;
    }
}
```

`getRoles()` may return the internal list because:

- `List.copyOf` produced an unmodifiable list, so `add` / `remove` / `set` throw.
- `String` elements are immutable, so an element cannot be changed in place.
- No mutable internal state is reachable from the returned reference.

Null handling: `List.copyOf` throws `NullPointerException` if `roles` is null or contains a null element. `name` is stored as passed. This constructor does not add a separate null check or blank-name rule. Add those only if the domain invariant requires them. `id` is a primitive, so there is no null `id`.

## J. Immutable updates

This method does not compile. `roles` is `final`, and assigning it would also abandon immutability even if the field were not final, by changing an existing object.

```java
public void addRole(String role) {
    List<String> newRoles = new ArrayList<>(this.roles);
    newRoles.add(role);
    this.roles = newRoles; // illegal: cannot assign a final field
}
```

Return a new employee. The original stays as it was.

```java
public Employee addRole(String role) {
    List<String> newRoles = new ArrayList<>(this.roles);
    newRoles.add(role);
    return new Employee(this.name, this.id, newRoles);
}
```

That is a functional-style update: the operation yields a new value and preserves the original. Callers who should see the new role must use the returned reference.

```java
Employee updated = employee.addRole("oncall");
```

If several threads share one `Employee holder` field and each does `holder = holder.addRole(...)`, the objects are still immutable and the assignments can still lose updates. Immutability removed in-place mutation. It did not make the shared authoritative reference atomic.

## K. Interview revision

**How do you design an immutable class?**  
`final` class when extension is unsafe, `private final` fields, no mutators, full initialization in the constructor, defensive copies of mutable inputs, and getters that do not leak mutable internals.

**Does `final List<String> roles` make the roles immutable?**  
It blocks reassignment of the field. The list object stays mutable unless you store an unmodifiable list and immutable elements.

**What is defensive copying?**  
Copying at the constructor and getter so a caller's list is not the object's list.

**Shallow or deep?**  
Shallow copies the container. Deep copies nested mutable objects. Share nested objects when they are immutable.

**What does `List.copyOf` guarantee?**  
An unmodifiable shallow copy of the element references, with no null list and no null elements. It does not promise a distinct new array on every call, and it does not deep-copy elements.

**Why is the employee above shareable across threads for reads?**  
After construction, its state does not change, and `final` fields are safely visible to threads that only obtain the reference after the constructor finishes, as long as `this` did not escape.

**What does immutability not fix?**  
Lost updates on a shared variable that is assigned a new employee, and coordination of external side effects.

### 30-second revision

- Immutable means observable state is fixed after construction.
- `final` fixes the reference, not the object's contents.
- `List.copyOf` is an unmodifiable shallow copy.
- Share immutable nested objects. Deep-copy mutable ones at the boundary.
- Updates return a new object. The original remains.

### Active recall

1. Why can `getRoles()` return the field in the `Employee` above, while the same return would be unsafe for an internal `ArrayList`?
2. Why does the address example print `Mumbai` even though the list was copied?
3. Why does assigning `this.roles = newRoles` fail, and what should `addRole` return instead?
4. Which JMM guarantee applies to `final` fields, and what constructor mistake voids the practical benefit?
5. Two threads each call `addRole` and write the result to the same field. What can still go wrong?

## See also

- [Module 2 — mutable keys and equality](../module-02-equals-and-hashcode/01-equals-and-hashcode-contracts.md)
- [Interview Companion](../../../02-interview-companion/core-java/module-01-java-object-model/04-immutability-and-defensive-copying.md)
