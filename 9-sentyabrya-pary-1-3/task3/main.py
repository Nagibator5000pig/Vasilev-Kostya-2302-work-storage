class MediaPlayer:
    def open(self, file):
        self.filename = file

    def play(self):
        print(f"Воспроизведение {self.filename}")

media1 = MediaPlayer()
media2 = MediaPlayer()
media1.open("A4_Kids.mp3")
media2.open("Гимн.mp3")
media1.play()
media2.play()