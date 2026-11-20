import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data = np.genfromtxt('Cau_3_Hoi_Quy/data/health.csv', delimiter=',', skip_header=1)
tuoi, bmi, chol = data.T

model_tuoi = LinearRegression().fit(tuoi.reshape(-1, 1), chol)
model_bmi = LinearRegression().fit(bmi.reshape(-1, 1), chol)
model_hai_bien = LinearRegression().fit(data[:, :2], chol)


def tinh_bmi(cao_cm, nang_kg):
    return nang_kg / (cao_cm / 100) ** 2


def du_doan(cao_cm, nang_kg, tuoi_nguoi):
    bmi_nguoi = tinh_bmi(cao_cm, nang_kg)
    return float(model_hai_bien.predict([[tuoi_nguoi, bmi_nguoi]])[0])


def widgets():
    import ipywidgets as w
    cao_bmi = w.FloatText(value=165, description='Cao (cm):')
    nang_bmi = w.FloatText(value=60, description='Nặng (kg):')
    cao_chol = w.FloatText(value=165, description='Cao (cm):')
    nang_chol = w.FloatText(value=60, description='Nặng (kg):')
    tuoi_nhap = w.IntText(value=30, description='Tuổi:')
    nut_bmi = w.Button(description='Tính BMI', button_style='info')
    nut_chol = w.Button(description='Dự đoán cholesterol', button_style='primary')
    ket_qua_1 = w.Output()
    ket_qua_2 = w.Output()

    def hien_bmi(_):
        with ket_qua_1:
            ket_qua_1.clear_output()
            if cao_bmi.value <= 0 or nang_bmi.value <= 0:
                print('Chiều cao và cân nặng phải lớn hơn 0.')
            else:
                print(f'BMI = {tinh_bmi(cao_bmi.value, nang_bmi.value):.2f}')

    def hien_chol(_):
        with ket_qua_2:
            ket_qua_2.clear_output()
            if cao_chol.value <= 0 or nang_chol.value <= 0 or tuoi_nhap.value <= 0:
                print('Vui lòng nhập các giá trị lớn hơn 0.')
            else:
                bmi_nguoi = tinh_bmi(cao_chol.value, nang_chol.value)
                print(f'BMI dùng trong mô hình = {bmi_nguoi:.2f}')
                print(f'Cholesterol dự đoán = {du_doan(cao_chol.value, nang_chol.value, tuoi_nhap.value):.2f}')

    nut_bmi.on_click(hien_bmi)
    nut_chol.on_click(hien_chol)
    display(w.VBox([w.HTML('<b>Widget 1: Tính BMI</b>'), cao_bmi, nang_bmi, nut_bmi, ket_qua_1]))
    display(w.VBox([w.HTML('<b>Widget 2: Dự đoán cholesterol</b>'),
                    cao_chol, nang_chol, tuoi_nhap, nut_chol, ket_qua_2]))


def ve_bieu_do():
    fig = plt.figure(figsize=(14, 5.2))
    ax = [fig.add_subplot(131), fig.add_subplot(132),
          fig.add_subplot(133, projection='3d')]
    for a, x, model, ten, xlabel in (
        (ax[0], tuoi, model_tuoi, 'Cholesterol theo tuổi', 'Tuổi'),
        (ax[1], bmi, model_bmi, 'Cholesterol theo BMI', 'BMI')):
        grid = np.linspace(x.min(), x.max(), 100)
        r = np.corrcoef(x, chol)[0, 1]
        a.scatter(x, chol, s=35, alpha=0.8)
        a.plot(grid, model.predict(grid.reshape(-1, 1)), color='#e76f51', lw=2)
        a.set(title=f'{ten}\nr = {r:.3f}; R² = {model.score(x.reshape(-1, 1), chol):.3f}',
              xlabel=xlabel, ylabel='Cholesterol')
        a.grid(alpha=0.2)

    tuoi_grid, bmi_grid = np.meshgrid(
        np.linspace(tuoi.min(), tuoi.max(), 20),
        np.linspace(bmi.min(), bmi.max(), 20))
    mat_phang = model_hai_bien.predict(
        np.column_stack((tuoi_grid.ravel(), bmi_grid.ravel()))
    ).reshape(tuoi_grid.shape)
    ax[2].plot_surface(tuoi_grid, bmi_grid, mat_phang,
                       color='#e76f51', alpha=0.35, edgecolor='none')
    ax[2].scatter(tuoi, bmi, chol, s=38, color='#087f6b', depthshade=False)
    ax[2].set(title=f'Hồi quy hai biến\nR² = {model_hai_bien.score(data[:, :2], chol):.3f}',
              xlabel='Tuổi', ylabel='BMI', zlabel='Cholesterol')
    ax[2].view_init(elev=24, azim=-55)

    he_so = model_hai_bien.coef_
    fig.suptitle('Phân tích hồi quy tuyến tính cholesterol', fontsize=15)
    fig.text(0.5, 0.035,
             f'Cholesterol = {model_hai_bien.intercept_:.3f} + '
             f'{he_so[0]:.3f} × Tuổi + {he_so[1]:.3f} × BMI',
             ha='center', fontsize=11)
    fig.subplots_adjust(left=0.06, right=0.97, bottom=0.17, top=0.82, wspace=0.28)
    fig.savefig('Cau_3_Hoi_Quy/output/hoi_quy.png', dpi=150)
    plt.close(fig)


if __name__ == '__main__':
    print('Ma tran tuong quan (tuoi, BMI, cholesterol):')
    print(np.round(np.corrcoef(data.T), 3))
    for ten, model, x in [('Tuoi', model_tuoi, tuoi.reshape(-1, 1)),
                          ('BMI', model_bmi, bmi.reshape(-1, 1)),
                          ('Tuoi + BMI', model_hai_bien, data[:, :2])]:
        print(f'{ten}: R2 = {model.score(x, chol):.3f}')
    try:
        get_ipython()
    except NameError:
        ve_bieu_do()
        print('Da xuat bieu do hoi quy. Chay bang Jupyter/Colab de mo widget.')
    else:
        widgets()
