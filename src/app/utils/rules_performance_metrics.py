"""Rules performance metrics module"""

# Standard library imports
import time
import psutil
import os

class RulesPerformanceMetrics:
    def __init__(self):
        """
        Initialize the performance metrics dictionary.
        """
        self.metrics = {
            "data_fetch_time": 0,
            "rules_fetch_time": 0,
            "rules_eval_time": 0,
            "cpu_usage": 0,
            "memory_usage": 0,
            "process_id": None,
            "process_name": None,
            "system_cpu_count": 0,
            "system_memory_total": 0,
            "system_memory_available": 0,
            "system_disk_usage": 0,
            "execution_details": {},
        }

    def start_timer(self):
        """
        Start a timer to measure execution time.
        :return: The start time.
        """
        return time.time()

    def stop_timer(self, start_time, metric_name):
        """
        Stop the timer and update the performance metric.
        :param start_time: The start time of the timer.
        :param metric_name: The name of the metric to update.
        """
        elapsed_time = time.time() - start_time
        self.metrics[metric_name] = elapsed_time

    def record_cpu_and_memory_usage(self):
        """
        Record CPU and memory usage of the current process.
        """
        process_info = psutil.Process()
        self.metrics["cpu_usage"] = process_info.cpu_percent(interval=1)
        self.metrics["memory_usage"] = process_info.memory_info().rss / (1024 * 1024)  # in MB
        self.metrics["process_id"] = os.getpid()
        self.metrics["process_name"] = process_info.name()

    def record_system_metrics(self):
        """
        Record system-level metrics such as CPU count, memory, and disk usage.
        """
        self.metrics["system_cpu_count"] = psutil.cpu_count(logical=True)
        self.metrics["system_memory_total"] = psutil.virtual_memory().total / (1024 * 1024)  # in MB
        self.metrics["system_memory_available"] = psutil.virtual_memory().available / (1024 * 1024)  # in MB
        self.metrics["system_disk_usage"] = psutil.disk_usage('/').used / (1024 * 1024 * 1024)  # in GB

    def record_execution_details(self, details):
        """
        Record additional execution details.
        :param details: A dictionary containing execution details.
        """
        self.metrics["execution_details"] = details

    def get_performance_metrics(self):
        """
        Retrieve the collected performance metrics.
        :return: A dictionary containing performance metrics.
        """
        return self.metrics