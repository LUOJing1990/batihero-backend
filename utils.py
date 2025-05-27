from models import Session, WindowType, PriceEntry

def ceil_to_grid(val, grid):
    """
    向上取整到 grid 列表中最小且 >= val 的值
    """
    for g in sorted(grid):
        if val <= g:
            return g
    raise ValueError("🛑 输入尺寸超出最大范围")

def get_price(type_name, largeur, hauteur, color='blanc', vitrage='4-20-4', ob=False):

    session = Session()

    # 查找窗户类型
    wt = session.query(WindowType).filter_by(name=type_name).first()
    if not wt:
        session.close()
        return {
            'matched_width': None,
            'matched_height': None,
            'base_price': None,
            'error': f"❌ 类型未找到：{type_name}"
        }

    # 获取该类型下所有标准尺寸
    # 获取该类型下所有标准尺寸
    all_entries = session.query(PriceEntry).filter_by(window_type=wt).all()

    width_list = sorted(set([e.width for e in all_entries if e.width is not None]))
    height_list = sorted(set([e.height for e in all_entries if e.height is not None]))

    print("📏 所有宽度：", width_list)
    print("📏 所有高度：", height_list)

    try:
        matched_w = ceil_to_grid(largeur, width_list)
        matched_h = ceil_to_grid(hauteur, height_list)
    except ValueError as e:
        session.close()
        return {
            'matched_width': None,
            'matched_height': None,
            'base_price': None,
            'error': str(e)
        }

    # 查找匹配价格
    entry = session.query(PriceEntry).filter_by(
        window_type=wt,
        width=matched_w,
        height=matched_h
    ).first()

    session.close()

    if entry and entry.price is not None:
        base_price = float(entry.price)

        # 加颜色比例价格
        color_ratio = {
            'blanc': 1.0,
            'blanc_color': 1.3,  # 单面带色 +30%
            'couleur': 1.4       # 双面带色 +40%
        }
        ratio = color_ratio.get(color, 1.0)
        color_price = round(base_price * ratio, 2)

        # 计算面积（单位 m²）
        area_m2 = (largeur * hauteur) / 1_000_000

        # 按面积计算玻璃加价
        vitrage_rate = {
            '4-20-4': 0,
            '4-20-4g200': 20,
            '44.2-16-4': 120,
            '44.2opale-16-4': 160
        }
        vitrage_price = round(area_m2 * vitrage_rate.get(vitrage, 0), 2)

        # 总价 = 颜色基础价 + vitrage 附加价
        # 总价 = 颜色基础价 + vitrage 附加价
        total_price = color_price + vitrage_price

        # OB 系统加价（每扇窗 +100€）
        # OB 系统加价：统一加价 100€
        ob_price = 0

        # 禁止加 OB 的窗型
        forbidden_types = [
            'FIXED_WINDOW_PRICING',
            'COULISSANT_PVC',
            'PORTE_1_VANTAIL_PVC',
            'OB_1_VANTAIL_PVC',
            'SOUFFLET_PVC',
            'PORTE_FENETRE_ALL'  # 如果你有这个值的话
        ]

        # 特定窗型除以几，决定单扇宽度（用于判定尺寸限制）
        split_width_rule = {
            'OF_2_VANTAUX_PVC': 2,
            'OF_3_VANTAUX_PVC': 3,
            'OF_4_VANTAUX_PVC': 4,
            'PORTE_FENETRE_2_PVC': 2,
            'PORTE_FENETRE_2_FIXE_1_PVC': 3,
            'PORTE_FENETRE_2_FIXE_2_PVC': 4
        }
        # 默认除以 1（即不除）
        split_factor = split_width_rule.get(type_name, 1)

        if ob:
            if type_name not in forbidden_types:
                width_per_leaf = largeur / split_factor
                if width_per_leaf <= 800 and hauteur <= 2000:
                    ob_price = 100  # ✅ 固定加价一次
                else:
                    print("❌ OB 尺寸超限，未计入加价")
            else:
                print("❌ 类型禁止加 OB，未计入加价")

        total_price += ob_price
        total_price = round(total_price, 2)  # 最后再四舍五入


        return {
            'matched_width': matched_w,
            'matched_height': matched_h,
            'base_price': total_price,
            'color': color,
            'vitrage': vitrage,
            'ob': ob
        }


    else:
        return {
            'matched_width': matched_w,
            'matched_height': matched_h,
            'base_price': None,
            'error': f"❌ 没有找到尺寸 {matched_w}×{matched_h} 的价格"
        }

