"""
中文工科顶刊插图绘制工具
==========================

提供顶刊风格的 matplotlib 配置 + 9 类常用图的快速函数。

用法
----
    from paper_plot import setup_paper_style, COLORS, save_paper_figure

    setup_paper_style()                     # 全局样式（一次即可）
    fig, ax = paper_subplots(figsize=(8, 6))
    ax.plot(x, y, color=COLORS['primary'])
    save_paper_figure(fig, 'output_name')   # 同时保存 pdf 与 png

设计依据：references/figures.md 的视觉规范。

字体说明
--------
- Windows: 默认使用 SimSun（宋体）+ Times New Roman
- macOS:   建议改 'STSong' 或 'Songti SC'
- Linux:   需安装中文字体，如 fonts-wqy-zenhei 或自行装 SimSun

如果中文显示成方框，调用 reset_font_cache() 重建字体缓存。
"""

from __future__ import annotations

import os
from typing import Iterable, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import LinearSegmentedColormap


# =============================================================================
# 配色方案（与 references/figures.md 一致）
# =============================================================================

COLORS = {
    # 主色（按使用频率排序）
    'primary':   '#1F77B4',  # 深蓝
    'secondary': '#D62728',  # 砖红
    'tertiary':  '#2CA02C',  # 草绿
    'quaternary':'#FF7F0E',  # 橙
    'quinary':   '#9467BD',  # 紫
    'senary':    '#8C564B',  # 棕

    # 中性
    'dark':      '#333333',  # 深灰
    'mid':       '#999999',  # 中灰
    'light':     '#CCCCCC',  # 浅灰

    # 背景
    'white':     '#FFFFFF',
    'bg_gray':   '#F5F5F5',
    'bg_header': '#E8E8E8',
    'bg_blue':   '#D6EAF8',  # 网络结构图：卷积/全连接背景
    'bg_yellow': '#FCF3CF',  # 网络结构图：注意力背景
    'bg_green':  '#D5F5E3',  # 网络结构图：跳连接背景
    'bg_red':    '#FADBD8',  # 网络结构图：损失/输出背景

    # 强调
    'highlight_yellow': '#FFF9E6',  # 表格本文行突出
    'load_arrow':       '#D62728',  # 机械结构图：载荷箭头
    'speed_arrow':      '#2CA02C',  # 机械结构图：转速箭头
}

# 多曲线推荐顺序（前 4 条用线型区分，第 5 条起加颜色区分）
LINE_STYLES = ['-', '--', '-.', ':']
MARKERS = ['o', 's', '^', 'D', 'v', 'p', '*', 'X']


# =============================================================================
# 推荐 Colormap
# =============================================================================

def get_cmap(kind: str = 'diverging'):
    """
    获取推荐 colormap。

    Parameters
    ----------
    kind : str
        - 'diverging' : 蓝-白-红，适合应力（有正负）、相关系数
        - 'physics'   : 蓝-绿-黄-红，适合压力 / 温度 / 能量场
        - 'attention' : 白-蓝，适合注意力权重 / 概率
        - 'sequential': viridis 替代品，感知均匀

    Returns
    -------
    matplotlib.colors.Colormap
    """
    if kind == 'diverging':
        return plt.get_cmap('RdBu_r')
    if kind == 'physics':
        # 蓝→青→绿→黄→红，工科常见的物理量配色
        colors_list = ['#0033A0', '#00A8E1', '#2CA02C', '#FFD700', '#D62728']
        return LinearSegmentedColormap.from_list('physics', colors_list, N=256)
    if kind == 'attention':
        return plt.get_cmap('Blues')
    if kind == 'sequential':
        return plt.get_cmap('viridis')
    raise ValueError(f"Unknown kind: {kind}. Use 'diverging' / 'physics' / 'attention' / 'sequential'.")


# =============================================================================
# 全局样式配置
# =============================================================================

