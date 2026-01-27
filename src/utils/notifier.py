
"""
System notification utility for macOS using osascript.
"""
import subprocess
from shlex import quote


def send_notification(title: str, message: str, sound: bool = True) -> None:
    """
    Send a macOS system notification.
    
    Args:
        title: Notification title
        message: Notification message body
        sound: Whether to play default sound
    """
def send_notification(title: str, message: str, sound: bool = True) -> None:
    """
    Send a macOS system notification.
    """
    # Escape quotes and backslashes for AppleScript string literals
    safe_title = title.replace('\\', '\\\\').replace('"', '\\"')
    safe_message = message.replace('\\', '\\\\').replace('"', '\\"')
    
    script = f'display notification "{safe_message}" with title "{safe_title}"'
    if sound:
        script += ' sound name "default"'

    try:
        # Pass script via stdin to avoid shell argument limit/parsing issues
        subprocess.run(['osascript'], input=script, text=True, check=False)
    except Exception:
        pass
