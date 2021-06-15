## Reference and Borrowing

### Mutable References

The benefit of having this restriction is that Rust can prevent data races at compile time. A *data race* is similar to a race condition and happens when these three behaviors occur:

- Two or more pointers access the same data at the same time.
- At least one of the pointers is being used to write to the data.
- There’s no mechanism being used to synchronize access to the data.



```
每个变量在同一个范围内只能允许一个可变应用的限制是为了不产生数据竞争，但是如果源变量和可变引用在多线程情况下有可能同时被修改，也会产生数据竞争。
```



- `可变引用` 和 `不可变引用` 不共戴天， 233333!!!



```rust
fn main() {
    let mut s = String::from("hello");

    let r1 = &s; // no problem
    let r2 = &s; // no problem
    println!("{} and {}", r1, r2);
    // r1 and r2 are no longer used after this point

    let r3 = &mut s; // no problem
    println!("{}", r3);
}
```

在不可变引用的范围外可以使用可变引用。



### The Rules of References

Let’s recap what we’ve discussed about references:

- At any given time, you can have *either* one mutable reference *or* any number of immutable references.
- References must always be valid.