def setup_paper_style(
    chinese_font: Optional[str] = None,
    english_font: str = 'Times New Roman',
    base_fontsize: int = 9,
    figsize: Tuple[float, float] = (8.0, 6.0),
    dpi: int = 300,
):
    """
    设置 matplotlib 为中文工科顶刊风格。

    Parameters
    ----------
    chinese_font : str, optional
        中文字体名。None 时按平台自动选择。
    english_font : str
        英文/数字字体（默认 Times New Roman）。
    base_fontsize : int
        基础字号，其他字号按比例。
    figsize : tuple
        默认图尺寸（英寸）。期刊单栏约 8x6，双栏约 16x6。
    dpi : int
        显示 DPI。保存 DPI 见 save_paper_figure。
    """
    if chinese_font is None:
        # 自动选择中文字体
        if os.name == 'nt':  # Windows
            chinese_font = 'SimSun'
        elif os.uname().sysname == 'Darwin':  # macOS
            chinese_font = 'STSong'
        else:  # Linux
            chinese_font = 'WenQuanYi Zen Hei'

    # 字体
    # 关键：matplotlib 不会自动 glyph fallback，因此把中文字体放在 family 列表前面，
    # 让一个能渲染中英文的字体（如 SimSun）作为主字体，避免缺字警告。
    # 英文/数字虽然由中文字体渲染，但宋体的 ASCII 符号视觉与 Times 接近，
    # 顶刊投稿时通常还会再过 LaTeX 排版，这里以"无报错、可预览"为目标。
    rcParams['font.serif'] = [chinese_font, english_font, 'DejaVu Serif']
    rcParams['font.sans-serif'] = [chinese_font, english_font, 'DejaVu Sans']
    rcParams['font.family'] = 'serif'
    rcParams['axes.unicode_minus'] = False  # 负号正常显示
    rcParams['mathtext.fontset'] = 'stix'   # 数学符号用 STIX，与 Times 协调

    # 字号
    rcParams['font.size'] = base_fontsize
    rcParams['axes.titlesize'] = base_fontsize + 2
    rcParams['axes.labelsize'] = base_fontsize
    rcParams['xtick.labelsize'] = base_fontsize - 1
    rcParams['ytick.labelsize'] = base_fontsize - 1
    rcParams['legend.fontsize'] = base_fontsize - 1
    rcParams['figure.titlesize'] = base_fontsize + 2

    # 图尺寸与分辨率
    rcParams['figure.figsize'] = figsize
    rcParams['figure.dpi'] = dpi
    rcParams['savefig.dpi'] = 600
    rcParams['savefig.bbox'] = 'tight'
    rcParams['savefig.pad_inches'] = 0.05

    # 坐标轴：四面闭合 + 朝内刻度
    rcParams['axes.linewidth'] = 0.8
    rcParams['axes.edgecolor'] = COLORS['dark']
    rcParams['axes.spines.top'] = True
    rcParams['axes.spines.right'] = True
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'
    rcParams['xtick.major.size'] = 4
    rcParams['ytick.major.size'] = 4
    rcParams['xtick.major.width'] = 0.8
    rcParams['ytick.major.width'] = 0.8
    rcParams['xtick.minor.visible'] = True
    rcParams['ytick.minor.visible'] = True
    rcParams['xtick.minor.size'] = 2
    rcParams['ytick.minor.size'] = 2
    rcParams['xtick.minor.width'] = 0.5
    rcParams['ytick.minor.width'] = 0.5
    rcParams['xtick.top'] = True
    rcParams['ytick.right'] = True

    # 网格：浅灰虚线，仅主刻度
    rcParams['axes.grid'] = True
    rcParams['axes.grid.which'] = 'major'
    rcParams['grid.linestyle'] = '--'
    rcParams['grid.linewidth'] = 0.5
    rcParams['grid.color'] = COLORS['light']
    rcParams['grid.alpha'] = 0.7
    rcParams['axes.axisbelow'] = True

    # 线条
    rcParams['lines.linewidth'] = 1.5
    rcParams['lines.markersize'] = 5

    # 图例
    rcParams['legend.frameon'] = True
    rcParams['legend.edgecolor'] = COLORS['mid']
    rcParams['legend.framealpha'] = 0.9
    rcParams['legend.facecolor'] = 'white'
    rcParams['legend.fancybox'] = False  # 直角边框更"论文"
    rcParams['legend.borderpad'] = 0.4

    # 颜色循环（前 4 条用线型 + 这套颜色循环）
    rcParams['axes.prop_cycle'] = plt.cycler(
        color=[
            COLORS['primary'],
            COLORS['secondary'],
            COLORS['tertiary'],
            COLORS['quaternary'],
            COLORS['quinary'],
            COLORS['senary'],
        ]
    )


# =============================================================================
# 便捷创建函数
# =============================================================================

def paper_subplots(
    nrows: int = 1,
    ncols: int = 1,
    figsize: Optional[Tuple[float, float]] = None,
    **kwargs,
):
    """
    创建符合论文规范的 figure & axes。等价于 plt.subplots，但应用了默认配置。

    figsize 缺省为 (8, 6)；多子图时按列数自动放大。
    """
    if figsize is None:
        figsize = (8.0 * ncols / 1.0, 6.0 * nrows / 1.0) if (ncols > 1 or nrows > 1) else (8.0, 6.0)
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, **kwargs)
    return fig, ax


