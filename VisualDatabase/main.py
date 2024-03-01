import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self) # создает структуру, которую можно заполнять вкладками
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_subject_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="vsdb",
                                     user="postgres",
                                     password="1m7v89c1w",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    ############################TEACHER############################################
    def _create_teacher_tab(self):
        self.teacher_tab = QWidget() # Класс QWidget() создает виджет, который будет являться вкладкой в нашем приложении
        self.tabs.addTab(self.teacher_tab, "Преподаватели") # добавляет в структуру с вкладками новую вкладку с названием "Table".
        self.teacher_gbox = QGroupBox("Преподаватели") # рамка, заголовок вверху и может отображать несколько виджетов внутри.

        self.svboxt = QVBoxLayout()
        self.shboxt1 = QHBoxLayout()
        self.shboxt2 = QHBoxLayout()
        self.svboxt.addLayout(self.shboxt1)
        self.svboxt.addLayout(self.shboxt2)
        self.shboxt1.addWidget(self.teacher_gbox)


        self.teacher_table = QTableWidget() # создает пустую пользовательскую таблицу
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents) # устанавливает возможность изменения размера под размер данных в ячейке

        self.teacher_table.setColumnCount(5) # задает таблице количество колонок
        self.teacher_table.setHorizontalHeaderLabels(["ID", "Full name", "Subject","",""])

        self._update_teacher_table() # заполнение таблицы

        # Делаем вкладки shedule, teacher одного размера
        self.tvbox = QVBoxLayout()
        self.tvbox.addWidget(self.teacher_table)
        self.teacher_gbox.setLayout(self.tvbox)


        self.update_shedule_buttont = QPushButton("Update")
        self.shboxt2.addWidget(self.update_shedule_buttont) # Привязка виджетов к осям
        self.update_shedule_buttont.clicked.connect(self._update_shedule) # обновление таблицы
        self.teacher_tab.setLayout(self.svboxt)

    def _update_teacher_table(self):
        self.conn.rollback() # откат изменений
        self.cursor.execute("SELECT * FROM teacher")
        records = list(self.cursor.fetchall())

        self.teacher_table.setRowCount(len(records) + 1) # задает таблице количество строк

        # для динамической обрабатки изменений в количестве записей.
        for i, r in enumerate(records): # i - номер r - содержимое
            r = list(r)
            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            # заполняем ячейки записи
            # id
            self.teacher_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0]))) # setItem - записывает в ячейку с определенным адресом строковые  данные. QTableWidgetItem - Объект ячейки
            # Имя
            self.teacher_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            # Предмет
            self.teacher_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[2])))

            self.teacher_table.setCellWidget(i, 3, joinButton) # добавляю кнопку 'изменить' в запись
            self.teacher_table.setCellWidget(i, 4, joinButton1)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_teacher(num)) # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_teacher(num)) # была нажата кнопка удалить
        joinButton2 = QPushButton("Добавить")

        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_teacher(num))
        self.teacher_table.setCellWidget(len(records), 0, joinButton2) # добавляю кнопку добавить после всех записей в первый столбец
        self.teacher_table.resizeRowsToContents() # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _del_day_from_teacher(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM teacher WHERE id = %s", (self.teacher_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.teacher_table.setRowCount(0)
        self._update_teacher_table()

    def _add_day_from_teacher(self, rowNum):
        self.cursor.execute("insert into teacher (teacher_name, subject_name) VALUES ('None', 'None')")
        self.conn.commit()
        self.teacher_table.setRowCount(0)
        self._update_teacher_table()

    def _change_day_from_teacher(self, rowNum):
        row = list()
        # нахожу строку, которую необходимо изменить, и записываю ее в качестве списка в row
        for column in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, column).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE teacher SET teacher_name = %s, subject_name = %s WHERE id = %s",
                                (row[1], row[2], row[0]))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", "Fill all")
            self.conn.rollback()
        self.teacher_table.setRowCount(0)
        self._update_teacher_table()

    ################################################################

    ############################SUBJECT############################################
    def _create_subject_tab(self):
        self.subject_tab = QWidget() # Класс QWidget() создает виджет, который будет являться вкладкой в нашем приложении
        self.tabs.addTab(self.subject_tab, "Предметы") # добавляет в структуру с вкладками новую вкладку с названием "Table".
        self.subject_gbox = QGroupBox("Предметы") # рамка, заголовок вверху и может отображать несколько виджетов внутри.

        self.svboxt = QVBoxLayout()
        self.shboxt1 = QHBoxLayout()
        self.shboxt2 = QHBoxLayout() # виджеты размещаются по вертикали сверху вниз
        self.svboxt.addLayout(self.shboxt1)
        self.svboxt.addLayout(self.shboxt2) # привязываем горизонтальные оси выравнивания
        self.shboxt1.addWidget(self.subject_gbox)

        self.subject_table = QTableWidget() # создает пустую пользовательскую таблицу
        self.subject_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents) # устанавливает возможность изменения размера под размер данных в ячейке

        self.subject_table.setColumnCount(5) # задает таблице количество колонок
        self.subject_table.setHorizontalHeaderLabels(["ID", "Subject", "","",""]) # задает колонкам подписи.


        self._update_subject_table() # заполнение таблицы

        # Делаем вкладки shedule, teacher, subject одного размера
        self.tvbox = QVBoxLayout() # виджеты размещаются по вертикали сверху вниз
        self.tvbox.addWidget(self.subject_table) # Привязка виджетов к осям
        self.subject_gbox.setLayout(self.tvbox)

        self.update_shedule_buttont = QPushButton("Update")
        self.shboxt2.addWidget(self.update_shedule_buttont) # Привязка виджетов к осям
        self.update_shedule_buttont.clicked.connect(self._update_shedule) # обновление таблицы
        self.subject_tab.setLayout(self.svboxt)

    def _update_subject_table(self):
        self.conn.rollback() # откат изменений
        self.cursor.execute("SELECT * FROM subject")
        records = list(self.cursor.fetchall())

        self.subject_table.setRowCount(len(records) + 1) # задает таблице количество строк

        # для динамической обрабатки изменений в количестве записей.
        for i, r in enumerate(records): # i - номер r - содержимое
            r = list(r)
            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            # заполняем ячейки записи
            # id
            self.subject_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0]))) # setItem - записывает в ячейку с определенным адресом строковые  данные. QTableWidgetItem - Объект ячейки

            self.subject_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))

            self.subject_table.setCellWidget(i, 3, joinButton) # добавляю кнопку изменить в запись
            self.subject_table.setCellWidget(i, 4, joinButton1)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_subject(num)) # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_subject(num)) # была нажата кнопка удалить
        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_subject(num))
        self.subject_table.setCellWidget(len(records), 0, joinButton2) # добавляю кнопку добавить после всех записей в первый столбец
        self.subject_table.resizeRowsToContents() # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _del_day_from_subject(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        try:
            self.cursor.execute("DELETE FROM subject WHERE id = %s", (self.subject_table.item(rowNum, 0).text(),))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Fill all")
            self.conn.rollback()
        self.subject_table.setRowCount(0)
        self._update_subject_table()

    def _add_day_from_subject(self, rowNum):
        self.cursor.execute("insert into subject (subject_name) VALUES ('None')")
        self.conn.commit()
        self.subject_table.setRowCount(0)
        self._update_subject_table()

    def _change_day_from_subject(self, rowNum):
        row = list()
        # нахожу строку, которую необходимо изменить, и записываю ее в качестве списка в row
        for column in range(self.subject_table.columnCount()):
            try:
                row.append(self.subject_table.item(rowNum, column).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("UPDATE subject SET subject_name = %s WHERE id = %s", (row[1], row[0]))
            self.conn.commit()
        except Exception as e:
            QMessageBox.about(self, "Error", "Fill all")
            self.conn.rollback()
        self.subject_table.setRowCount(0)
        self._update_subject_table()

    ################################################################

    ######################SHEDULE############################################
    def _create_shedule_tab(self):
            self.shedule_tab = QWidget()
            self.tabs.addTab(self.shedule_tab, "Расписание")

            self.monday_gbox = QGroupBox("Понедельник")
            self.tuesday_gbox = QGroupBox("Вторник")
            self.wednesday_gbox = QGroupBox("Среда")
            self.thursday_gbox = QGroupBox("Четверг")
            self.friday_gbox = QGroupBox("Пятница")
            self.saturday_gbox = QGroupBox("Суббота")

            self.svbox = QVBoxLayout()
            self.shbox1 = QHBoxLayout()
            self.shbox2 = QHBoxLayout()
            self.shbox3 = QHBoxLayout()

            self.svbox.addLayout(self.shbox1)
            self.svbox.addLayout(self.shbox2)
            self.svbox.addLayout(self.shbox3)

            self.shbox1.addWidget(self.monday_gbox)
            self.shbox1.addWidget(self.tuesday_gbox)
            self.shbox1.addWidget(self.wednesday_gbox)
            self.shbox3.addWidget(self.thursday_gbox)
            self.shbox3.addWidget(self.friday_gbox)
            self.shbox3.addWidget(self.saturday_gbox)

            self._create_monday_table()
            self._create_tuesday_table()
            self._create_wednesday_table()
            self._create_thursday_table()
            self._create_friday_table()
            self._create_saturday_table()

            self.update_shedule_button = QPushButton("Update")
            self.shbox2.addWidget(self.update_shedule_button)
            self.update_shedule_button.clicked.connect(self._update_shedule)
            self.shedule_tab.setLayout(self.svbox)

    #######################MONDAY##############################################
    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(7)
        self.monday_table.setHorizontalHeaderLabels(["Id", "Предмет", "Аудитория", "Время", "","",""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)


    def _update_monday_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM timetable WHERE day='Понедельник'")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        if records == []:
            return 0;

        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.monday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[5])))

            self.monday_table.setCellWidget(i, 5, joinButton)  # добавляю кнопку изменить в запись
            self.monday_table.setCellWidget(i, 6, joinButton1)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_monday(num))  # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_monday(num))  # была нажата кнопка удалить

        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_monday(num))

        self.monday_table.setCellWidget(len(records), 0,
                                         joinButton2)  # добавляю кнопку добавить после всех записей в первый столбец
        self.monday_table.resizeRowsToContents()  # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.


    def _change_day_from_monday(self, rowNum):
        print()
        row = list()

        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)

        try:
            self.cursor.execute("UPDATE timetable SET subject_name = %s, room_numb = %s, start_time = %s, teacher_name = %s   WHERE id = %s", (row[1],row[2],row[3], row[4], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
        self.monday_table.setRowCount(0)
        self._update_monday_table()



    def _del_day_from_monday(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM timetable WHERE id = %s", (self.monday_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.monday_table.setRowCount(0)
        self._update_monday_table()

    def _add_day_from_monday(self, rowNum):
        self.cursor.execute("insert into timetable (day, subject_name) VALUES ('Понедельник', 'None')")
        self.conn.commit()
        self.monday_table.setRowCount(0)
        self._update_monday_table()
    #####################################################################################


    #######################TUESDAY##############################################
    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(7)
        self.tuesday_table.setHorizontalHeaderLabels(["Id", "Предмет", "Аудитория", "Время", "", "",""])

        self._update_tuesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _update_tuesday_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM timetable WHERE day='Вторник'")
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records) + 1)

        if records == []:
            return 0;

        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            self.tuesday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.tuesday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.tuesday_table.setItem(i, 4,
                                       QTableWidgetItem(str(r[5])))

            self.tuesday_table.setCellWidget(i, 5, joinButton)  # добавляю кнопку изменить в запись
            self.tuesday_table.setCellWidget(i, 6, joinButton1)

            joinButton.clicked.connect(
                lambda ch, num=i: self._change_day_from_tuesday(num))  # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_tuesday(num))  # была нажата кнопка удалить
        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_tuesday(num))
        self.tuesday_table.setCellWidget(len(records), 0,
                                        joinButton2)  # добавляю кнопку добавить после всех записей в первый столбец
        self.tuesday_table.resizeRowsToContents()  # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _change_day_from_tuesday(self, rowNum):
        print()
        row = list()

        for i in range(self.tuesday_table.columnCount()):
            try:
                row.append(self.tuesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)

        try:
            self.cursor.execute("UPDATE timetable SET subject_name = %s, room_numb = %s, start_time = %s, teacher_name = %s   WHERE id = %s", (row[1],row[2],row[3], row[4], row[0]))

            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
        self.tuesday_table.setRowCount(0)
        self._update_tuesday_table()

    def _del_day_from_tuesday(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM timetable WHERE id = %s", (self.tuesday_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.tuesday_table.setRowCount(0)
        self._update_tuesday_table()

    def _add_day_from_tuesday(self, rowNum):
        self.cursor.execute("insert into timetable (day, subject_name) VALUES ('Вторник', 'None')")
        self.conn.commit()
        self.tuesday_table.setRowCount(0)
        self._update_tuesday_table()

    #####################################################################################


    #######################WEDNESDAY##############################################
    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(7)
        self.wednesday_table.setHorizontalHeaderLabels(["Id", "Предмет", "Аудитория", "Время", "", "",""])

        self._update_wednesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _update_wednesday_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM timetable WHERE day='Среда'")
        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records) + 1)

        if records == []:
            return 0;

        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            self.wednesday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.wednesday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.wednesday_table.setItem(i, 4,
                                         QTableWidgetItem(str(r[5])))

            self.wednesday_table.setCellWidget(i, 5, joinButton)  # добавляю кнопку изменить в запись
            self.wednesday_table.setCellWidget(i, 6, joinButton1)

            joinButton.clicked.connect(
                lambda ch, num=i: self._change_day_from_wednesday(num))  # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_wednesday(num))  # была нажата кнопка удалить
        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_wednesday(num))
        self.wednesday_table.setCellWidget(len(records), 0,
                                        joinButton2)  # добавляю кнопку добавить после всех записей в первый столбец
        self.wednesday_table.resizeRowsToContents()  # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _change_day_from_wednesday(self, rowNum):
        print()
        row = list()

        for i in range(self.wednesday_table.columnCount()):
            try:
                row.append(self.wednesday_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)

        try:
            self.cursor.execute("UPDATE timetable SET subject_name = %s, room_numb = %s, start_time = %s, teacher_name = %s   WHERE id = %s", (row[1],row[2],row[3], row[4], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
        self.wednesday_table.setRowCount(0)
        self._update_wednesday_table()

    def _del_day_from_wednesday(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM timetable WHERE id = %s", (self.wednesday_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.wednesday_table.setRowCount(0)
        self._update_wednesday_table()

    def _add_day_from_wednesday(self, rowNum):
        self.cursor.execute("insert into timetable (day, subject_name) VALUES ('Среда', 'None')")
        self.conn.commit()
        self.wednesday_table.setRowCount(0)
        self._update_wednesday_table()

    #####################################################################################




    #######################THURSDAY##############################################
    def _create_thursday_table(self):
        self.thursday_table = QTableWidget()
        self.thursday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.thursday_table.setColumnCount(7)
        self.thursday_table.setHorizontalHeaderLabels(["Id", "Предмет", "Аудитория", "Время", "", "", "",""])

        self._update_thursday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.thursday_table)
        self.thursday_gbox.setLayout(self.mvbox)

    def _update_thursday_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM timetable WHERE day='Четверг'")
        records = list(self.cursor.fetchall())

        self.thursday_table.setRowCount(len(records) + 1)

        if records == []:
            return 0;

        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            self.thursday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.thursday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.thursday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.thursday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))

            self.thursday_table.setItem(i, 4,
                                        QTableWidgetItem(str(r[5])))

            self.thursday_table.setCellWidget(i, 5, joinButton)  # добавляю кнопку изменить в запись
            self.thursday_table.setCellWidget(i, 6, joinButton1)

            joinButton.clicked.connect(
                lambda ch, num=i: self._change_day_from_thursday(num))  # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_thursday(num))  # была нажата кнопка удалить
        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_thursday(num))
        self.thursday_table.setCellWidget(len(records), 0,
                                        joinButton2)  # добавляю кнопку добавить после всех записей в первый столбец
        self.thursday_table.resizeRowsToContents()  # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _change_day_from_thursday(self, rowNum):
        print()
        row = list()

        for i in range(self.thursday_table.columnCount()):
            try:
                row.append(self.thursday_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)

        try:
            self.cursor.execute("UPDATE timetable SET subject_name = %s, room_numb = %s, start_time = %s, teacher_name = %s   WHERE id = %s", (row[1],row[2],row[3], row[4], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
        self.thursday_table.setRowCount(0)
        self._update_thursday_table()

    def _del_day_from_thursday(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM timetable WHERE id = %s", (self.thursday_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.thursday_table.setRowCount(0)
        self._update_thursday_table()

    def _add_day_from_thursday(self, rowNum):
        self.cursor.execute("insert into timetable (day, subject_name) VALUES ('Четверг', 'None')")
        self.conn.commit()
        self.thursday_table.setRowCount(0)
        self._update_thursday_table()

    #####################################################################################

    #######################FRIDAY##############################################
    def _create_friday_table(self):
        self.friday_table = QTableWidget()
        self.friday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.friday_table.setColumnCount(7)
        self.friday_table.setHorizontalHeaderLabels(["Id", "Предмет", "Аудитория", "Время", "", "",""])

        self._update_friday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.friday_table)
        self.friday_gbox.setLayout(self.mvbox)

    def _update_friday_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM timetable WHERE day='Пятница'")
        records = list(self.cursor.fetchall())

        self.friday_table.setRowCount(len(records) + 1)

        if records == []:
            return 0;

        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            self.friday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.friday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.friday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.friday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.friday_table.setItem(i, 4,
                                      QTableWidgetItem(str(r[5])))

            self.friday_table.setCellWidget(i, 5, joinButton)  # добавляю кнопку изменить в запись
            self.friday_table.setCellWidget(i, 6, joinButton1)

            joinButton.clicked.connect(
                lambda ch, num=i: self._change_day_from_friday(num))  # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_friday(num))  # была нажата кнопка удалить
        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_friday(num))
        self.friday_table.setCellWidget(len(records), 0,
                                        joinButton2)  # добавляю кнопку добавить после всех записей в первый столбец
        self.friday_table.resizeRowsToContents()  # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _change_day_from_friday(self, rowNum):
        print()
        row = list()

        for i in range(self.friday_table.columnCount()):
            try:
                row.append(self.friday_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)

        try:
            self.cursor.execute("UPDATE timetable SET subject_name = %s, room_numb = %s, start_time = %s, teacher_name = %s   WHERE id = %s", (row[1],row[2],row[3], row[4], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
        self.friday_table.setRowCount(0)
        self._update_friday_table()

    def _del_day_from_friday(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM timetable WHERE id = %s", (self.friday_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.friday_table.setRowCount(0)
        self._update_friday_table()

    def _add_day_from_friday(self, rowNum):
        self.cursor.execute("insert into timetable (day, subject_name) VALUES ('Пятница', 'None')")
        self.conn.commit()
        self.friday_table.setRowCount(0)
        self._update_friday_table()

    #####################################################################################

    #######################SATURDAY##############################################
    def _create_saturday_table(self):
        self.saturday_table = QTableWidget()
        self.saturday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.saturday_table.setColumnCount(7)
        self.saturday_table.setHorizontalHeaderLabels(["Id", "Предмет", "Аудитория", "Время", "", "",""])

        self._update_saturday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.saturday_table)
        self.saturday_gbox.setLayout(self.mvbox)

    def _update_saturday_table(self):
        self.conn.rollback()
        self.cursor.execute("SELECT * FROM timetable WHERE day='Суббота'")
        records = list(self.cursor.fetchall())

        self.saturday_table.setRowCount(len(records) + 1)

        if records == []:
            return 0;

        for i, r in enumerate(records):
            r = list(r)

            joinButton = QPushButton("Изменить")
            joinButton1 = QPushButton("Удалить")

            self.saturday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.saturday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[2])))
            self.saturday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[3])))
            self.saturday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[4])))
            self.saturday_table.setItem(i, 4,
                                        QTableWidgetItem(str(r[5])))

            self.saturday_table.setCellWidget(i, 5, joinButton)  # добавляю кнопку изменить в запись
            self.saturday_table.setCellWidget(i, 6, joinButton1)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_saturday(num))  # была нажата кнопка изменить
            joinButton1.clicked.connect(lambda ch, num=i: self._del_day_from_saturday(num))  # была нажата кнопка удалить

        joinButton2 = QPushButton("Добавить")
        joinButton2.clicked.connect(lambda ch, num=i: self._add_day_from_saturday(num))
        self.saturday_table.setCellWidget(len(records), 0,
                                        joinButton2)  # добавляю кнопку добавить после всех записей в первый столбец
        self.saturday_table.resizeRowsToContents()  # автоматически адаптирует размеры ячеек таблицы под размер данных внутри этой ячейки.

    def _change_day_from_saturday(self, rowNum):
        print()
        row = list()

        for i in range(self.saturday_table.columnCount()):
            try:
                row.append(self.saturday_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)

        try:
            self.cursor.execute("UPDATE timetable SET subject_name = %s, room_numb = %s, start_time = %s, teacher_name = %s   WHERE id = %s", (row[1],row[2],row[3], row[4], row[0]))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")
        self.saturday_table.setRowCount(0)
        self._update_saturday_table()

    def _del_day_from_saturday(self, rowNum):
        # нахожу id удаляемой записи (строка rowNum, столбец 0) и удаляю запись из базы данных
        self.cursor.execute("DELETE FROM timetable WHERE id = %s", (self.saturday_table.item(rowNum, 0).text(),))
        self.conn.commit()
        self.saturday_table.setRowCount(0)
        self._update_saturday_table()

    def _add_day_from_saturday(self, rowNum):
        self.cursor.execute("insert into timetable (day, subject_name) VALUES ('Суббота', 'None')")
        self.conn.commit()
        self.saturday_table.setRowCount(0)
        self._update_saturday_table()

    #####################################################################################


    def _update_shedule(self):
        self.monday_table.setRowCount(0)
        self._update_monday_table()

        self.tuesday_table.setRowCount(0)
        self._update_tuesday_table()

        self.wednesday_table.setRowCount(0)
        self._update_wednesday_table()

        self.thursday_table.setRowCount(0)
        self._update_thursday_table()

        self.friday_table.setRowCount(0)
        self._update_friday_table()

        self.saturday_table.setRowCount(0)
        self._update_saturday_table()

        self.teacher_table.setRowCount(0)
        self._update_teacher_table()

        self.subject_table.setRowCount(0)
        self._update_subject_table()



app = QApplication(sys.argv)
win = MainWindow()
win.showMaximized()
sys.exit(app.exec_())