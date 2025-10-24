import datetime
import threading
import time
import sys
import os
import atexit
import logging

# ANSI color code for orange (RGB: 255, 165, 0)
ORANGE = '\033[38;2;255;165;0m'
RESET = '\033[0m'

# Global variables for startup initialization
_hooks_installed = False
_start_time = None
_original_send_sync = None
_interrupt_detected = False
_message_printed = False

def format_time_minutes_seconds(total_seconds):
    """Convert seconds to minutes and seconds format"""
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def check_for_interrupt():
    """Check if KeyboardInterrupt occurred and handle it"""
    global _start_time, _interrupt_detected
    if _interrupt_detected and _start_time is not None:
        total_time = time.time() - _start_time
        formatted_time = format_time_minutes_seconds(total_time)
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"{ORANGE}🕒 [{timestamp}] Process interrupted (Time taken: {formatted_time}){RESET}")
        _start_time = None
        _interrupt_detected = False

def cleanup_on_exit():
    """Called when program exits"""
    global _start_time
    if _start_time is not None:
        total_time = time.time() - _start_time
        formatted_time = format_time_minutes_seconds(total_time)
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"{ORANGE}🕒 [{timestamp}] Process interrupted (Time taken: {formatted_time}){RESET}")

class LoggingInterceptor(logging.Handler):
    """Custom logging handler to intercept server startup message"""
    def __init__(self):
        super().__init__()
        
    def emit(self, record):
        global _message_printed
        
        # Check if this is the server URL message
        if not _message_printed and "To see the GUI go to:" in record.getMessage():
            # Print  message right after
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"{ORANGE}\n🕒 [{timestamp}] Show 24h Clock in CMD console-SG initialized at ComfyUI startup{RESET}")
            sys.stdout.flush()
            _message_printed = True

def install_logging_interceptor():
    """Install logging handler to intercept server messages"""
    try:
        # Get the root logger
        root_logger = logging.getLogger()
        
        # Add interceptor
        interceptor = LoggingInterceptor()
        interceptor.setLevel(logging.INFO)
        root_logger.addHandler(interceptor)
        
        return True
    except Exception as e:
        print(f"\033[91mLogging interceptor error: {e}\033[0m")
        return False

def install_startup_hooks():
    """Install hooks with delayed initialization for startup"""
    global _hooks_installed, _original_send_sync
    
    if _hooks_installed:
        return True
    
    try:
        # Register exit handler instead of signal handler
        atexit.register(cleanup_on_exit)
        
        # Import here to avoid potential circular imports at startup
        from server import PromptServer
        
        # Check if PromptServer instance exists and is properly initialized
        if hasattr(PromptServer, 'instance') and PromptServer.instance is not None:
            _original_send_sync = PromptServer.instance.send_sync
            
            def startup_logging_send_sync(event, data, sid=None):
                global _start_time
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                
                if event == "execution_start":
                    _start_time = time.time()
                    print(f"\033[96m🕒 [{timestamp}] Processing Begins...\033[0m")
                
                elif event == "execution_success":
                    if _start_time is not None:
                        total_time = time.time() - _start_time
                        formatted_time = format_time_minutes_seconds(total_time)
                        print(f"\033[92m🕒 [{timestamp}] Processing Completed (Time Taken: {formatted_time}) \033[0m")
                        _start_time = None  # Reset for next execution
                    else:
                        print(f"\033[92m🕒 [{timestamp}] Processing Completed \033[0m")
                
                elif event == "execution_error":
                    if _start_time is not None:
                        total_time = time.time() - _start_time
                        formatted_time = format_time_minutes_seconds(total_time)
                        print(f"\033[91m🕒 [{timestamp}] Processing Failed (Total time: {formatted_time})\033[0m")
                        _start_time = None  # Reset for next execution
                    else:
                        print(f"\033[91m🕒 [{timestamp}] Processing Failed\033[0m")
                
                elif event == "execution_interrupted":
                    if _start_time is not None:
                        total_time = time.time() - _start_time
                        formatted_time = format_time_minutes_seconds(total_time)
                        print(f"{ORANGE}🕒 [{timestamp}] Process interrupted (Time taken: {formatted_time}) {RESET}")
                        _start_time = None  # Reset for next execution
                
                return _original_send_sync(event, data, sid)
            
            PromptServer.instance.send_sync = startup_logging_send_sync
            _hooks_installed = True
            
            return True
            
    except Exception as e:
        print(f"\033[91mShow Clock in CMD console hook error: {e}\033[0m")
        return False

def delayed_hook_installation():
    """Attempt hook installation with retries and delays"""
    max_attempts = 10
    delay = 0.5
    
    for attempt in range(max_attempts):
        if install_startup_hooks():
            return
        
        print(f"\033[93mShow Clock in CMD console startup attempt {attempt + 1}/{max_attempts}, retrying in {delay}s...\033[0m")
        time.sleep(delay)
        delay = min(delay * 1.5, 5.0)  # Exponential backoff, max 5 seconds
    
    print("\033[91m⚠️ 🕒 Show Clock in CMD console failed to initialize at startup\033[0m")

# Install logging interceptor immediately when module loads
install_logging_interceptor()

# Start delayed hook installation
threading.Thread(target=delayed_hook_installation, daemon=True).start()

class ShowClockinCMDconsoleSG:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # Explicitly require IMAGE type
            },
        }

    RETURN_TYPES = ("IMAGE",)  # Explicitly return IMAGE type
    RETURN_NAMES = ("image",)
    FUNCTION = "process_image"
    CATEGORY = "utils"

    def __init__(self):
        pass

    def process_image(self, image):
        """Pass through the image unchanged"""
        try:
            return (image,)
        except KeyboardInterrupt:
            global _start_time, _interrupt_detected
            if _start_time is not None:
                total_time = time.time() - _start_time
                formatted_time = format_time_minutes_seconds(total_time)
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                print(f"\033[93m🕒 [{timestamp}] Process interrupted (Time taken: {formatted_time})\033[0m")
                _start_time = None
            raise

NODE_CLASS_MAPPINGS = {
    "ShowClockinCMDconsoleSG": ShowClockinCMDconsoleSG,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowClockinCMDconsoleSG": "🕒Show Clock in CMD console-SG",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]


