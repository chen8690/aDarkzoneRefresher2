"""「暗区突围」武装派遣自动刷新。

只校验词条、只点该行的 ↻ 刷新；**绝不代点「派遣」**（派遣永远由人手动点）。
默认 dry-run（只读屏、算坐标、不点击），加 ``--live`` 才真点。

导入本包时会把子进程的 stdout/stderr 统一收敛到 UTF-8。原因：中文 Windows 的
控制台代码页通常是 GBK(cp936)，一旦把输出**重定向到文件或管道**（CI、写日志、
父进程捕获），Python 就不再用控制台 API 而是退回该代码页编码，此时 ``print``
刷新箭头 ``↻``(U+21BB) 之类字符会抛 ``UnicodeEncodeError`` 直接把脚本打断。
控制台下本来就是 UTF-8，会被跳过，行为不变。
"""

from __future__ import annotations

import sys

__version__ = "1.0.0"

__all__ = ["__version__"]


def force_utf8_stdio() -> None:
    """把标准输出/错误切到 UTF-8，能切多少切多少，绝不因此报错。"""
    for stream in (sys.stdout, sys.stderr):
        if stream is None:
            continue
        enc = (getattr(stream, "encoding", None) or "")
        enc = enc.replace("-", "").replace("_", "").lower()
        if enc in ("utf8", "cp65001"):
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass


force_utf8_stdio()