def add_minor_grid(ax, alpha: float = 0.3):
    """给坐标轴加次刻度线网格（更精细的栅格感）。"""
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth=0.3, color=COLORS['light'], alpha=alpha)


def style_legend(ax, loc: str = 'best', ncol: int = 1):
    """对已经画好的 ax 应用论文风格图例。"""
    leg = ax.legend(loc=loc, ncol=ncol)
    if leg:
        leg.get_frame().set_linewidth(0.6)
    return leg


# =============================================================================
# 9 类图的快速绘制
# =============================================================================

def plot_lines(
    ax,
    x_data: Sequence,
    y_list: Sequence[Sequence],
    labels: Sequence[str],
    use_markers: bool = False,
    marker_every: int = 5,
):
    """
    标准多曲线图：前 4 条用线型区分（实线/虚线/点划线/点线），更多则颜色区分。

    Parameters
    ----------
    ax : matplotlib axes
    x_data : 1-D x 序列
    y_list : N x len(x_data) 的曲线列表
    labels : N 个曲线的图例
    use_markers : 是否给每条曲线加 marker
    marker_every : marker 间隔（避免遮蔽曲线）
    """
    n = len(y_list)
    color_keys = ['primary', 'secondary', 'tertiary', 'quaternary', 'quinary', 'senary']
    for i, (y, label) in enumerate(zip(y_list, labels)):
        kwargs = dict(
            label=label,
            linewidth=1.5,
            linestyle=LINE_STYLES[i % len(LINE_STYLES)],
            color=COLORS[color_keys[i % len(color_keys)]],
        )
        if use_markers:
            kwargs.update(
                marker=MARKERS[i % len(MARKERS)],
                markevery=marker_every,
                markersize=5,
            )
        ax.plot(x_data, y, **kwargs)
    style_legend(ax)
    return ax


def plot_bars(
    ax,
    categories: Sequence[str],
    values: Sequence[float],
    errs: Optional[Sequence[float]] = None,
    color_key: str = 'primary',
    show_value: bool = True,
):
    """
    标准柱状图（单组）。
    """
    bars = ax.bar(
        categories,
        values,
        yerr=errs,
        color=COLORS[color_key],
        edgecolor=COLORS['dark'],
        linewidth=0.8,
        capsize=4,
        error_kw=dict(elinewidth=1.0, ecolor=COLORS['dark']),
    )
    if show_value:
        for bar, v in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f'{v:.3g}',
                ha='center', va='bottom', fontsize=8,
            )
    return bars


