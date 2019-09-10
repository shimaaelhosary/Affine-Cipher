import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QErrorMessage
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator


class AffineCipher(QDialog):
    alphabetic = []

    def __init__(self):
        super(AffineCipher, self).__init__()
        loadUi('Affine_Cipher.ui', self)
        self.setWindowTitle('AFFine Cipher')
        self.onlyInt1 = QIntValidator()
        self.l2.setValidator(self.onlyInt1)
        self.onlyInt2 = QIntValidator()
        self.l3.setValidator(self.onlyInt2)
        self.p3.clicked.connect(self.push_button2_clicked)
        self.p4.clicked.connect(self.push_button3_clicked)
        #self.alphabetic = self.l1.text()
        self.p1.clicked.connect(self.plain_text_encryption)
        self.p2.clicked.connect(self.cipher_text_decryption)

    @pyqtSlot()
    def push_button2_clicked(self):
        uppercase = list(map(chr, range(ord('A'), ord('Z') + 1)))
        uppercase = "".join(uppercase)
        return self.l1.setText(uppercase)

    def push_button3_clicked(self):
        lowercase = list(map(chr, range(ord('a'), ord('z') + 1)))
        lowercase = "".join(lowercase)
        return self.l1.setText(lowercase)

    def gcd(self, a, b):
        if b == 0:
            return a
        else:
            return self.gcd(b, a % b)

    def plain_text_encryption(self):
        mul_key = int(self.l2.text())
        add_key = int(self.l3.text())
        plain_text = self.l4.text()
        alphabetic = self.l1.text()
        alphabetic = self.remove_duplicates(alphabetic)
        n = len(alphabetic)
        alphabetic = [i for i in alphabetic]
        cipher_text = []
        for i in plain_text:
            if i not in alphabetic:
                error_dialog = QErrorMessage()
                error_dialog.showMessage(i + ' not in alphabets')
                error_dialog.exec_()
            else:
                digit = ((alphabetic.index(i) * mul_key) + add_key) % n
                cIdx = digit % n
                cipher_text.append(alphabetic[cIdx])
        cipher_text = ''.join(cipher_text)
        return self.output.setText(cipher_text)

    def cipher_text_decryption(self):
        mul_key = int(self.l2.text())
        sub_key = int(self.l3.text())
        cipher_text = self.l4.text()
        alphabetic = self.l1.text()
        alphabetic = self.remove_duplicates(alphabetic)
        n = len(alphabetic)
        alphabetic = [i for i in alphabetic]
        plain_text = []
        if self.gcd(mul_key, len(alphabetic)) == 1:
            for i in cipher_text:
                # digit = self.inverse(mul_key, n, n) * (alphabetic.index(i)-sub_key) % n
                inverse = self.multiplicative_inverse(mul_key, len(alphabetic))
                digit = (inverse * (alphabetic.index(i) - sub_key)) % n
                if digit < 0:
                    digit += len(alphabetic)
                plain_text.append(alphabetic[digit])

            plain_text = ''.join(plain_text)
            return self.output.setText(plain_text)
        else:
            error_dialog_2 = QErrorMessage()
            error_dialog_2.showMessage('The multiplication factor '
                                       'and the number of alphabets'
                                       ' are not relatively prime')
            error_dialog_2.exec_()



    def multiplicative_inverse(self, a, alpha):
        result = 1
        for i in range(1, alpha):
            if (a * i) % alpha == 1:
                result = i
        return result

    def remove_duplicates(self, text):
        if isinstance(text, str):
            new_string = text[0]
            for char in text[1:]:
                if char not in new_string:
                    new_string += char
            return new_string


app = QApplication(sys.argv)
widget = AffineCipher()
widget.show()
sys.exit(app.exec_())







