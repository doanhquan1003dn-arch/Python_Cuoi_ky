import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.ticker import FuncFormatter

data_goc = np.loadtxt('Cau_2_Co_Phieu/data/abc-2.csv', delimiter=',')
tham_chieu = np.r_[data_goc[0, 6], data_goc[:-1, 6]]
gia_san, gia_tran = tham_chieu * 0.9, tham_chieu * 1.1
data = np.clip(data_goc, gia_san[:, None], gia_tran[:, None])

dong_cua = data[:, 6]
thap_nhat, cao_nhat = data.min(axis=1), data.max(axis=1)
trung_binh = data.mean(axis=1)
q1, trung_vi, q3 = np.percentile(data, [25, 50, 75], axis=1)

XANH_DUONG, TIM, VANG = '#00cfff', '#ae78ef', '#ffe329'
DO, XANH_LA = '#f12b36', '#20c938'


def mau_nen(i):
    if np.isclose(dong_cua[i], gia_san[i], atol=0.5, rtol=0):
        return XANH_DUONG
    if np.isclose(dong_cua[i], gia_tran[i], atol=0.5, rtol=0):
        return TIM
    if np.isclose(dong_cua[i], tham_chieu[i], atol=0.5, rtol=0):
        return VANG
    return DO if dong_cua[i] < tham_chieu[i] else XANH_LA


def ve_bieu_do(a=1, b=365):
    fig, ax1 = plt.subplots(figsize=(14, 5.5))
    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')

    for i in range(a - 1, b):
        x, color = i + 1, mau_nen(i)
        ax1.plot([x, x], [thap_nhat[i], cao_nhat[i]], color=color, lw=1)
        ax1.add_patch(Rectangle((x - 0.34, q1[i]), 0.68,
                                max(q3[i] - q1[i], 0.01), color=color))
        ax1.plot([x - 0.25, x + 0.25], [trung_vi[i], trung_vi[i]],
                 color='white', lw=0.7)

    ymin, ymax = thap_nhat[a - 1:b].min(), cao_nhat[a - 1:b].max()
    padding = max((ymax - ymin) * 0.08, 100)
    ax1.set(xlim=(a - 1, b + 1), ylim=(ymin - padding, ymax + padding),
            title='Biểu đồ nến thống kê giá trong phiên (1 phiên = 1 nến)',
            xlabel='Phiên giao dịch', ylabel='Giá (VND)')
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f'{value:,.0f}'))
    ax1.tick_params(colors='white')
    ax1.title.set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.grid(alpha=0.16, linestyle=':')
    for spine in ax1.spines.values():
        spine.set_color('white')

    ax1.legend(handles=[Patch(color=XANH_LA, label='Tăng'),
                        Patch(color=DO, label='Giảm'),
                        Patch(color=VANG, label='Tham chiếu'),
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

    khoang = widgets.IntRangeSlider(value=[1, len(data)], min=1, max=len(data),
                                    description='Phiên:', continuous_update=False)
    nut = widgets.Button(description='Cập nhật', button_style='primary')
    dat_lai = widgets.Button(description='Đặt lại')
    thong_ke = widgets.HTML()
    bang = widgets.Output(layout=widgets.Layout(max_height='350px', overflow='auto'))
    do_thi = widgets.Output()

    def cap_nhat(_=None):
        a, b = khoang.value
        sl = slice(a - 1, b)
        thong_ke.value = (f'<b>Thấp nhất:</b> {thap_nhat[sl].min():,.2f} &nbsp; '
                          f'<b>Cao nhất:</b> {cao_nhat[sl].max():,.2f} &nbsp; '
                          f'<b>Trung bình:</b> {trung_binh[sl].mean():,.2f}')

        with bang:
            bang.clear_output(wait=True)
            print('Phiên | Tham chiếu | Thấp nhất | Q1 | Trung vị | Q3 | Cao nhất | Đóng cửa')
            for i in range(a - 1, b):
                print(f'{i + 1:5d} | {tham_chieu[i]:10.2f} | {thap_nhat[i]:9.2f} | '
                      f'{q1[i]:.2f} | {trung_vi[i]:9.2f} | {q3[i]:.2f} | '
                      f'{cao_nhat[i]:8.2f} | {dong_cua[i]:9.2f}')

        with do_thi:
            do_thi.clear_output(wait=True)
            display(ve_bieu_do(a, b))
            plt.close()

    def khoi_phuc(_):
        khoang.value = (1, len(data))
        cap_nhat()

    nut.on_click(cap_nhat)
    dat_lai.on_click(khoi_phuc)
    print('MODULE 1: BỘ LỌC VÀ NÚT ĐIỀU KHIỂN')
    display(widgets.HBox([khoang, nut, dat_lai]), thong_ke)
    print('MODULE 2: BẢNG SỐ LIỆU')
    display(bang)
    print('MODULE 3: BIỂU ĐỒ NẾN THỐNG KÊ')
    display(do_thi)
    cap_nhat()


if __name__ == '__main__':
    try:
        get_ipython()
    except NameError:
        fig = ve_bieu_do(1, len(data))
        fig.savefig('Cau_2_Co_Phieu/output/co_phieu.png', dpi=160, facecolor=fig.get_facecolor())
        plt.close(fig)
        print(f'Da ve {len(data)} nen, moi phien tuong ung mot nen.')
    else:
        dashboard()
