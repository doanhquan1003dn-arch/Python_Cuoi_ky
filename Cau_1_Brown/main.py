import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

SO_HAT = 3
SO_GIAY = 30
FPS = 6
SO_KHUNG = SO_GIAY * FPS
GIOI_HAN = 5

rng = np.random.default_rng(12)
buoc = rng.normal(0, 0.30, (SO_KHUNG - 1, SO_HAT, 3))
vi_tri = np.zeros((SO_KHUNG, SO_HAT, 3))

for i in range(1, SO_KHUNG):
    vi_tri[i] = vi_tri[i - 1] + buoc[i - 1]
    vi_tri[i] = np.where(vi_tri[i] > GIOI_HAN, 2 * GIOI_HAN - vi_tri[i], vi_tri[i])
    vi_tri[i] = np.where(vi_tri[i] < -GIOI_HAN, -2 * GIOI_HAN - vi_tri[i], vi_tri[i])

fig = plt.figure(figsize=(11, 7.3), facecolor='white')
ax = fig.add_axes([0.04, 0.11, 0.66, 0.80], projection='3d')
ax.set(xlim=(-5, 5), ylim=(-5, 5), zlim=(-5, 5), xlabel='x', ylabel='y', zlabel='z')
ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=24, azim=-62)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
for pane, shade in zip((ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane), (0.78, 0.86, 0.68)):
    pane.set_facecolor((shade, shade, shade, 1))
    pane.set_edgecolor('white')
    pane.fill = True

hinh_chieu = []
for j, ten in enumerate(('xy', 'yz', 'xz')):
    a = fig.add_axes([0.76, 0.73 - j * 0.32, 0.18, 0.22])
    a.set(xlim=(-5, 5), ylim=(-5, 5), title=ten)
    a.set_aspect('equal')
    a.set_xticks([-5, 0, 5])
    a.set_yticks([-5, 0, 5])
    a.grid(alpha=0.35, linestyle=':')
    hinh_chieu.append(a)

mau = ['Blues', 'Reds', 'Greens']
mau_chu = ['navy', 'darkred', 'darkgreen']
nhan = [fig.text(0.08, 0.91, '', color='navy', fontsize=11),
        fig.text(0.08, 0.07, '', color='darkred', fontsize=11),
        fig.text(0.50, 0.07, '', color='darkgreen', fontsize=11)]
nhan_thoi_gian = fig.text(0.50, 0.91, '', ha='right', fontsize=11, color='black')

hat_3d = []
hat_2d = []
for k in range(SO_HAT):
    hat_3d.append(ax.scatter([], [], [], s=36, color=mau_chu[k], depthshade=False))
    hat_2d.append([a.scatter([], [], s=24, color=mau_chu[k])
                   for a in hinh_chieu])

def ve(khung):
    for k in range(SO_HAT):
        duong = vi_tri[:khung + 1, k]
        sac_do = plt.get_cmap(mau[k])(np.linspace(0.25, 0.98, len(duong)))
        hat_3d[k]._offsets3d = (duong[:, 0], duong[:, 1], duong[:, 2])
        hat_3d[k].set_color(sac_do)
        for h, (a, b) in enumerate(((0, 1), (1, 2), (0, 2))):
            hat_2d[k][h].set_offsets(duong[:, [a, b]])
            hat_2d[k][h].set_color(sac_do)
        x, y, z = duong[-1]
        nhan[k].set_text(f'● ({x:.2f}, {y:.2f}, {z:.2f})')
    nhan_thoi_gian.set_text(f'Thời gian: {khung / (SO_KHUNG - 1) * SO_GIAY:.1f} giây')
    return hat_3d + [p for nhom in hat_2d for p in nhom] + nhan + [nhan_thoi_gian]

phim = FuncAnimation(fig, ve, frames=SO_KHUNG, interval=1000 / FPS, blit=False)
phim.save('Cau_1_Brown/output/brownian_30s.mp4', writer=FFMpegWriter(fps=FPS, codec='libx264',
           bitrate=1200, extra_args=['-pix_fmt', 'yuv420p']), dpi=76)
ve(SO_KHUNG - 1)  # Cùng trạng thái cuối của khung hình cuối trong video.
fig.savefig('Cau_1_Brown/output/anh_brown.png', dpi=120)
plt.close(fig)
print('Da xuat video Brown 30 giay. Tat ca cac hat o trong hop:', bool(np.all(np.abs(vi_tri) <= GIOI_HAN)))
