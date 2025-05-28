import pandas as pd
from models import Base, engine, Session, WindowType, PriceEntry

def load_excel_to_db(filename, type_name):
    # 读取 Excel
    df = pd.read_excel(f'data/{filename}', index_col=0, engine='openpyxl')
    Base.metadata.create_all(engine)
    session = Session()

    # 获取或创建窗户类型
    wt = session.query(WindowType).filter_by(name=type_name).first()
    if not wt:
        wt = WindowType(name=type_name)
        session.add(wt)
        session.commit()

    # 导入所有尺寸-价格数据
    for h, row in df.iterrows():
        for w, price in row.items():
            if pd.isna(price):
                continue
            w_i, h_i, p_f = int(w), int(h), float(price)
            exists = session.query(PriceEntry).filter_by(
                window_type=wt, width=w_i, height=h_i
            ).first()
            if not exists:
                entry = PriceEntry(
                    window_type=wt, width=w_i, height=h_i, price=p_f
                )
                session.add(entry)

    session.commit()
    session.close()
    print(f"✅ 导入完成：{type_name} ← {filename}")

if __name__ == '__main__':
    files = [
        ("fixed_window_pricing.xlsx", "FIXED_WINDOW_PRICING"),
        ("coulissant_pvc.xlsx", "COULISSANT_PVC"),
        ("OB 1 VANTAIL_pvc.xlsx", "OB_1_VANTAIL_PVC"),
        ("OF 1 VANTAIL_pvc.xlsx", "OF_1_VANTAIL_PVC"),
        ("OF 2 VANTAUX_pvc.xlsx", "OF_2_VANTAUX_PVC"),
        ("OF 3 VANTAUX_pvc.xlsx", "OF_3_VANTAUX_PVC"),
        ("OF 4 VANTAUX_pvc.xlsx", "OF_4_VANTAUX_PVC"),
        ("OF2_1 FIXE_pvc.xlsx", "OF2_1_FIXE_PVC"),
        ("OF2_2 FIXES_pvc.xlsx", "OF2_2_FIXES_PVC"),
        ("Porte 1 vantail_pvc.xlsx", "PORTE_1_VANTAIL_PVC"),
        ("PORTE FENETRE 1_pvc.xlsx", "PORTE_FENETRE_1_PVC"),
        ("PORTE FENETRE 2_fixe 1_pvc.xlsx", "PORTE_FENETRE_2_FIXE_1_PVC"),
        ("PORTE FENETRE 2_fixe 2_pvc.xlsx", "PORTE_FENETRE_2_FIXE_2_PVC"),
        ("PORTE FENETRE 2_pvc.xlsx", "PORTE_FENETRE_2_PVC"),
        ("PORTE FENETRE 3_pvc.xlsx", "PORTE_FENETRE_3_PVC"),
        ("PORTE FENETRE 4_pvc.xlsx", "PORTE_FENETRE_4_PVC"),
        ("soufflet_pvc.xlsx", "SOUFFLET_PVC"),
    ]
    
def import_excel_to_db():
    files = [
        ("fixed_window_pricing.xlsx", "FIXED_WINDOW_PRICING"),
        ("coulissant_pvc.xlsx", "COULISSANT_PVC"),
        ("OB 1 VANTAIL_pvc.xlsx", "OB_1_VANTAIL_PVC"),
        ("OF 1 VANTAIL_pvc.xlsx", "OF_1_VANTAIL_PVC"),
        ("OF 2 VANTAUX_pvc.xlsx", "OF_2_VANTAUX_PVC"),
        ("OF 3 VANTAUX_pvc.xlsx", "OF_3_VANTAUX_PVC"),
        ("OF 4 VANTAUX_pvc.xlsx", "OF_4_VANTAUX_PVC"),
        ("OF2_1 FIXE_pvc.xlsx", "OF2_1_FIXE_PVC"),
        ("OF2_2 FIXES_pvc.xlsx", "OF2_2_FIXES_PVC"),
        ("Porte 1 vantail_pvc.xlsx", "PORTE_1_VANTAIL_PVC"),
        ("PORTE FENETRE 1_pvc.xlsx", "PORTE_FENETRE_1_PVC"),
        ("PORTE FENETRE 2_fixe 1_pvc.xlsx", "PORTE_FENETRE_2_FIXE_1_PVC"),
        ("PORTE FENETRE 2_fixe 2_pvc.xlsx", "PORTE_FENETRE_2_FIXE_2_PVC"),
        ("PORTE FENETRE 2_pvc.xlsx", "PORTE_FENETRE_2_PVC"),
        ("PORTE FENETRE 3_pvc.xlsx", "PORTE_FENETRE_3_PVC"),
        ("PORTE FENETRE 4_pvc.xlsx", "PORTE_FENETRE_4_PVC"),
        ("soufflet_pvc.xlsx", "SOUFFLET_PVC"),
    ]

    for file, type_name in files:
        load_excel_to_db(file, type_name)

    
    for file, type_name in files:
        load_excel_to_db(file, type_name)

