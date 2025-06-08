import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-white')
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch

labels = ['Control', 'BB94', 'SMT', 'DAPT', 'LA', 'PP2']
values_0_24 = [24.80350775, 19.68635506, 29.8564267,  20.29966978, 20.75237095, 22.76304645]
values_0_48 = [31.1369994, 23.23392604, 36.24916948, 21.45373371, 28.95981218, 31.56824106]

palette = dict(zip(labels, sns.color_palette("tab20", n_colors=len(labels))))

x = np.arange(len(labels))  
width = 0.35  

fig, ax = plt.subplots(figsize=(10, 6))

bars1 = ax.bar(x - width/2, values_0_24, width, 
               color=[palette[label] for label in labels], 
               label='0h–24h')

bars2 = ax.bar(x + width/2, values_0_48, width, 
               color=[palette[label] for label in labels], 
               hatch='///', edgecolor='black', 
               label='0h–48h')

ax.set_ylabel('Percentage [%]', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=12)
ax.tick_params(axis='y', labelsize=12)

legend_elements = [
    Patch(facecolor='none', edgecolor='black', label='0h–24h'),
    Patch(facecolor='none', edgecolor='black', hatch='///', label='0h–48h')
]
ax.legend(handles=legend_elements, fontsize=14)

for bar in bars1 + bars2:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(r'./bar_plot_scratch.png', dpi=600)
plt.show()
