# token-cost-calculator

在没有任何依赖的情况下，**启发式估算**一段中英文混合文本的 token 数，并按内置模型价格表估算调用成本、做多模型对比。

> ⚠️ **重要声明**
> - 本工具的 token 数为**启发式估算、非精确值**，精确结果请以官方 tokenizer（如 tiktoken）为准；
> - 内置价格表为**快照**，实际费用以各模型官方最新定价为准。

## 功能简介

- **中英文混合 token 估算**：汉字按字计数，英文按「单词数 × 1.3」经验比例折算；
- **内置模型价格表**（`tokencalc/data/models.json`）：常见模型 input / output 每百万 token 价格；
- **CLI**：`list`（查看价格表）、`calc`（单模型 token + 成本）、`compare`（多模型成本对比表）；
- 零第三方依赖，Python 3.10+ 直接运行。

## 快速开始

```bash
git clone https://github.com/ljiang9/token-cost-calculator.git
cd token-cost-calculator
python3 -m tokencalc --help
```

## 使用示例

**1. 列出内置模型价格表**

```bash
python3 -m tokencalc list
```

输出（节选）：

```
内置价格表（2026-10，单位：美元 / 百万 token）：

模型                  厂商              输入        输出
gpt-4o-mini           OpenAI             0.15      0.60
gpt-4o                OpenAI             2.50     10.00
deepseek-chat         DeepSeek           0.27      1.10
...
本工具的 token 数为启发式估算、非精确值，精确以 tokenizer 为准；价格为快照，以官方定价为准。
```

**2. 估算单段文本在某个模型上的成本**

```bash
python3 -m tokencalc calc --text "你好，请用一句话解释什么是光合作用。" --model gpt-4o
```

输出：

```
输入文本估算：汉字 15 个、英文词 0 个 ≈ 共 15 tokens（中文 15 + 英文 0）
按输出 15 tokens 估算：
  模型 gpt-4o（OpenAI）
  输入成本: $0.000038
  输出成本: $0.000150
  合计:    $0.000188
...
```

也可以传文件：

```bash
python3 -m tokencalc calc --file prompt.txt --model claude-3-5-sonnet
```

输出 token 默认按「输入 token × 1.0」估算，可用 `--output-ratio` 或 `--output-tokens` 调整：

```bash
python3 -m tokencalc calc --file prompt.txt --model gpt-4o --output-ratio 2
python3 -m tokencalc compare --file prompt.txt --output-tokens 500
```

**3. 多模型成本对比表**

```bash
python3 -m tokencalc compare --file prompt.txt
```

输出（按总成本由低到高）：

```
输入 ≈ 120 tokens（中文 80 + 英文 40），输出按 120 tokens 估算，各模型成本对比（由低到高）：

模型                  厂商                输入$          输出$           合计$
gpt-4o-mini           OpenAI          0.000018      0.000072      0.000090
deepseek-chat         DeepSeek        0.000032      0.000132      0.000165
gpt-4o                OpenAI          0.000300      0.001200      0.001500
...
```

## 估算口径（透明说明）

- 每个汉字（含中文标点）≈ 1 个 token；
- 英文及数字：连续字母/数字串算一个词，`tokens ≈ round(单词数 × 1.3)`；
- 这只是为了在没有 tiktoken 等库时快速估计量级，**不要当作精确计费依据**。

## 目录结构

```
token-cost-calculator/
├── tokencalc/
│   ├── __main__.py      # 支持 python -m tokencalc
│   ├── cli.py           # list / calc / compare
│   ├── tokenizer.py     # 启发式 token 估算
│   ├── prices.py        # 价格表 JSON 加载
│   ├── calculator.py    # 成本计算与多模型对比
│   └── data/models.json # 内置模型价格表（快照）
├── tests/               # unittest 测试
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m compileall tokencalc
python3 -m unittest discover -s tests
```

## 许可证

本项目基于 [MIT 许可证](./LICENSE) 开源。
