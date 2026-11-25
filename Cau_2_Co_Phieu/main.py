import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.ticker import FuncFormatter

data_goc = np.loadtxt('Cau_2_Co_Phieu/data/abc-2.csv', delimiter=',')
SO_PHIEN = len(data_goc)

# Phiên đầu tiên dùng giá đóng cửa đầu vào làm mốc; các phiên sau lấy giá đóng cửa phiên trước.
tham_chieu = np.empty(SO_PHIEN)
data = np.empty_like(data_goc)
tham_chieu[0] = data_goc[0, 6]
for i in range(SO_PHIEN):
    if i > 0:
        tham_chieu[i] = data[i - 1, 6]
    gia_san = tham_chieu[i] * 0.90
    gia_tran = tham_chieu[i] * 1.10
    data[i] = np.clip(data_goc[i], gia_san, gia_tran)

dong_cua = data[:, 6]
gia_san = tham_chieu * 0.90
gia_tran = tham_chieu * 1.10
thap_nhat = data.min(axis=1)
cao_nhat = data.max(axis=1)
trung_binh = data.mean(axis=1)
q1, trung_vi, q3 = np.percentile(data, [25, 50, 75], axis=1)

XANH_DUONG = '#00cfff'
TIM = '#ae78ef'
VANG = '#ffe329'
DO = '#f12b36'
XANH_LA = '#20c938'
SAI_SO_SO_SANG = 1e-8


def mau_nen(i):
    close = dong_cua[i]
    if abs(close - gia_san[i]) <= SAI_SO_SO_SANG:
        return XANH_DUONG
    if abs(close - gia_tran[i]) <= SAI_SO_SO_SANG:
        return TIM
    if abs(close - tham_chieu[i]) <= SAI_SO_SO_SANG:
        return VANG
    return DO if close < tham_chieu[i] else XANH_LA


def ve_bieu_do(dau=1, cuoi=SO_PHIEN):
    fig, ax = plt.subplots(figsize=(14, 5.5))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    for i in range(dau - 1, cuoi):
        x = i + 1
        color = mau_nen(i)
        ax.vlines(x, thap_nhat[i], cao_nhat[i], color=color, linewidth=1)
        ax.add_patch(Rectangle((x - 0.34, q1[i]), 0.68,
                               max(q3[i] - q1[i], 0.01), color=color))
        ax.hlines(trung_vi[i], x - 0.25, x + 0.25, color='white', linewidth=0.7)

    low = thap_nhat[dau - 1:cuoi].min()
    high = cao_nhat[dau - 1:cuoi].max()
    padding = max((high - low) * 0.08, 100)
    ax.set(xlim=(dau - 1, cuoi + 1), ylim=(low - padding, high + padding),
           title='Biểu đồ nến thống kê theo phiên (1 phiên = 1 nến)',
           xlabel='Phiên giao dịch', ylabel='Giá trị trong CSV')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:,.0f}'))
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.grid(alpha=0.16, linestyle=':')
    for spine in ax.spines.values():
        spine.set_color('white')

    ax.legend(handles=[Patch(color=XANH_LA, label='Tăng'),
                       Patch(color=DO, label='Giảm'),
                       Patch(color=VANG, label='Giá tham chiếu'),
                       Patch(color=TIM, label='Giá trần'),
                       Patch(color=XANH_DUONG, label='Giá sàn')],
              ncol=5, fontsize=8, loc='upper left')
    fig.text(0.5, 0.02,
             'Thân nến: Q1–Q3 | Đường trắng: trung vị | Râu nến: thấp nhất–cao nhất',
             color='white', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    return fig


def dashboard():
    import ipywidgets as widgets

    khoang = widgets.IntRangeSlider(value=[1, SO_PHIEN], min=1, max=SO_PHIEN,
                                    description='Phiên:', continuous_update=False)
    cap_nhat_nut = widgets.Button(description='Cập nhật', button_style='primary')
    dat_lai_nut = widgets.Button(description='Đặt lại')
    thong_ke = widgets.HTML()
    bang = widgets.Output(layout=widgets.Layout(max_height='350px', overflow='auto'))
    do_thi = widgets.Output()

    def cap_nhat(_=None):
        dau, cuoi = khoang.value
        mien = slice(dau - 1, cuoi)
        thong_ke.value = (
            f'<b>Thấp nhất:</b> {thap_nhat[mien].min():,.2f} &nbsp; '
            f'<b>Cao nhất:</b> {cao_nhat[mien].max():,.2f} &nbsp; '
            f'<b>Trung bình:</b> {trung_binh[mien].mean():,.2f}'
        )

        with bang:
            bang.clear_output(wait=True)
            print('Phiên | Tham chiếu | Thấp nhất | Q1 | Trung vị | Q3 | Cao nhất | Đóng cửa')
            for i in range(dau - 1, cuoi):
                print(f'{i + 1:5d} | {tham_chieu[i]:10.2f} | {thap_nhat[i]:9.2f} | '
                      f'{q1[i]:.2f} | {trung_vi[i]:9.2f} | {q3[i]:.2f} | '
                      f'{cao_nhat[i]:8.2f} | {dong_cua[i]:9.2f}')

        with do_thi:
            do_thi.clear_output(wait=True)
            display(ve_bieu_do(dau, cuoi))
            plt.close()

    def khoi_phuc(_):
        khoang.value = (1, SO_PHIEN)
        cap_nhat()

    cap_nhat_nut.on_click(cap_nhat)
    dat_lai_nut.on_click(khoi_phuc)
    display(widgets.VBox([
        widgets.HTML('<b>Module 1: Bộ lọc và nút điều khiển</b>'),
        widgets.HBox([khoang, cap_nhat_nut, dat_lai_nut]),
        thong_ke,
        widgets.HTML('<b>Module 2: Bảng số liệu</b>'), bang,
        widgets.HTML('<b>Module 3: Biểu đồ nến thống kê</b>'), do_thi
    ]))
    cap_nhat()


if __name__ == '__main__':
    try:
        get_ipython()
    except NameError:
        fig = ve_bieu_do()
        fig.savefig('Cau_2_Co_Phieu/output/co_phieu.png', dpi=160,
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f'Đã vẽ {SO_PHIEN} nến; mỗi dòng tương ứng một phiên.')
    else:
        dashboard()
