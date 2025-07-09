class Log4P:
    def __init__(self,):
        pass
    
    def _log(self, level, message):
        print(f"[{level}] {message}")
    
    def info(self, message):
        self._log("INFO",
                  message)