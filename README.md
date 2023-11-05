Service which manages drone flight path and communication with the main system.

# First run - local
```poetry install```
```poetry run python mission-manager```

Testing without broker connection:
``` --no-kafka```

With kafka for linux- works on my machine - kafka needs to be installed in a certain directory etc. etc.
```sudo run_locally.sh```

# Tests
To run tests see run_test.sh