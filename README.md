# python-multiprocessing-bfs-crawler
A simple multiprocessing example in python

This is a multiprocessing example in python.
Multi-threading is not used as it has a major drawback. Python interpreter doesn't actually implement multthreading to use multiple cores of the cpu. So, implementing multi-threading won't do any merit in terms of faster execution. It will be same as single thread.
In multi-processing, the os initializes a separate python interpreter instance to each sub process and so, it can be used to speed up your code.
Multi-threading and multi-processing has different advantages depending on the usage.
