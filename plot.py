import matplotlib.pyplot as plt
from sklearn.metrics import auc

# 先前收集的数据
fpr_cot_gpt4 = [0, 0.005, 0.01, 0.02, 0.1, 0.2, 0.5, 1]
tpr_cot_gpt4 = [0, 0.7, 0.85, 0.9, 0.98, 0.99, 0.998, 1]

fpr_cot_gpt35 = [0, 0.005, 0.01, 0.03, 0.1, 0.2, 0.5, 1]
tpr_cot_gpt35 = [0, 0.65, 0.8, 0.9, 0.97, 0.99, 0.997, 1]

fpr_phishpedia = [0, 0.01, 0.03, 0.05, 0.1, 0.2, 0.5, 1]
tpr_phishpedia = [0, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 0.98]

fpr_visualphishnet = [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1]
tpr_visualphishnet = [0, 0.4, 0.5, 0.65, 0.75, 0.85, 0.9, 0.95]

fpr_chatgpt4 = [0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.5, 1]
tpr_chatgpt4 = [0, 0.4, 0.6, 0.7, 0.8, 0.9, 0.99, 1]

fpr_chatgpt35 = [0, 0.01, 0.03, 0.05, 0.1, 0.2, 0.5, 1]
tpr_chatgpt35 = [0, 0.35, 0.55, 0.65, 0.75, 0.85, 0.95, 1]

# 计算AUC
auc_cot_gpt4 = auc(fpr_cot_gpt4, tpr_cot_gpt4)
auc_cot_gpt35 = auc(fpr_cot_gpt35, tpr_cot_gpt35)
auc_phishpedia = auc(fpr_phishpedia, tpr_phishpedia)
auc_visualphishnet = auc(fpr_visualphishnet, tpr_visualphishnet)
auc_chatgpt4 = auc(fpr_chatgpt4, tpr_chatgpt4)
auc_chatgpt35 = auc(fpr_chatgpt35, tpr_chatgpt35)

# 绘制ROC曲线
plt.figure(figsize=(10, 7))

plt.plot(fpr_cot_gpt4, tpr_cot_gpt4, color='purple', lw=2, linestyle='-', label='ours: Gemini-1.5-pro (AUC = {:.3f})'.format(auc_cot_gpt4))
plt.plot(fpr_cot_gpt35, tpr_cot_gpt35, color='green', lw=2, linestyle='-.', label='ours: Deepseek-v2 (AUC = {:.3f})'.format(auc_cot_gpt35))
plt.plot(fpr_phishpedia, tpr_phishpedia, color='red', lw=2, linestyle=':', label='Phishpedia (AUC = {:.3f})'.format(auc_phishpedia))
# plt.plot(fpr_visualphishnet, tpr_visualphishnet, color='cyan', lw=2, linestyle='-.', label='VisualPhishnet (AUC = {:.3f})'.format(auc_visualphishnet))
plt.plot(fpr_chatgpt4, tpr_chatgpt4, color='blue', lw=2, linestyle='-', label='ChatPhishDetector: Gemini-1.5-pro (AUC = {:.3f})'.format(auc_chatgpt4))
plt.plot(fpr_chatgpt35, tpr_chatgpt35, color='orange', lw=2, linestyle='--', label='ChatPhishDetector: Deepseek-v2 (AUC = {:.3f})'.format(auc_chatgpt35))

# 设置图形属性
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curve Comparison', fontsize=16)
plt.legend(loc="lower right", fontsize=12)
plt.grid(True)
plt.show()