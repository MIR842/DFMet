
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests


def perform_wilcoxon_test(scores_method_1, scores_method_2):
    """
    对两个方法的分数进行Wilcoxon检验。

    参数:
        scores_method_1 (list or np.array): 方法1的分数。
        scores_method_2 (list or np.array): 方法2的分数。

    返回:
        float: Wilcoxon检验的p值。
    """
    stat, p = wilcoxon(scores_method_1, scores_method_2)
    return p


def adjust_p_values(p_values, method='bonferroni'):
    """
    对p值进行多重比较校正。

    参数:
        p_values (list of float): p值列表。
        method (str): 校正方法，默认为'bonferroni'。

    返回:
        tuple: (拒绝零假设的布尔数组, 校正后的p值数组, _, _)
    """
    return multipletests(p_values, alpha=0.05, method=method)


def analyze_dataset_and_print_results(input_csv):
    """
    从CSV文件读取数据，执行Wilcoxon检验并打印结果。

    参数:
        input_csv (str): 输入CSV文件路径。
    """
    # 读取data.csv文件
    df = pd.read_csv(input_csv)

    # 检查数据是否包含方法和Dice列
    if 'Method' not in df.columns or 'Dice' not in df.columns:
        print("输入数据缺少 'Method' 或 'Dice' 列！")
        return

    # 提取不同方法的分数
    methods = df['Method'].unique()  # 获取所有方法的名称
    scores_dict = {}

    for method in methods:
        scores_dict[method] = df[df['Method'] == method]['Dice'].values

    # 计算每两个方法之间的Wilcoxon检验
    p_values = []
    method_pairs = []

    for i in range(len(methods)):
        for j in range(i + 1, len(methods)):
            method_1 = methods[i]
            method_2 = methods[j]

            scores_method_1 = scores_dict[method_1]
            scores_method_2 = scores_dict[method_2]

            # 确保样本数量一致
            if len(scores_method_1) == len(scores_method_2):
                p_value = perform_wilcoxon_test(scores_method_1, scores_method_2)
                p_values.append(p_value)
                method_pairs.append(f"{method_1} vs {method_2}")
            else:
                print(f"警告: {method_1} 和 {method_2} 的样本数量不一致，跳过该对比。")

    # 对所有p值进行多重比较校正
    reject, pvals_corrected, _, _ = adjust_p_values(p_values, method='bonferroni')

    # 打印最终结果
    print(f"\n=== analysis result ===")
    # print(f"Method Pair        | P-value | Bonferroni Corrected P-value | Significance")
    print(f"Method Pair        | P-value | Significance")
    print("=" * 80)

    # 输出每个方法对比的p值
    for i, method_pair in enumerate(method_pairs):
        p = p_values[i]
        p_corrected = pvals_corrected[i]
        significance = "Significant (p < 0.05)" if reject[i] else "Not Significant (p >= 0.05)"
        print(f"{method_pair:<18} |  {p:.4f},  conclusion: {significance}")
        print(f"{method_pair:<18} | conclusion: {significance}")

    # 输出读取了多少Dice值
    total_dice = len(df)
    print(f"\n一共读取了 {total_dice} 个 Dice 值。")


def main():
    """
    主函数，执行所有数据集的分析，并打印结果。
    """
    input_csv = r'C:\Users\18846\Desktop\data1.csv'  # 输入文件路径

    # 分析并打印结果
    analyze_dataset_and_print_results(input_csv)


if __name__ == "__main__":
    main()

