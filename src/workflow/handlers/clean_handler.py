"""
Handler for the 'clean' command.
"""
from typing import Tuple, List
from ..feedback_builder import FeedbackBuilder
from ..input_handler import ParsedInput
from ...services.eventkit_bridge import EventKitBridge
from ...utils.logger import get_logger

logger = get_logger(__name__)

def handle_clean_command(parsed_input: ParsedInput, feedback: FeedbackBuilder) -> FeedbackBuilder:
    """
    Handle the 'clean' command to remove future/incomplete tagged items.
    
    Args:
        parsed_input: Parsed input with command and args
        feedback: FeedbackBuilder to add results
        
    Returns:
        FeedbackBuilder with result items
    """
    bridge = EventKitBridge()
    
    # Check if 'confirm' is in args
    is_confirm = "confirm" in parsed_input.args
    
    try:
        if not is_confirm:
            # Dry run: show what would be deleted
            ev_count, rm_count, titles = bridge.cleanup_tagged_items(dry_run=True)
            
            if ev_count + rm_count == 0:
                return feedback.add_item(
                    title="没有发现需要清理的日程或提醒",
                    subtitle="只清理带有 #Reminder-Alf 标签的未来日程和未完成提醒",
                    valid=False
                )
            
            feedback.add_item(
                title=f"准备清理 {ev_count} 个日程和 {rm_count} 个提醒",
                subtitle="⚠️ 点击确认执行 (只清理未发生的日程和未完成的提醒)",
                arg="clean confirm",
                valid=True
            )
            
            for title in titles[:10]: # Show top 10 as preview
                feedback.add_item(
                    title=f"待删除: {title}",
                    subtitle="符合清理规则",
                    valid=False
                )
                
            if len(titles) > 10:
                feedback.add_item(
                    title=f"... 以及另外 {len(titles) - 10} 项",
                    valid=False
                )
        else:
            # Actual cleanup
            ev_count, rm_count, titles = bridge.cleanup_tagged_items(dry_run=False)
            
            feedback.add_item(
                title="清理成功！",
                subtitle=f"已移除 {ev_count} 个未来日程和 {rm_count} 个未完成提醒。",
                valid=False
            )
            
    except Exception as e:
        logger.error(f"Cleanup error: {e}", exc_info=True)
        return feedback.add_error("清理失败", str(e))
        
    return feedback
