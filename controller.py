import model as m

pb = m.Phonebook()
#Вывод телефонного справочника
# 2 то как оно реализовано в классе Record
def show_phonebook():
    records = pb.get_records()
    return records


# #     #Проивзольный вывод
#def show_phonebook(pb):
#     name = record.name
#     tephone = record.telephone
#     comment = record.comment
#     print(f"{name} {tephone} {comment}")

# 2. Добавление записи
def input_contact():
    name = input('Ведите ФИО контакта: ') #можно удалить запись внутри инпута, если для интерфейса она не нужна
    phone = input('Ведите телефон контакта: ')
    comment = input('Ведите комментарий: ')
    record = m.Record(name, phone, comment)
    m.Phonebook.add_record(record)
    m.Phonebook.dump()

#3. Удаление записи
def delеtе_contact(index):
    pb.__delitem__(index)

#4. Поиск по индексу
def search_contact_by_id(index):
    return show_phonebook()[index]
    
#6. Поиск посимвольно
def search_contact(string):
    records = m.Phonebook.get_records()
    result = None
    for index, record in enumerate(records):
        name = record.name
        telphone = record.telephone
        comment = record.comment
        if name == string or telphone == string or comment == string:
            result = record
            break
    if result is not None:
        print(result)

#7. Редактирование
def change_contact(index, name, telephone, comment):
    record_new = m.Record(name, telephone, comment)
    m.Phonebook.get_records()[index] = record_new
    m.Phonebook.dump()
