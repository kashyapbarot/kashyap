import xlrd

workbook = xlrd.open_workbook("/home/kashyap.barot/Downloads/Sales Order.xls")
worksheet = workbook.sheet_by_index(0)
worksheet.cell_value(1, 0)
order_list = []
sale_dic = {}
for row in range(worksheet.nrows):
    ref = False
    for col in range(0, 4):
        if row == 0:
            continue
        if col == 0:
            if worksheet.cell_value(row, col) in sale_dic:
                ref = worksheet.cell_value(row, col)
                continue
            ref = worksheet.cell_value(row, col)
            sale_dic.update(
                {worksheet.cell_value(row, col): [],
                 f'{ref}_{worksheet.cell_value(row, 1)}': worksheet.cell_value(
                     row, 1),
                 f'{ref}_{worksheet.cell_value(row, 2)}': worksheet.cell_value(
                     row, 2)})
        if col == 3:
            if ref in sale_dic:
                order_line_product = sale_dic.get(ref) or []
                order_line_product.append(
                    worksheet.cell_value(row, col))
                sale_dic.update({ref: order_line_product})
                continue
            sale_dic.update({
                ref: [worksheet.cell_value(row, col)]})
print(sale_dic)
# final_list = []
# l = False
# for k in sale_dic.keys():
#     if '_' in k:
#         final_list.append(k.split('_')[-1])
#
#     if '_' not in k:
#         l = k
#         final_list.append(k)
#         product = sale_dic.get(ref)
#         p = [i for i in product]
#         final_list.append(p)
# print(final_list)
