import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

gdp = np.genfromtxt('Cau_4_GDP_Lam_Phat/data/vietnam_gdp_growth_1985_2024.csv', delimiter=',', skip_header=1)
lam_phat = np.genfromtxt('Cau_4_GDP_Lam_Phat/data/vietnam_inflation_1996_2024.csv', delimiter=',', skip_header=1)
nam = np.intersect1d(gdp[:, 0], lam_phat[:, 0])
tang_truong = np.array([gdp[gdp[:, 0] == n, 1][0] for n in nam])
lam_phat_chung = np.array([lam_phat[lam_phat[:, 0] == n, 1][0] for n in nam])

sns.set_theme(style='whitegrid')
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(x=nam, y=tang_truong, marker='o', color='#1976d2',
             label='Tăng trưởng GDP', ax=ax1)
sns.lineplot(x=nam, y=lam_phat_chung, marker='o', color='#ef6c42',
             label='Lạm phát', ax=ax1)
ax1.set(title='Tăng trưởng GDP và lạm phát Việt Nam (1996–2024)',
        xlabel='Năm', ylabel='Tỷ lệ (%)')
fig1.tight_layout()
fig1.savefig('Cau_4_GDP_Lam_Phat/output/gdp_lam_phat_theo_nam.png', dpi=160)
plt.close(fig1)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.regplot(x=tang_truong, y=lam_phat_chung, ax=ax2,
            scatter_kws={'alpha': 0.7}, line_kws={'color': '#ef6c42'})
ax2.set(title='Mối liên hệ giữa tăng trưởng GDP và lạm phát',
        xlabel='Tăng trưởng GDP (%)', ylabel='Lạm phát (%)')
fig2.tight_layout()
fig2.savefig('Cau_4_GDP_Lam_Phat/output/quan_he_gdp_lam_phat.png', dpi=160)
plt.close(fig2)

r = np.corrcoef(tang_truong, lam_phat_chung)[0, 1]
print(f'{len(nam)} nam chung, {int(nam[0])}-{int(nam[-1])}; tuong quan Pearson r = {r:.3f}')
print('Lam phat dat dinh vao 2008 va tang cao tro lai vao 2011; nam 2000-2001 co lam phat am.')
print('Tang truong GDP giam manh trong 2020-2021 va phuc hoi vao 2022.')
