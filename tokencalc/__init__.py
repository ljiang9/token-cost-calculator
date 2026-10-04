"""token-cost-calculator：启发式估算中英文混合文本的 token 数，并按内置价格表算成本。

重要声明：本项目的 token 数为**启发式估算，非精确值**，精确结果请以官方 tokenizer 为准；
价格表为**快照**，实际费用以各模型官方最新定价为准。
"""

__version__ = "0.1.0"

DISCLAIMER = "本工具的 token 数为启发式估算、非精确值，精确以 tokenizer 为准；价格为快照，以官方定价为准。"
