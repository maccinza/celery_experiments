[<< Voltar](../README.md)

## Tests with Monitoring

For monitoring CPU and Memory consumption during the tests we used [syrupy](https://github.com/jeetsukumaran/Syrupy).

### Procedures

For recording the memory and cpu usage for all celery processes during the tests it was as simple as running `syrupy.py --separator=, --no-align -c celery -S >> /your/path/raw_data.txt`.

With those files in place we used the `reporter/report.py` script to clean the raw data and plot a graphical representation of it.

While the tests were running we also monitored the number of connections to the backend result (redis server) and to the message broker (rabbitmq):
   - Backend Result: we connected to the server using `redis-cli` and periodically ran `info clients`, taking note of the maximum value for simultaneous client connections;
   - Broker: we monitored the maximum number of connections for each test through rabbitmq web interface `http://localhost:15672`, under the connections tab.

### Results

#### __Baseline (Prefork)__

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 1947.09 | 1 | 3 |

![PID 94502](../results/base/monitoring/plot-94502.png)
![PID 94507](../results/base/monitoring/plot-94507.png)

We can see that the CPU usage stayed below 1% most of the time, having a peak of approximately 2% for one of the celery processes.

For the memory (rss) we can see that a total maximum of approximately 100MB was consumed, but most of the time it stayed below 80MB.

#### __Concurrency with Prefork__

##### _Concurrency of 2_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 986.22 | 2 | 4 |

![PID 77464](../results/prefork/2/monitoring/plot-77464.png)
![PID 77467](../results/prefork/2/monitoring/plot-77467.png)
![PID 77468](../results/prefork/2/monitoring/plot-77468.png)

We can see that the CPU usage stayed below 2% most of the time, having a peak of approximately 3.5% for one of the celery processes and 1.6% for another of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 140MB was consumed, but most of the time it stayed below 90MB.

##### _Concurrency of 4_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 586.12 | 4 | 4 |

![PID 83508](../results/prefork/4/monitoring/plot-83508.png)
![PID 83516](../results/prefork/4/monitoring/plot-83516.png)
![PID 83518](../results/prefork/4/monitoring/plot-83518.png)
![PID 83519](../results/prefork/4/monitoring/plot-83519.png)
![PID 83520](../results/prefork/4/monitoring/plot-83520.png)

We can see that the CPU usage stayed below 2% most of the time, having a peak of approximately 5.5%, 4.5%, 1.7%, 0.8% and 0.1% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 200MB was consumed, but most of the time it stayed below 180MB.

##### _Concurrency of 8_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 392.08 | 8 | 4 |

![PID 89427](../results/prefork/8/monitoring/plot-89427.png)
![PID 89432](../results/prefork/8/monitoring/plot-89432.png)
![PID 89433](../results/prefork/8/monitoring/plot-89433.png)
![PID 89434](../results/prefork/8/monitoring/plot-89434.png)
![PID 89435](../results/prefork/8/monitoring/plot-89435.png)
![PID 89436](../results/prefork/8/monitoring/plot-89436.png)
![PID 89437](../results/prefork/8/monitoring/plot-89437.png)
![PID 89438](../results/prefork/8/monitoring/plot-89438.png)
![PID 89439](../results/prefork/8/monitoring/plot-89439.png)

We can see that the CPU usage stayed below 2% most of the time, having a peak of approximately 3.5%, 1.4%, 1.0%, 0.9%, 0.8%, 0.1% and 0.1% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 265MB was consumed.

##### _Concurrency of 16_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 207.03 | 10 | 4 |

![PID 95744](../results/prefork/16/monitoring/plot-95744.png)
![PID 95753](../results/prefork/16/monitoring/plot-95753.png)
![PID 95754](../results/prefork/16/monitoring/plot-95754.png)
![PID 95756](../results/prefork/16/monitoring/plot-95756.png)
![PID 95757](../results/prefork/16/monitoring/plot-95757.png)
![PID 95758](../results/prefork/16/monitoring/plot-95758.png)
![PID 95759](../results/prefork/16/monitoring/plot-95759.png)
![PID 95760](../results/prefork/16/monitoring/plot-95760.png)
![PID 95761](../results/prefork/16/monitoring/plot-95761.png)
![PID 95762](../results/prefork/16/monitoring/plot-95762.png)
![PID 95763](../results/prefork/16/monitoring/plot-95763.png)
![PID 95764](../results/prefork/16/monitoring/plot-95764.png)
![PID 95765](../results/prefork/16/monitoring/plot-95765.png)
![PID 95766](../results/prefork/16/monitoring/plot-95766.png)
![PID 95767](../results/prefork/16/monitoring/plot-95767.png)
![PID 95768](../results/prefork/16/monitoring/plot-95768.png)
![PID 95769](../results/prefork/16/monitoring/plot-95769.png)

We can see that the CPU usage stayed below 4% most of the time, having a peak of approximately 3.5%, 1.3%, 1.2%, 1.2%, 1.2%, 0.9%, 0.9%, 0.7%, 0.6% and 0.5% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 325MB was consumed.

##### _Concurrency of 32_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 206.05 | 10 | 4 |

![PID 814](../results/prefork/32/monitoring/plot-814.png)
![PID 819](../results/prefork/32/monitoring/plot-819.png)
![PID 820](../results/prefork/32/monitoring/plot-820.png)
![PID 821](../results/prefork/32/monitoring/plot-821.png)
![PID 822](../results/prefork/32/monitoring/plot-822.png)
![PID 823](../results/prefork/32/monitoring/plot-823.png)
![PID 824](../results/prefork/32/monitoring/plot-824.png)
![PID 825](../results/prefork/32/monitoring/plot-825.png)
![PID 826](../results/prefork/32/monitoring/plot-826.png)
![PID 827](../results/prefork/32/monitoring/plot-827.png)
![PID 828](../results/prefork/32/monitoring/plot-828.png)
![PID 829](../results/prefork/32/monitoring/plot-829.png)
![PID 830](../results/prefork/32/monitoring/plot-830.png)
![PID 831](../results/prefork/32/monitoring/plot-831.png)
![PID 832](../results/prefork/32/monitoring/plot-832.png)
![PID 834](../results/prefork/32/monitoring/plot-834.png)
![PID 837](../results/prefork/32/monitoring/plot-837.png)
![PID 838](../results/prefork/32/monitoring/plot-838.png)
![PID 841](../results/prefork/32/monitoring/plot-841.png)
![PID 843](../results/prefork/32/monitoring/plot-843.png)
![PID 844](../results/prefork/32/monitoring/plot-844.png)
![PID 845](../results/prefork/32/monitoring/plot-845.png)
![PID 846](../results/prefork/32/monitoring/plot-846.png)
![PID 849](../results/prefork/32/monitoring/plot-849.png)
![PID 852](../results/prefork/32/monitoring/plot-852.png)
![PID 853](../results/prefork/32/monitoring/plot-853.png)
![PID 854](../results/prefork/32/monitoring/plot-854.png)
![PID 855](../results/prefork/32/monitoring/plot-855.png)
![PID 856](../results/prefork/32/monitoring/plot-856.png)
![PID 857](../results/prefork/32/monitoring/plot-857.png)
![PID 858](../results/prefork/32/monitoring/plot-858.png)
![PID 859](../results/prefork/32/monitoring/plot-859.png)
![PID 860](../results/prefork/32/monitoring/plot-860.png)

We can see that the CPU usage stayed below 4% most of the time, having a peak of approximately 5.8%, 1.75%, 1.6%, 1.2%, 0.7%, 0.6%, 0.4%, 0.4%, 0.3%, 0.2% and 0.1% for each of the celery processes.

For the memory (rss) we can see that a total maximum (considering all celery precesses) of approximately 550MB was consumed.

Overall we can see that using concurrency with prefork spawns multiple celery processes, mainly increasing memory consumption and the number of connections used for the backend result, the connection to the backend is far from exhausting the default limit (1000 for redis) though.

#### __Concurrency with Gevent__

##### _Concurrency of 2_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 990.77 | 4 | 4 |

![PID 60287](../results/gevent/2/monitoring/plot-60287.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 2.75%.

For the memory (rss) we can see a maximum of approximately 75MB was consumed, with mainly 5 plateaus of memory consumption being formed during the tests execution at 75MB, 65MB, 40MB and 20MB (twice).

##### _Concurrency of 4_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 597.12 | 4 | 4 |

![PID 54144](../results/gevent/4/monitoring/plot-54144.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 4.0%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 4 plateaus of memory consumption being formed during the tests execution at 77.25MB, 60MB, 55MB, and 20MB.

##### _Concurrency of 8_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 385.08 | 6 | 4 |

![PID 63906](../results/gevent/8/monitoring/plot-63906.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 3.0%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 8 plateaus of memory consumption being formed during the tests execution at 77.5MB, 60MB, 57.5MB, 40MB, 30MB, 20MB (twice) and 10MB.

##### _Concurrency of 16_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 208.03 | 8 | 4 |

![PID 67673](../results/gevent/16/monitoring/plot-67673.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 6.3%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 3 plateaus of memory consumption being formed during the tests execution at 77.5MB, 47.5MB, and 41MB. By the end of the process the memory consumption progressively increases again with another peak coinciding with the CPU peak.

##### _Concurrency of 32_

| Total Time (sec) | Backend Connections (max) | Broker Connections (max) |
| :---: | :---: | :---: |
| 206.03 | 8 | 4 |

![PID 72130](../results/gevent/32/monitoring/plot-72130.png)

We can see that the CPU usage stayed below 1% most having a peak of approximately 6.3%.

For the memory (rss) we can see a maximum of approximately 77.5MB was consumed, with mainly 5 plateaus of memory consumption being formed during the tests execution at 77.5MB, 75.5MB, 61MB, 60MB and 20MB.