def plot_grouped_bars(
    ax,
    categories: Sequence[str],
    series_values: Sequence[Sequence[float]],
    series_labels: Sequence[str],
    width: float = 0.8,
):
    """
    分组柱状图：x 轴是 categories，每个 category 上有多组柱。

    Parameters
    ----------
    series_values : len(series) x len(categories)
    """
    import numpy as np
    n_series = len(series_values)
    bar_width = width / n_series
    x = np.arange(len(categories))
    color_keys = ['primary', 'secondary', 'tertiary', 'quaternary', 'quinary']
    for i, (vals, label) in enumerate(zip(series_values, series_labels)):
        offset = (i - (n_series - 1) / 2) * bar_width
        ax.bar(
            x + offset, vals, bar_width,
            label=label,
            color=COLORS[color_keys[i % len(color_keys)]],
            edgecolor=COLORS['dark'],
            linewidth=0.5,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    style_legend(ax)


def plot_heatmap(
    ax,
    data,
    cmap_kind: str = 'physics',
    cbar_label: str = '',
    contour: bool = False,
    n_levels: int = 20,
):
    """
    云图 / 热力图。

    Parameters
    ----------
    cmap_kind : 'physics' / 'diverging' / 'attention' / 'sequential'
    cbar_label : 色条标签（含单位），如"压力 / MPa"
    contour : 是否叠加等值线
    """
    cmap = get_cmap(cmap_kind)
    im = ax.imshow(data, cmap=cmap, aspect='auto', origin='lower')
    if contour:
        cs = ax.contour(data, levels=n_levels, colors='black', linewidths=0.4, alpha=0.5)
        ax.clabel(cs, inline=True, fontsize=7, fmt='%.2g')
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(cbar_label)
    cbar.ax.tick_params(labelsize=8)
    cbar.outline.set_linewidth(0.8)
    return im, cbar


def plot_scatter_categorized(
    ax,
    x_list: Sequence[Sequence],
    y_list: Sequence[Sequence],
    labels: Sequence[str],
    sizes: Optional[Sequence[Sequence]] = None,
):
    """
    多类散点图（双重区分：颜色 + marker）。

    Parameters
    ----------
    sizes : 每类的标记大小（可对应第三维数据，如参数量）
    """
    color_keys = ['primary', 'secondary', 'tertiary', 'quaternary', 'quinary', 'senary']
    for i, (xs, ys, lbl) in enumerate(zip(x_list, y_list, labels)):
        s = sizes[i] if sizes else 40
        ax.scatter(
            xs, ys,
            label=lbl,
            color=COLORS[color_keys[i % len(color_keys)]],
            marker=MARKERS[i % len(MARKERS)],
            s=s,
            alpha=0.7,
            edgecolors=COLORS['dark'],
            linewidths=0.5,
        )
    style_legend(ax)


def plot_with_confidence(
    ax,
    x: Sequence,
    y_mean: Sequence,
    y_lower: Sequence,
    y_upper: Sequence,
    label: str,
    color_key: str = 'primary',
):
    """
    带置信区间的曲线（用于不确定性可视化）。
    """
    ax.plot(x, y_mean, label=label, color=COLORS[color_key], linewidth=1.5)
    ax.fill_between(
        x, y_lower, y_upper,
        color=COLORS[color_key],
        alpha=0.18,
        linewidth=0,
    )


# =============================================================================
# 保存图片
# =============================================================================

def save_paper_figure(
    fig,
    name: str,
    formats: Iterable[str] = ('pdf', 'png'),
    output_dir: str = '.',
    dpi: int = 600,
):
    """
    保存图片。同时保存 PDF（投稿用）和 PNG（预览用）。

    Parameters
    ----------
    name : 文件名（不含扩展名）
    formats : 要保存的格式
    output_dir : 输出目录
    dpi : 栅格化分辨率
    """
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    for fmt in formats:
        path = os.path.join(output_dir, f'{name}.{fmt}')
        fig.savefig(path, dpi=dpi, bbox_inches='tight', pad_inches=0.05)
        saved.append(path)
    return saved


# =============================================================================
# 故障排查
# =============================================================================

def reset_font_cache():
    """中文显示成方框时，重建 matplotlib 字体缓存。"""
    import matplotlib
    cache_path = matplotlib.get_cachedir()
    print(f"matplotlib cache dir: {cache_path}")
    # 较新版本：matplotlib >= 3.5
    try:
        from matplotlib.font_manager import _load_fontmanager
        _load_fontmanager(try_read_cache=False)
        print("Font manager rebuilt.")
    except Exception:
        # 老版本退路
        try:
            from matplotlib.font_manager import _rebuild
            _rebuild()
            print("Font cache rebuilt (legacy).")
        except Exception as e:
            print(f"Manual rebuild failed ({e}). Try removing files in cache dir manually.")


def list_chinese_fonts():
    """列出系统可用的中文字体（看 matplotlib 能找到哪些）。"""
    from matplotlib.font_manager import fontManager
    chinese_keywords = ['宋', 'song', 'kai', '黑', 'hei', 'yahei', 'simsun', 'fangsong', 'simhei']
    found = []
    for f in fontManager.ttflist:
        name_lower = f.name.lower()
        if any(k in name_lower for k in chinese_keywords):
            found.append(f.name)
    return sorted(set(found))


# =============================================================================
# 自检
# =============================================================================

if __name__ == '__main__':
    # 跑一个最小示例，确认环境正常
    import numpy as np

    setup_paper_style()
    fig, ax = paper_subplots()
    x = np.linspace(0, 10, 200)
    plot_lines(
        ax,
        x_data=x,
        y_list=[np.sin(x), np.sin(x + 0.5), np.sin(x + 1.0), np.sin(x + 1.5)],
        labels=['方法 A', '方法 B', '方法 C', '方法 D'],
        use_markers=True,
        marker_every=20,
    )
    ax.set_xlabel('迭代步数')
    ax.set_ylabel('目标函数值')
    ax.set_title('示例：多曲线对比')
    save_paper_figure(fig, 'demo_paper_plot', output_dir='.')
    print("Saved demo_paper_plot.pdf and demo_paper_plot.png")
    print("Available Chinese fonts:", list_chinese_fonts())
