"""命令行入口。

用法：
    python3 -m tokencalc calc --file prompt.txt --model gpt-4o
    python3 -m tokencalc compare --file prompt.txt
    python3 -m tokencalc list
"""

from __future__ import annotations

import argparse
import sys

from . import DISCLAIMER
from .calculator import compare, cost_for_model
from .prices import PriceTable
from .tokenizer import estimate_tokens


def _read_text(args) -> str:
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    if args.text:
        return args.text
    return ""


def _output_tokens_for(input_tokens: int, args) -> int:
    if args.output_tokens is not None:
        return args.output_tokens
    return int(round(input_tokens * args.output_ratio))


def cmd_list(args) -> int:
    table = PriceTable.load()
    print(f"内置价格表（{table.meta.get('updated', '?')}，单位：美元 / 百万 token）：\n")
    print(f"{'模型':<22}{'厂商':<16}{'输入':>10}{'输出':>10}")
    for m in table.list_models():
        print(f"{m['id']:<22}{m.get('provider',''):<16}"
              f"{m['input_per_1m']:>10.2f}{m['output_per_1m']:>10.2f}")
    print(f"\n{DISCLAIMER}")
    return 0


def cmd_calc(args) -> int:
    text = _read_text(args)
    if not text.strip():
        print("错误：请用 --file 或 --text 提供文本。", file=sys.stderr)
        return 2
    est = estimate_tokens(text)
    out_tokens = _output_tokens_for(est["total"], args)

    table = PriceTable.load()
    if not table.has(args.model):
        print(f"错误：模型 {args.model} 不在价格表中，可用 list 查看。", file=sys.stderr)
        return 2

    row = cost_for_model(table.get(args.model), est["total"], out_tokens)
    print(f"输入文本估算：汉字 {est['cjk_chars']} 个、英文词 {est['latin_words']} 个 "
          f"≈ 共 {est['total']} tokens（中文 {est['cjk_tokens']} + 英文 {est['latin_tokens']}）")
    print(f"按输出 {out_tokens} tokens 估算：")
    print(f"  模型 {row['id']}（{row['provider']}）")
    print(f"  输入成本: ${row['input_cost']:.6f}")
    print(f"  输出成本: ${row['output_cost']:.6f}")
    print(f"  合计:    ${row['total_cost']:.6f}")
    print(f"\n{DISCLAIMER}")
    return 0


def cmd_compare(args) -> int:
    text = _read_text(args)
    if not text.strip():
        print("错误：请用 --file 或 --text 提供文本。", file=sys.stderr)
        return 2
    est = estimate_tokens(text)
    out_tokens = _output_tokens_for(est["total"], args)

    table = PriceTable.load()
    rows = compare(table, est["total"], out_tokens)
    print(f"输入 ≈ {est['total']} tokens（中文 {est['cjk_tokens']} + 英文 {est['latin_tokens']}），"
          f"输出按 {out_tokens} tokens 估算，各模型成本对比（由低到高）：\n")
    print(f"{'模型':<22}{'厂商':<16}{'输入$':>12}{'输出$':>12}{'合计$':>14}")
    for r in rows:
        print(f"{r['id']:<22}{r['provider']:<16}"
              f"{r['input_cost']:>12.6f}{r['output_cost']:>12.6f}{r['total_cost']:>14.6f}")
    print(f"\n{DISCLAIMER}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tokencalc", description="启发式 token 估算与多模型成本对比")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_input_args(sp):
        sp.add_argument("--file", help="输入文本文件路径")
        sp.add_argument("--text", help="直接传入文本")
        sp.add_argument("--output-tokens", type=int, default=None,
                        help="指定输出 token 数（默认按 --output-ratio 推算）")
        sp.add_argument("--output-ratio", type=float, default=1.0,
                        help="输出 token = 输入 token × 该比例（默认 1.0）")

    c = sub.add_parser("calc", help="估算给定文本的 token 与单模型成本")
    add_input_args(c)
    c.add_argument("--model", required=True, help="模型 id（见 list）")
    c.set_defaults(func=cmd_calc)

    cmp_ = sub.add_parser("compare", help="多模型成本对比表")
    add_input_args(cmp_)
    cmp_.set_defaults(func=cmd_compare)

    lst = sub.add_parser("list", help="列出内置模型价格表")
    lst.set_defaults(func=cmd_list)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
