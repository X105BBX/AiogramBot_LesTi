import openpyxl
import pandas
import re
import os
import datetime

letter = [i for i in 'ABCDEFGHIJKLMN']
book_file_name = os.path.join('documents', 'Расписание уроков.xlsx')
wbook = openpyxl.open(book_file_name)
ws = wbook.active


def WithoutTeacher(full_name, next_day):
    teachers = []
    lessons = []
    for sheet_teacher in ws['D49':'D75']:
        for cell_teacher in sheet_teacher:
            teachers.append(cell_teacher.value)

    for sheet_day in ws['B2':'B38']:
        for cell_day in sheet_day:
            if cell_day.value == f'{next_day}':
                position_day_1 = letter[cell_day.column + 1] + str(cell_day.row + 1)
                position_day_2 = letter[cell_day.column + 8] + str(cell_day.row + 8)

    cabinet = ""
    for teacher in teachers:
        if re.search(f'{full_name}', f'{teacher}'):
            for sheet_cabinet in ws['D49':'D75']:
                for cell_cabinet in sheet_cabinet:
                    if cell_cabinet.value == teacher:
                        cabinet = letter[cell_cabinet.column] + str(cell_cabinet.row)

    if len(cabinet) > 0:
        wc = get_week_sheet()
        cabinet_number = wc[f'{cabinet}']
        for sheet in wc[f'{position_day_1}':f'{position_day_2}']:
            for cell in sheet:
                if re.search(cabinet_number.value[1:4], f'{cell.value}'):
                    pos_les = letter[cell.column - 1] + str(cell.row)
                    lessons.append([cell.column, cell.value])
                    wc[f'{pos_les}'] = ''
        wbook.save(book_file_name)
    return True


def get_week_sheet():
    week_num = str(datetime.date.today().isocalendar()[1])
    if week_num in wbook.sheetnames:
        return wbook[week_num]
    else:
        target = wbook.copy_worksheet(ws)
        target.title = week_num
        return target

def LesPlan(is_class, is_next_day):
    les_plan = ['']
    wc = get_week_sheet()
    for sheet_days in wc['B2':'B38']:
        for cell_days in sheet_days:
            if cell_days.value == f'{is_next_day}':
                position_class_1 = letter[cell_days.column + 1] + str(cell_days.row)
                position_class_2 = letter[cell_days.column + 11] + str(cell_days.row)
                for sheet_class in wc[f'{position_class_1}':f'{position_class_2}']:
                    for cell_class in sheet_class:
                        if cell_class.value == f'{is_class}':
                            position_plan_1 = letter[cell_class.column - 1] + str(cell_class.row + 1)
                            position_plan_2 = letter[cell_class.column - 1] + str(cell_class.row + 8)
                            for sheet_lesson in wc[f'{position_plan_1}':f'{position_plan_2}']:
                                for cell_lesson in sheet_lesson:
                                    if cell_lesson.value is None:
                                        break
                                    else:
                                        les_plan.append(cell_lesson.value)
                            result = {f'{is_class}': les_plan}
                            df = pandas.DataFrame(result)
                            return df
                    return 'Такого класса не существует'
