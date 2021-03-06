from src.LogInfo import write_error
import random


SIMULATION_DURATION = 1800
MAX_JOB_NUM = 10000
TIME_GAP = 0.01


class Job(object):
    def __init__(self, job_str):
        """
        Init a job object based on the job_string
        :param job_str: a string to describe the job
        """
        job_info_list = job_str.split("\t")
        self.job_str = job_str
        self.jobID = job_info_list[1]
        self.ts = float(job_info_list[0]) if float(job_info_list[0])>TIME_GAP else TIME_GAP
        self.origPort = int(job_info_list[3])
        self.endStatus = str(job_info_list[11])
        # Initially the port num is not assigned
        self.realPort = -1

        self.fromPort = self.origPort
        self.toPort = int(job_info_list[5])
        self.status = 0
        # 0: to_do
        # 1: doing
        # 2: just_finished
        # 3: cleaned

        self.duration = float(job_info_list[8])

    def __str__(self):
        return "%s\t%f\t%d\t%d\t%d\t%d\t%f\n" % (self.jobID,
                                                 self.ts,
                                                 self.origPort,
                                                 self.realPort,
                                                 self.fromPort,
                                                 self.toPort,
                                                 self.duration
        )

    def __repr__(self):
        return "%s\t%f\t%d\t%d\t%d\t%d\t%f\n" % (self.jobID,
                                                 self.ts,
                                                 self.origPort,
                                                 self.realPort,
                                                 self.fromPort,
                                                 self.toPort,
                                                 self.duration
        )

    def increase_origPort(self, gap):
        """
        Reset the origPort
        :param gap: the gap between oldOrigPort and newOrigPort.
        :return:
        """
        self.origPort += gap
        if self.origPort >= 65535:
            self.origPort = self.origPort - 16383


class JobQueue(object):
    def __init__(self,file_path=None):
        """
        Job Queue Object, describe the overall jobs
        :param file_path: the folder where all job strings are stored.
        """
        if file_path is None:
            file_path = "../data/sample_test.log"
        self.total_job_queue = []
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line.split("\t")[8] == "-":
                    # Get rid of those without a duration field.
                    continue
                job_tmp = Job(line)
                self.total_job_queue.append(job_tmp)

        self.todo_queue = []
        self.doing_queue = []
        self.finish_queue = []

        # Get start time and reset the ts for all records
        ts_start = min(float(job.ts) for job in self.total_job_queue)
        for job in self.total_job_queue:
            job.ts -= ts_start
        self.total_job_queue.sort(key=lambda x: x.ts, reverse=False)
        for job in self.total_job_queue:
            self.todo_queue.append(job)

    def get_ready(self, cur_time, time_gap):
        """
        Get The list of all "ready" jobs. These job should be added to NAT in the next time slice
        :param cur_time: current time
        :param time_gap: should use default TIME_GAP
        :return:
        """
        ready_list = []
        for job in self.todo_queue:
            if job.ts < (cur_time + time_gap):
                ready_list.append(job)

        return ready_list

    def set_doing(self, job):
        """
        Set the status of jobs as doing
        :param job: job object
        :return: True if set correctly, else False
        """
        if job in self.todo_queue:
            self.todo_queue.remove(job)
            self.doing_queue.append(job)
            ### ?job.status = 1
            return True
        else:
            write_error("Error, current job %s not in QueueTodo." % job.jobID)
            return False

    def set_finish(self, job):
        """
        Set the status of a job as finish and put it into the cooldown pool.
        :param job: job object
        :return: True if set correctly, else False
        """
        if job in self.doing_queue:
            self.doing_queue.remove(job)
            self.finish_queue.append(job)
            return True
        else:
            write_error("Error, current job %s not in QueueDoing." % job.jobID)
            return False

    def insert_urgent_job(self, job):
        """
        Insert temporary job into the system
        Be cautious when using this method
        :param job: job Object
        :return:
        """
        self.total_job_queue.append(job)
        self.todo_queue.append(job)

    def __str__(self):
        return [len(self.todo_queue), len(self.doing_queue),
                len(self.finish_queue)]


if __name__ == '__main__':
    jq = JobQueue()