## Old results

These are the old results of the tests, when using the `sortinator` app to emulate long processing.

### Baseline
![Baseline Table](results/images/baseline.png)

### Concurrent Processes - Average Times
![Average Times Table](results/images/processes_avg_time.png =800x160)

### Concurrent Processes - Total Times
![Total Times Table](results/images/processes_total_time.png =600x150)

The total time is being calculated as `MAX(end_timestamp) - MIN(start_timestamp)` for all tasks from both chords, meaning it represents the time
for finish running both chords.
