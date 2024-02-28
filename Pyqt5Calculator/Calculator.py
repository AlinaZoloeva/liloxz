import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()

        self.vbox = QVBoxLayout(self) # Выстраивает виджеты по вертикали
        self.hbox_input = QHBoxLayout() # Выстраивает виджеты по горизонтали
        self.hbox_digits1 = QHBoxLayout()
        self.hbox_digits2 = QHBoxLayout()
        self.hbox_digits3 = QHBoxLayout()
        self.hbox_digits4 = QHBoxLayout()
        self.hbox_oper = QHBoxLayout()
        self.hbox_result = QHBoxLayout()
        self.hbox_clear = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input) # К главной вертикальной оси vbox привязываем горизонтальные оси выравнивания
        self.vbox.addLayout(self.hbox_digits1)
        self.vbox.addLayout(self.hbox_digits2)
        self.vbox.addLayout(self.hbox_digits3)
        self.vbox.addLayout(self.hbox_digits4)
        self.vbox.addLayout(self.hbox_oper)
        self.vbox.addLayout(self.hbox_result)
        self.vbox.addLayout(self.hbox_clear)



        # Привязка виджетов к осям осуществляется
        # с помощью функции addWidget()

        self.input = QLineEdit(self) #QLineEdit - виджет, разрешащий вводить и редактировать одну строку текста
        self.hbox_input.addWidget(self.input) # Привязка виджета к оси

        self.b_0 = QPushButton("0", self)
        self.hbox_digits1.addWidget(self.b_0)

        self.b_1 = QPushButton("1", self) # Создание кнопки
        self.hbox_digits2.addWidget(self.b_1) # Привязка виджета к оси

        self.b_2 = QPushButton("2", self)
        self.hbox_digits2.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_digits2.addWidget(self.b_3)

        self.b_4 = QPushButton("4", self)
        self.hbox_digits3.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_digits3.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_digits3.addWidget(self.b_6)

        self.b_7 = QPushButton("7", self)
        self.hbox_digits4.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_digits4.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_digits4.addWidget(self.b_9)


        self.b_plus = QPushButton("+", self)
        self.hbox_oper.addWidget(self.b_plus)

        self.b_min = QPushButton("-", self)
        self.hbox_oper.addWidget(self.b_min)

        self.b_mult = QPushButton("*", self)
        self.hbox_oper.addWidget(self.b_mult)

        self.b_div = QPushButton("/", self)
        self.hbox_oper.addWidget(self.b_div)

        self.b_point = QPushButton(".", self)
        self.hbox_oper.addWidget(self.b_point)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_clear = QPushButton("clear", self)
        self.hbox_clear.addWidget(self.b_clear)



        # Создаем события, отвечающие за реакции на нажатия по кнопкам
        # Lambda-функция позволяет нам определять функцию анонимно.

        # Функция connect(<имя_функции/метода>), вызывает
        # функцию/метод с именем указанным в аргументах.
        # В указанную функцию/метод нельзя передавать аргументы.
        # Для решения этой проблемы используем lambda-функции.


        # если вводим вместо первого числа операцию
        if (self.b_plus.clicked.connect(lambda: self._operation("+")) == -1):
            self.input.setText("")

        if (self.b_min.clicked.connect(lambda: self._minus("-")) == -1):
            self.input.setText("")

        if (self.b_mult.clicked.connect(lambda: self._operation("*")) == -1):
            self.input.setText("")

        if (self.b_div.clicked.connect(lambda: self._operation("/")) == -1):
            self.input.setText("")

        self.b_result.clicked.connect(self._result)

        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_point.clicked.connect(lambda: self._button("."))
        self.b_clear.clicked.connect(lambda: self._clear())


    def _clear(self):
        self.input.setText("") # очищаем линию ввода

    def _button(self, param):
        line = self.input.text() # получаем уже существующую строку в линии ввода

        if (param == "." and line.count(".") != 0):
            return -1
        self.input.setText(line + param) # конкатенируем ее с аргументом param и устанавливаем как как отображаемый в линии ввода текст


    def _operation(self, op):
        try:
            if self.input.text().isdigit(): # проверка на правильность ввода 1 числа (чтобы не было букв)
                pass
            else:
                try:
                    float(self.input.text())
                    pass
                except ValueError:
                    self.input.setText("Is not a number")
                    return -1

            self.num_1 = float(self.input.text()) # запоминаем первое число в  типе данных

        except:
            return -1

        self.op = op # запоминаем в качестве операции аргумент op
        self.input.setText("") # очищаем линию ввода

    def _minus(self, op):
        if (self.input.text() == "-"): # два минуса подряд
            return 0

        if (self.input.text() == "" ): # если минус в качестве минуса для отрицательного числа
            self.input.setText("-")
            return 1

        if self.input.text().isdigit():  # проверка на правильность ввода 1 числа (чтобы не было букв)
            pass
        else:
            try:
                float(self.input.text())
                pass
            except ValueError:
                self.input.setText("Is not a number")
                return -1

        if (self.input.text() != ""): # если минус - операция
            self.num_1 = float(self.input.text())  # запоминаем первое число в  типе данных

            self.op = op  # запоминаем в качестве операции аргумент op

            self.input.setText("")  # очищаем линию ввода

    def _result(self):
        if (hasattr(self, 'num_1') == False): # =
            return -1

        if (self.input.text() == ""): # 5*=
            return -1

        if self.input.text().isdigit():  # проверка на правильность ввода числа (чтобы не было букв)
            pass
        else:
            try:
                float(self.input.text())
                pass
            except ValueError:
                self.input.setText("Is not a number")
                return -1

        self.num_2 = float(self.input.text()) # запоминаем второе число типе данных

        if (self.num_2 == ""):
            return -1


        if (self.op == "/" and self.num_2 == 0.0):
            self.input.setText("Cannot divide by zero")
            return -1

        if self.op == "+": # производим вычисление в зависимости от операции и устанавливаем его в качестве текста в линию ввода
            self.res = self.num_1 + self.num_2
            if (self.res - int(self.res) == 0):
                self.input.setText(str(int(self.res)))
            else:
                self.input.setText(str(self.res))

        if self.op == "-": # производим вычисление в зависимости от операции и устанавливаем его в качестве текста в линию ввода
            self.res = self.num_1 - self.num_2
            if (self.res - int(self.res) == 0):
                self.input.setText(str(int(self.res)))
            else:
                self.input.setText(str(self.res))

        if self.op == "*": # производим вычисление в зависимости от операции и устанавливаем его в качестве текста в линию ввода
            self.res = self.num_1 * self.num_2
            if (self.res - int(self.res) == 0): # является ли число целым или дробным и как при это выводить
                self.input.setText(str(int(self.res)))
            else:
                self.input.setText(str(self.res))

        if self.op == "/": # производим вычисление в зависимости от операции и устанавливаем его в качестве текста в линию ввода
            self.res = self.num_1 / self.num_2

            if (self.res - int(self.res) == 0):
                self.input.setText(str(int(self.res)))
            else:
                self.input.setText(str(self.res))







app = QApplication(sys.argv)

win = Calculator()
win.setWindowTitle('Calculator')
win.setWindowIcon(QtGui.QIcon('calc.png'))
win.show()

sys.exit(app.exec_())


