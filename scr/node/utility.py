import json
import time
import random

class timer():
    def __init__(self, time_min=2000, time_max = 3000):
        self.time_min = time_min
        self.time_max = time_max
        self.timer_max = random.randint(time_min, time_max)  # 计时器最大时间
        self.timer_start = None       # 计时器开始时间
        self.timer_stop = self.time_max  # 计时器停止时间
        self.timer_running: bool = True  # 计时器运行状态     

    def timer_function(self):
        """
        计时器函数
        :return: bool   True:超时, False:未超时
        """
        self.timer_start = time.time()
        # while True:
        while self.timer_running:
            Time = (time.time() - self.timer_start) * 1000
            if Time > self.timer_stop:
                print("Time out")
                return True
            # time.sleep(0.1)         #新加，防止繁忙访问
        return False


    # def start_timer(self):
    #     """
    #     启动计时器
    #     """
    #     timer_thread = threading.Thread(target=self.timer_function)
    #     timer_thread.daemon = True  # 设置为守护线程，以便主线程退出时自动退出
    #     timer_thread.start()

    def restart_timer(self, time_min=2000, time_max = 3000):
        """
        重置计时器
        :param time_min: 计时器最小时间
        :param time_max: 计时器最大时间
        """
        self.time_min = time_min
        self.time_max = time_max
        self.timer_start = time.time()
        self.timer_stop = self.timer_max
        self.timer_running = True

    def stop_timer(self):
        """
        停止计时器
        """
        self.timer_running = False

    def start_timer(self, time_min=2000, time_max = 3000):
        """
        启动计时器,重置计时器
        """
        self.restart_timer(time_min, time_max)
        self.timer_running = True

class peer():
    def load_config(filename):
        with open(filename, 'r') as file:
            config = json.load(file)

        return config