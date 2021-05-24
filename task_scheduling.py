import schedule
import arrow
import time
import threading

def job1(): #job1完成再进行job2
    print("job1 start time: %s" % arrow.get().format())
    time.sleep(5)
    print("job1 end")
    job2()

def job2():
    print("job2 start time: %s" % arrow.get().format())


def job3():
    print("job3 start time: %s" % arrow.get().format())

def run_threaded(job_func): #多线程同时进行
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == '__main__':
    schedule.every(10).seconds.do(run_threaded,job1)
    schedule.every(10).seconds.do(run_threaded,job3)
    schedule.every().day.at("17:37").do(run_threaded,job3)

    while True:
        schedule.run_pending()

