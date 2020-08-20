from taskSamples import taskManager

import multiprocessing as mp

import time

def template_target(q):
    print('start Process')
    item = q.get()
    while True:
        item = q.get()
        print('Get an item', item**512**10)
        print('end Task')

class WorkersManager():
    def __init__(self, /, target=None, workersCount = 4, max_task_count = 30, daemon=False):
        if target==None:
            target = template_target
        self.m_workersCount = workersCount
        self.m_isDaemon = daemon
        self.m_queue = mp.Queue(max_task_count)
        self.m_taskQueue = []
        self.m_workers = []
        self.m_lastTaskNumber = 1
        # self.m_emptyId = [i for i in range(1, workersCount + 1)]
        self.m_busyWorkers = 0

        # lizy initialization
        # self.m_workers = [mp.Process(target=target, args=(self.m_queue,), daemon=daemon) for index in range(1, workersCount + 1)]

    def _hasFreeWorker(self):
        print('!@#', self.m_busyWorkers < self.m_workersCount)
        return self.m_busyWorkers < self.m_workersCount

    def startTask(self, taskData, task=None):
        if not task:
            task = template_target
        # is task already on queue?
        # 1) create a process
        # 2) create an unique id for process
        # 3) create timer that should refresh the element 

        if self._hasFreeWorker():
            worker = mp.Process(target=task, args=(self.m_queue,))
            worker.start()
            self.m_busyWorkers += 1
            self.m_workers.append(worker)
            self.m_lastTaskNumber+=1
        return self.m_lastTaskNumber - 1

    def join(self):
        if self.m_isDaemon:
            return
        for worker in self.m_workers:
            worker.join()
        
def main():
    workersManager = WorkersManager(target=template_target, daemon=False)

if __name__ == "__main__":
    main()