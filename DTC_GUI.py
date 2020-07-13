#!/usr/bin/python

import sysy
from PyQt5.QWidgets import QApplication, QWidget

class DTCGUI(self):
    def main(self):
        app = QApplication(sys.argv)

        w = QWidget()
        w.resize(300, 300)
        w.setWindowTitle("Dark Time Calculator")
        w.show()

        sys.exit(app.exec_())

    if __name__ == '__main__':
        main()        

    
