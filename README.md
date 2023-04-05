# Celery Investigation

![Celery Logo](https://blog.4linux.com.br/wp-content/uploads/2017/07/celery.jpg)

## Goal

The goal with this repo is to investigate, test, and compare different configurations for Celery in order to try to improve performance by reducing the total time spent running a set of tasks.

For this purpose we are assuming the tasks have some characteristics:
   - They are I/O bound: the time it takes to complete a computation is determined mainly by the period it spends waiting for input/output operations;
   - They are long running: they spend a couple minutes running to acomplish their purpose

## Requirements

For running all the components you might need to add the root of this repo to you pythonpath on each shell you use to run a component.

```
$ export PYTHONPATH=$PYTHONPATH:/full/path/to/repo/root
```

It is also recommended to create a python virtual environment and install the dependencies there.

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## Structure

To be able to achieve the tasks characteristics mentioned above and test the different configurations we have implemented the following structure.

### webserver
This is a simple fastapi server with an endpoint that, upon request:
   - Randomly choses a value between 180 and 210 seconds;
   - Sleeps for that amount of seconds;
   - Inserts a record containing the id, the sleep time in seconds and total request time in secods;
   - Returns an http response containing the same data from the previous step;

### utils
This is a package with some utilities such as a small client to request data from the webserver, logging configuration and helper functions.

### waitinator
This is a celery application configured with 2 queues, a producer and the consumer implementations.
The consumer implements 2 different types of tasks:
   - `waitinate`: this task fires up a request to the webserver, parses the response, inserts a record into an sqlite database and returns a dictionary with collected data and measurements;
   - `summarize`: this task expects a list of dictionaries (outputs from `waitinate` tasks) to summarize and insert a record into an sqlite database
The producer submits 2 chords (for most of the tests run):
   - 1 chord containing `7 waitinate` tasks as header tasks and a `summarize` task as the callback task;
   - 1 chord containing `3 waitinate` tasks as header tasks and a `summarize` task as the callback task;

### reporter
This is a package with a python script that loads recorded raw data for cpu and memory usage, parses it, cleans it and outputs a json file with the cleaned data, as well as a graphic representation of the data for each of the monitored PIDs.

## Running

If you intend to run/experiment by yourself, assuming you have rabbitmq and redis installed in your machine, you will need:
   - A shell for running rabbitmq as the broker: in my case, on macos:
   ```
    $ CONF_ENV_FILE="/opt/homebrew/etc/rabbitmq/rabbitmq-env.conf" /opt/homebrew/opt/rabbitmq/sbin/rabbitmq-server
   ```
   - A shell for running redis as the backend result:
   ```
   $ redis-server
   ```
   - A shell for running the webserver/api:
   ```
   $ python webserver/run.py
   ```
   - A shell for running the consumer (with the various configurations):
   ```
   celery -A waitinator.tasks worker --loglevel=info --without-gossip --without-mingle
   ```
   - A shell for running the producer:
   ```
   python waitinator/producer.py
   ```

For running the monitor, in a separate shell:
```
$ syrupy.py --separator=, --no-align -c celery -S >> /your/output/path/raw_data.txt
```

For running the script to parse the data and generate their graphical representation:
```
$ python reporter/report.py --path /your/output/path/raw_data.txt
```

## Tests with Monitoring and Results

The followed "methodology" was to run the consumer with a set of configurations, run the producer, collect the data and store the sqlite databases of that run for analysis.

For the initial tests we ran the base case where we have:
   - worker_prefetch_multiplier set to 1
   - worker_concurrency set to 1
   - worker_pool set to default (prefork)
This constitutes our baseline for further comparison.

The other runs, for which the databases and results are stored under the results folder, tested the following variations:
   - Concurrency: Without changing any other setting, we varied the number of concurrent processes under the worker, using the default prefork pool of processes;
   - Process Pool: Also with the different number of concurrent processes/greenlets we also varied the process pools:
      - gevent
      - eventlet

For monitoring CPU and Memory consumption during the tests we used [syrupy](https://github.com/jeetsukumaran/Syrupy).

<br>

### Procedures

For recording the memory and cpu usage for all celery processes during the tests it was as simple as running `syrupy.py --separator=, --no-align -c celery -S >> /your/path/raw_data.txt`.

With those files in place we used the `reporter/report.py` script to clean the raw data and plot a graphical representation of it.

While the tests were running we also monitored the number of connections to the backend result (redis server) and to the message broker (rabbitmq):
   - Backend Result: we connected to the server using `redis-cli` and periodically ran `info clients`, taking note of the maximum value for simultaneous client connections;
   - Broker: we monitored the maximum number of connections for each test through rabbitmq web interface `http://localhost:15672`, under the connections tab.

<br>

### Results

The total time is being calculated as `MAX(end_timestamp) - MIN(start_timestamp)` for all tasks from both chords, meaning it represents the time for finish running both chords.

#### __Baseline (Prefork)__

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 1947.09 | 1 | 3 |

![PID 94502](results/base/monitoring/plot-94502.png)
![PID 94507](results/base/monitoring/plot-94507.png)

We can see that the CPU usage stayed below 1% most of the time, having a peak of approximately 2% for one of the celery processes.

For the memory (rss) we can see that a total maximum of approximately 100MB was consumed, but most of the time it stayed below 80MB.

#### __Concurrency with Prefork__

##### _Concurrency of 2_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 986.22 | 2 | 4 |

![PID 77464](results/prefork/2/monitoring/plot-77464.png)
![PID 77467](results/prefork/2/monitoring/plot-77467.png)
![PID 77468](results/prefork/2/monitoring/plot-77468.png)

We can see that the CPU usage stayed below 2% most of the time, having a peak of approximately 3.5% for one of the celery processes and 1.6% for another of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 140MB was consumed, but most of the time it stayed below 90MB.

##### _Concurrency of 4_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 586.12 | 4 | 4 |

![PID 83508](results/prefork/4/monitoring/plot-83508.png)
![PID 83516](results/prefork/4/monitoring/plot-83516.png)
![PID 83518](results/prefork/4/monitoring/plot-83518.png)
![PID 83519](results/prefork/4/monitoring/plot-83519.png)
![PID 83520](results/prefork/4/monitoring/plot-83520.png)

We can see that the CPU usage stayed below 2% most of the time, having a peak of approximately 5.5%, 4.5%, 1.7%, 0.8% and 0.1% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 200MB was consumed, but most of the time it stayed below 180MB.

##### _Concurrency of 8_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 392.08 | 8 | 4 |

![PID 89427](results/prefork/8/monitoring/plot-89427.png)
![PID 89432](results/prefork/8/monitoring/plot-89432.png)
![PID 89433](results/prefork/8/monitoring/plot-89433.png)
![PID 89434](results/prefork/8/monitoring/plot-89434.png)
![PID 89435](results/prefork/8/monitoring/plot-89435.png)
![PID 89436](results/prefork/8/monitoring/plot-89436.png)
![PID 89437](results/prefork/8/monitoring/plot-89437.png)
![PID 89438](results/prefork/8/monitoring/plot-89438.png)
![PID 89439](results/prefork/8/monitoring/plot-89439.png)

We can see that the CPU usage stayed below 2% most of the time, having a peak of approximately 3.5%, 1.4%, 1.0%, 0.9%, 0.8%, 0.1% and 0.1% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 265MB was consumed.

##### _Concurrency of 16_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 207.03 | 10 | 4 |

![PID 95744](results/prefork/16/monitoring/plot-95744.png)
![PID 95753](results/prefork/16/monitoring/plot-95753.png)
![PID 95754](results/prefork/16/monitoring/plot-95754.png)
![PID 95756](results/prefork/16/monitoring/plot-95756.png)
![PID 95757](results/prefork/16/monitoring/plot-95757.png)
![PID 95758](results/prefork/16/monitoring/plot-95758.png)
![PID 95759](results/prefork/16/monitoring/plot-95759.png)
![PID 95760](results/prefork/16/monitoring/plot-95760.png)
![PID 95761](results/prefork/16/monitoring/plot-95761.png)
![PID 95762](results/prefork/16/monitoring/plot-95762.png)
![PID 95763](results/prefork/16/monitoring/plot-95763.png)
![PID 95764](results/prefork/16/monitoring/plot-95764.png)
![PID 95765](results/prefork/16/monitoring/plot-95765.png)
![PID 95766](results/prefork/16/monitoring/plot-95766.png)
![PID 95767](results/prefork/16/monitoring/plot-95767.png)
![PID 95768](results/prefork/16/monitoring/plot-95768.png)
![PID 95769](results/prefork/16/monitoring/plot-95769.png)

We can see that the CPU usage stayed below 4% most of the time, having a peak of approximately 3.5%, 1.3%, 1.2%, 1.2%, 1.2%, 0.9%, 0.9%, 0.7%, 0.6% and 0.5% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 325MB was consumed.

##### _Concurrency of 32_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 206.05 | 10 | 4 |

![PID 814](results/prefork/32/monitoring/plot-814.png)
![PID 819](results/prefork/32/monitoring/plot-819.png)
![PID 820](results/prefork/32/monitoring/plot-820.png)
![PID 821](results/prefork/32/monitoring/plot-821.png)
![PID 822](results/prefork/32/monitoring/plot-822.png)
![PID 823](results/prefork/32/monitoring/plot-823.png)
![PID 824](results/prefork/32/monitoring/plot-824.png)
![PID 825](results/prefork/32/monitoring/plot-825.png)
![PID 826](results/prefork/32/monitoring/plot-826.png)
![PID 827](results/prefork/32/monitoring/plot-827.png)
![PID 828](results/prefork/32/monitoring/plot-828.png)
![PID 829](results/prefork/32/monitoring/plot-829.png)
![PID 830](results/prefork/32/monitoring/plot-830.png)
![PID 831](results/prefork/32/monitoring/plot-831.png)
![PID 832](results/prefork/32/monitoring/plot-832.png)
![PID 834](results/prefork/32/monitoring/plot-834.png)
![PID 837](results/prefork/32/monitoring/plot-837.png)
![PID 838](results/prefork/32/monitoring/plot-838.png)
![PID 841](results/prefork/32/monitoring/plot-841.png)
![PID 843](results/prefork/32/monitoring/plot-843.png)
![PID 844](results/prefork/32/monitoring/plot-844.png)
![PID 845](results/prefork/32/monitoring/plot-845.png)
![PID 846](results/prefork/32/monitoring/plot-846.png)
![PID 849](results/prefork/32/monitoring/plot-849.png)
![PID 852](results/prefork/32/monitoring/plot-852.png)
![PID 853](results/prefork/32/monitoring/plot-853.png)
![PID 854](results/prefork/32/monitoring/plot-854.png)
![PID 855](results/prefork/32/monitoring/plot-855.png)
![PID 856](results/prefork/32/monitoring/plot-856.png)
![PID 857](results/prefork/32/monitoring/plot-857.png)
![PID 858](results/prefork/32/monitoring/plot-858.png)
![PID 859](results/prefork/32/monitoring/plot-859.png)
![PID 860](results/prefork/32/monitoring/plot-860.png)

We can see that the CPU usage stayed below 4% most of the time, having a peak of approximately 5.8%, 1.75%, 1.6%, 1.2%, 0.7%, 0.6%, 0.4%, 0.4%, 0.3%, 0.2% and 0.1% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 550MB was consumed.

Overall we can see that using concurrency with prefork spawns multiple celery processes, mainly increasing memory consumption and the number of connections used for the backend result, the connection to the backend is far from exhausting the default limit (1000 for redis) though.

#### __Concurrency with Gevent__

##### _Concurrency of 2_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 990.77 | 4 | 4 |

![PID 60287](results/gevent/2/monitoring/plot-60287.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 2.75%.

For the memory (rss) we can see a maximum of approximately 75MB was consumed, with mainly 5 plateaus of memory consumption being formed during the tests execution at 75MB, 65MB, 40MB and 20MB (twice).

##### _Concurrency of 4_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 597.12 | 4 | 4 |

![PID 54144](results/gevent/4/monitoring/plot-54144.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 4.0%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 4 plateaus of memory consumption being formed during the tests execution at 77.25MB, 60MB, 55MB, and 20MB.

##### _Concurrency of 8_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 385.08 | 6 | 4 |

![PID 63906](results/gevent/8/monitoring/plot-63906.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 3.0%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 8 plateaus of memory consumption being formed during the tests execution at 77.5MB, 60MB, 57.5MB, 40MB, 30MB, 20MB (twice) and 10MB.

##### _Concurrency of 16_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 208.03 | 8 | 4 |

![PID 67673](results/gevent/16/monitoring/plot-67673.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 6.3%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 3 plateaus of memory consumption being formed during the tests execution at 77.5MB, 47.5MB, and 41MB. By the end of the process the memory consumption progressively increases again with another peak coinciding with the CPU peak.

##### _Concurrency of 32_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 206.03 | 8 | 4 |

![PID 72130](results/gevent/32/monitoring/plot-72130.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 6.3%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 5 plateaus of memory consumption being formed during the tests execution at 77.5MB, 75.5MB, 61MB, 60MB and 20MB.

Overall we can see there is a lot of time execution reduction by increasing concurrency with gevent while there is no significant increase in memory or CPU usages. The number of connections to the broker also stayed stable and the number of backend connections has grown sustainably.

#### __Concurrency with Eventlet__

##### _Concurrency of 2_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 951.19 | 5 | 4 |

![PID 60287](results/eventlet/2/monitoring/plot-3211.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 5.5%.

For the memory (rss) we can see a maximum of approximately 78MB was consumed, with mainly 8 plateaus of memory consumption being formed during the tests execution at 78MB, 72MB, 64MB, 44MB (twice) and 20MB (three times).

##### _Concurrency of 4_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 580.11 | 7 | 4 |

![PID 54144](results/eventlet/4/monitoring/plot-8922.png)

We can see that the CPU usage stayed below 1% most having two main peaks of approximately 7.5% and 17.5%.

For the memory (rss) we can see a maximum of approximately 78MB was consumed, with mainly 5 plateaus of memory consumption being formed during the tests execution at 78MB, 73MB, 55MB, 22MB and 20MB.

##### _Concurrency of 8_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 391.06 | 5 | 4 |

![PID 54144](results/eventlet/8/monitoring/plot-14189.png)

We can see that the CPU usage stayed below 1% most having two main peaks of approximately 3.75% and 17.5%.

For the memory (rss) we can see a maximum of approximately 78MB was consumed, with mainly 5 plateaus of memory consumption being formed during the tests execution at 78MB, 75MB, 62MB, 57.5MB, and 25MB.

#### _Concurrency of 16_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 206.02 | 7 | 4 |

![PID 54144](results/eventlet/16/monitoring/plot-97334.png)

We can see that the CPU usage stayed below 1% most having two main peaks of approximately 1.5% and 3.75%.

For the memory (rss) we can see a maximum of approximately 79.75MB was consumed, with mainly 3 plateaus of memory consumption being formed during the tests execution at 79.75MB, 79MB, and 78.6MB.

#### _Concurrency of 32_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 206.03 | 4 | 4 |

![PID 54144](results/eventlet/32/monitoring/plot-19375.png)

We can see that the CPU usage stayed below 1% most having three main peaks of approximately 11%, 9% and 3.5%.

For the memory (rss) we can see a maximum of approximately 81MB was consumed, with mainly 2 plateaus of memory consumption being formed during the tests execution at 81MB, and 79.5MB.

Overall we can see that using concurrency with eventlet also reduces the execution time significantly while not seeing a big impact on memory usage. The CPU usage showed a little bit of instability, having some high peaks if compared to other pools of processes (but still moderate in general). The number of backend and broker connections did not grow significantly when increasing concurrency but there does not seem to be a clear pattern on how they scale.

## Discussion

It looks clear that for long running, I/O bound tasks there is a gain in increasing concurrency for the celery worker, resulting in shorter execution times.

For all different pool types and number of concurrent processes it presented an improvement by reducing the total execution time, with very similar total times taken for the different pools to complete the tasks at the same level of concurrency.

The main difference between the pools was related to resources consumption and connections management.
With that considered, it looks like the best performance was achieved by __gevent__ with a concurrency level of __32__, since it managed to reduce the running time by approximately `89.42%` while keeping a stable CPU/memory consumption and managing the backend and broker connections efficiently.

It is important to notice all the tabled results might be subjected to some fluctuation due to the fact the webserver (and other machine processes) are running in the machine and might vary on CPU/Memory consumption and I/O delays, but the experiment gives as a general idea of the possible improvements we might achieve in production if we are willing to test and find the "sweetspot" of concurrency/pool configuration for our scenario.

### Observations

One possible downside is that, for being able to run celery with gevent and eventlet, I had to:
   - Set `broker_heartbeat = 0`, otherwise some tasks would miss the heartbeat and be re-run, while celery would also log some warning messages;
   - Run celery from the shell, not being able to use the `celery_app.main_worker_main(..)` approach from a python script. When trying to do so the celery
   worker would receive a couple tasks and hang, not running any tasks.
