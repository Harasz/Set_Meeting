# Copyright 2017 Jakub Sydor
#
#   Author: Jakub Sydor
#   Contact: sydorjakub@gmail.com
#   Name: SetMeeting
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
#    Niniejszy program jest wolnym oprogramowaniem; możesz go
#    rozprowadzać dalej i/lub modyfikować na warunkach Powszechnej
#    Licencji Publicznej GNU, wydanej przez Fundację Wolnego
#    Oprogramowania - według wersji 3 tej Licencji lub (według twojego
#    wyboru) którejś z późniejszych wersji.
#
#    Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on
#    użyteczny - jednak BEZ JAKIEJKOLWIEK GWARANCJI, nawet domyślnej
#    gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH
#    ZASTOSOWAŃ. W celu uzyskania bliższych informacji sięgnij do     Powszechnej Licencji Publicznej GNU.
#
#    Z pewnością wraz z niniejszym programem otrzymałeś też egzemplarz
#    Powszechnej Licencji Publicznej GNU (GNU General Public License);
#    jeśli nie - zobacz <http://www.gnu.org/licenses/>.

# Importowanie potrzebnych bibliotek
from random import shuffle
import itertools


class GenerateFinalFrame(object):

    """Zestawianie graczy i generowanie wstępnych rozkładów."""

    matched = []
    y = 725

    def __init__(self, data):
        self.data = data
        self.match()
        self.decay()

    def match(self):
        self.matched = list(itertools.combinations(self.data, 2))
        shuffle(self.matched)

    def decay(self):
        from reportlab.pdfgen import canvas
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.pagesizes import letter

        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

        file = canvas.Canvas("Rozpiska_sptokań.pdf", pagesize=letter)

        count = int(input("Ile spotkań zaplanowano? "))
        print("Rozpoczynam generowanie spotkań", end="...")

        per_meet = int(len(self.matched)/count)
        if per_meet == 0:
            per_meet = 1

        file.setFont('Arial', 22)
        file.drawCentredString(letter[0] / 2.0, 750, "Rozpiska spotkań kółka szachowego")
        file.setFont('Arial', 10)
        file.drawCentredString(letter[0] / 2.0, 735, "Opiekun: Rafał Kamiński")

        for meet in range(count):
            self.y -= 30

            if self.y <= 40:
                file.showPage()
                self.y = 750

            file.setFont('Arial', 12)
            file.drawString(50, self.y, "Spotkanie numer: {}".format(meet+1))
            self.y -= 20
            for day in range(per_meet):

                if self.y <= 40:
                    file.showPage()
                    self.y = 750

                if self.matched:
                    file.setFont('Arial', 10)
                    file.drawString(100, self.y, "{number}. {first} - {second}".format(number=day+1,
                                                                                       first=self.matched[0][0],
                                                                                       second=self.matched[0][1]))
                    self.y -= 10
                    self.matched.pop(0)
                else:
                    break


        if self.matched:
            self.y -= 20

            if self.y <= 40:
                file.showPage()
                self.y = 750

            file.setFont('Arial', 12)
            file.drawString(50, self.y, "Mecze do samodzielnego rozdania:")
            for rest in self.matched:
                self.y -= 20
                if self.y <= 40:
                    file.showPage()
                    self.y = 750
                file.setFont('Arial', 10)
                file.drawString(100, self.y, "{first} - {second}".format(first=rest[0],
                                                                         second=rest[1]))

        file.setFont('Arial', 6)
        self.y -= 50

        if self.y <= 40:
            file.showPage()
            self.y = 750

        file.drawString(350, self.y, "Wygenerowane przez 'SetMeeting' by Jakub Sydor")
        print("Gotowe!")
        print("Zakończono generowanie rozkładu spotkań")
        try:
            file.save()
        except PermissionError:
            print("Nie można zapisać rozpiski do pliku."
                  "Upewnij się, że możesz tworzyć nowe pliki, oraz że plik istnieje i nikt go nie używa.")
            exit(4)



class ReadUsersFile(object):

    """Czytanie listy i wczytywanie uczestników"""

    data = []

    def __init__(self):
        print("Wczytywanie pliku z uczestnikami...", end=' ')
        try:
            self.file = open(sys.argv[1], 'r').read()
        except Exception as er:
            print("Błąd!")
            print("Wystąpił błąd podczas ładowania pliku: {}".format(er))
            exit(1)
        print("Gotowe!")
        self.read_file()
        GenerateFinalFrame(self.data)


    def read_file(self):
        user_list = self.file.splitlines()
        for user in user_list:
            meta = user.split(" ")
            if len(meta) is not 3:
                print("Błędny zapis jednego z uczestników.")
                answear = input("Kontynuować generowanie listy? [T/n]")
                if answear.lower() == 'n':
                    exit(2)
                else:
                    continue
            self.data.append("{name} {surname} ({klass})".format(name=meta[0], surname=meta[1], klass=meta[2]))


if __name__ == '__main__':
    import sys
    # Sprawdzanie czy argument został podany
    if len(sys.argv) < 2:
        print("Użycie: {} <list_z_uczestnikami>".format(sys.argv[0]))
        # print("Podaj ścieżkę do listy uczestników jako argument.")
        exit(0)
    else:
        ReadUsersFile()
