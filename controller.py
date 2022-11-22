import model as m

pb = m.Phonebook()
# 1. Вывод телефонного справочника
def show_phonebook():
    records = pb.get_records()
    pb.dump()
    return records

# 2. Добавление записи
def input_contact(name, telephone, comment):
    record = m.Record(name, telephone, comment)
    pb.add_record(record)
    pb.dump()

#3. Удаление записи
def delеtе_contact(index):
    pb.__delitem__(index)
    pb.dump()

#4. Поиск по индексу
def search_contact_by_id(index):
    return show_phonebook()[index]
    
# 6. Поиск посимвольно
def search_contact(string):
    records = pb.get_records()
    result = list()
    for index, record in enumerate(records):
        name = record.name
        telphone = record.telephone
        if string.lower() in name.lower() or string in telphone:
            result.append(record)
    return result

#7. Редактирование
def change_contact(index, name, telephone, comment):
    record_new = m.Record(name, telephone, comment)
    pb[index] = record_new
    pb.dump()
