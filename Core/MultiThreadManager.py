import asyncio
import concurrent.futures

class MultiThreadManager:
    def __init__(self, max_workers=6):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    async def run(self, func, *args, timeout=None):
        loop = asyncio.get_running_loop()

        try:
            task = loop.run_in_executor(self.executor, func, *args)

            if timeout:
                return await asyncio.wait_for(task, timeout=timeout)

            return await task

        except asyncio.TimeoutError:
            return "Task timed out safely."
        except Exception as e:
            return f"Thread error: {e}"

    def run_sync(self, func, *args):
        try:
            return self.executor.submit(func, *args).result()
        except Exception as e:
            return f"Execution failed: {e}"

    def shutdown(self):
        self.executor.shutdown(wait=False)


ThreadManager = MultiThreadManager()