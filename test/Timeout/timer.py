import threading
import time
import random

class timer():
    """
    计时器类
    测试计时器线程以及计时器停用、启用、重启功能
    """
    def __init__(self):
        self.time_max = random.randint(2000, 3000)    # 计时器最大时间
        self.timer_start = None       # 计时器开始时间
        self.timer_stop = self.time_max # 计时器停止时间
        self.timer_running: bool = True  # 计时器运行状态     

    def timer_function(self):
        """
        计时器函数
        """
        self.timer_start = time.time()
        while True:
            while self.timer_running:
                Time = (time.time() - self.timer_start) * 1000
                if Time > self.timer_stop:
                    print("Time:" + str(Time))
                    print("Time stop:" + str(self.timer_stop))
                    print("Time out")
                    self.stop_timer()

    def run_timer(self):
        """
        运行计时器
        """
        timer_thread = threading.Thread(target=self.timer_function)
        timer_thread.daemon = True  # 设置为守护线程，以便主线程退出时自动退出
        timer_thread.start()

    def restart_timer(self):
        """
        重启计时器
        """
        self.timer_start = time.time()
        self.time_max = random.randint(2000, 3000) 
        self.timer_stop = self.time_max

    def stop_timer(self):
        """
        停止计时器
        """
        self.timer_running = False

    def start_timer(self):
        """
        启动计时器
        """
        self.timer_running = True


def main():
    Timer = timer()
    Timer.run_timer()
    time.sleep(3)
    Timer.restart_timer()
    Timer.start_timer()
    time.sleep(3)


if __name__=="__main__":
    main()