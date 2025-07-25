import logging
import struct
import random
import time
import sys
from handler.manager import CommManager
from comm.protocol.command import Command
from config.log import setup_logging
from util.signal import generate_test_signal

setup_logging()
logger = logging.getLogger(__name__)

manager = CommManager("COM2")


def send_check_resp():
    """发送CHECK_RESP消息"""
    t, sig, freq = generate_test_signal()
    test_data = sig.tolist()
    data_bytes = struct.pack(f">{len(test_data)}f", *test_data)
    manager._send_message(Command.CHECK_RESP, data_bytes)
    logger.info(f"已发送CHECK_RESULT消息，包含{len(test_data)}个浮点数")


def loop_check_resp():
    global _should_stop_check
    _should_stop_check = False
    """循环发送CHECK_RESP消息"""
    while not _should_stop_check:
        send_check_resp()
        logger.info("等待1秒后再次发送CHECK_RESP消息...")
        time.sleep(1)  # 每秒发送一次


def stop_check_resp():
    """停止循环发送CHECK_RESP消息"""
    global _should_stop_check
    _should_stop_check = True
    logger.info("已请求停止发送CHECK_RESP消息")


def cli():
    """命令行界面"""
    print("FTIR Slave CLI")
    print("可用命令: connect, check_resp, exit")

    while True:
        cmd = input("> ").strip().lower()

        if cmd == "connect":
            manager.connect()
        elif cmd == "disconnect":
            manager.disconnect()
        elif cmd == "check_resp":
            send_check_resp()
        elif cmd == "loop_check_resp":
            loop_check_resp()
        elif cmd == "stop_check_resp":
            stop_check_resp()
        elif cmd == "exit":
            break
        else:
            print("未知命令")
    sys.exit(0)


if __name__ == "__main__":
    cli()
