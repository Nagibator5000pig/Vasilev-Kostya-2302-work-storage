class MediaPlayer:
    def open(self, file):
        self.filename = file

    def play(self):
        print(f'Воспроизведение {self.filename}')

media1 = MediaPlayer()
media1.open('media1.mp3')
media2 = MediaPlayer()
media2.open('media2.mp3')

media1.play()
media2.play()

