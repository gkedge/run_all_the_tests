The

```
├─ src
│
│<-- # run selected __main__'s from this working directory
│
│  └─ __init__.py
│  └─ foo.py
│  ├─ bar
│  │   └─ __init__.py
│  │   └─ bar.py
│  │
│  │<-- # run selected __main__'s from this working directory
│  │
│  └─ run_foo_main.py
│  └─ run_bar_main.py
│
│<-- # run selected test cases from this working directory
│
├─ tests
│  │
│  │<-- # run selected test cases from this working directory
│  │
│  └─ test_foo.py
│  └─ bar
│        │<-- # run selected bar test cases from this working directory
│        │
│        └─ test_bar.py
└─ setup.py
```
