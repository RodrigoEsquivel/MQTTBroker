import threading

class ThreadManager:
    
    @staticmethod
    def create_new_thread(target_function, arguments): 
        return threading.Thread(target=target_function, args=arguments)
        
    @staticmethod
    def start_thread(thread):
        thread.start()
