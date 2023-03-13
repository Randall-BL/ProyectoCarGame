"""******************************************************************************
                                   Instituto Tecnológico de Costa Rica
                                         Ingeniería en Computadores
Lenguaje: Python 3.8.5
Profesor: Jason Leiton Jimenez
Autor: Randall Bryan Bolaños López
Versión: 1.0
Fecha Última Modificación: 11 de MAYO 2022
*****************************************************************************"""

import tkinter.messagebox
import json
import time
import os
import vlc
import threading
from threading import Timer
from tkinter import *
from random import randint



"Determinación de variables que se van a utilizar en el codigo"


player = vlc.MediaPlayer("fondo.mp3")
playermusicaJuego= vlc.MediaPlayer("cancionjuego.mp3")
HiloVivo=FALSE
name=[]
Dificultad=0




def musicaInicial():
    "Funcion que permite la reproducción de musica en la pantalla principal"
    global player
    if HiloVivo== False:
        player.play()
        time.sleep(3)
        player.stop()
        return musicaInicial()
    if HiloVivo==True:
        return MusicaJuego()

def HiloInicialMusica():
    "Hilo para que la musica siga repitiendose constantemente"
    hiloFondo = threading.Thread(target=musicaInicial)
    hiloFondo.start()


def MusicaJuego():
    "Funcion de la musica en la pantalla de juego"
    global playermusicaJuego
    playermusicaJuego.play()
    time.sleep(10)
    playermusicaJuego.stop()
    return MusicaJuego()

def HiloJuego():
    "Hilo de la musica en la pantalla de juego y que detiene la musica de la pantalla principal"
    global HiloVivo
    HiloVivo=True
    if HiloVivo==True:
        hiloJuego=threading.Thread(target=musicaInicial)
        hiloJuego.start()



def TiempoEspera(seg):
    t=Timer(seg)
    t.start()

def cargarImg(archivo):
    "Funcion que permite cargar imagenes"
    ruta= os.path.join('archivos', archivo)
    imagen=PhotoImage(file=ruta)
    return imagen


class Game:
    "Clase donde está la mayor parte del juego programado"
    def __init__(self):
        "Creacion de la ventana del juego"
        HiloJuego()
        self.DocuGame()
        self.width, self.height = 600, 592
        self.game = Tk()
        self.game.title('BrickCarGameProyecto')
        self.game.geometry("600x900+590+40")  # Tamaño de ventana
        self.game.resizable(False, False)  # No se cambia el tamaño de la ventana
        self.game.attributes('-topmost', True)  # Ventana siempre al frente

        "Funciones donde se indica las teclas para las cuales va a ocurrir el movimiento del carro"

        self.game.bind('<KeyRelease-a>', lambda event: self.left())
        self.game.bind('<KeyRelease-A>', lambda event: self.left())
        self.game.bind('<KeyRelease-w>', lambda event: self.Arriba())
        self.game.bind('<KeyRelease-W>', lambda event: self.Arriba())
        self.game.bind('<KeyRelease-s>', lambda event: self.abajo())
        self.game.bind('<KeyRelease-S>', lambda event: self.abajo())

        self.game.bind('<KeyRelease-d>', lambda event: self.derecha())
        self.game.bind('<KeyRelease-D>', lambda event: self.derecha())



        "Teclas para cada una de las marchas"
        ###Marchas###
        self.game.bind('<KeyRelease-e>', lambda event: self.Hilo2())
        self.game.bind('<KeyRelease-E>', lambda event: self.Hilo2())
        self.game.bind('<KeyRelease-Q>', lambda event: self.Hilo3())
        self.game.bind('<KeyRelease-q>', lambda event: self.Hilo3())
        self.game.bind('<KeyRelease-r>', lambda event: self.Hilo4())
        self.game.bind('<KeyRelease-R>', lambda event: self.Hilo4())
        self.game.bind('<KeyRelease-f>', lambda event: self.Hilo1())
        self.game.bind('<KeyRelease-F>', lambda event: self.Hilo1())

        "Variables utilizadas en el juego para su funcionamiento"
        self.status = True
        self.player_position = 1
        self.movimientovel = 25
        self.VelocidadNivel=0
        self.car_position = 0
        self.car_y = 0
        self.roca_position = 0
        self.roca_y = 0
        self.score = 0
        self.oleadas = 0
        self.y = 0
        self.NivelActual= 0

        "Creacion de todo lo relacionado con las imagenes y los cuadros del juego"
        self.background_image = cargarImg("wallpaper.png")
        self.background = Label(self.game, image=self.background_image)
        self.player_image = cargarImg("player.png")
        self.player = Label(self.game, image=self.player_image, border='0', relief=FLAT)
        self.car_image = cargarImg("car.png")
        self.car = Label(self.game, image=self.car_image, border='0', relief=FLAT)
        self.roca_image = cargarImg("roca.png")
        self.roca = Label(self.game, image=self.roca_image, bg='Pink', border='0', relief=FLAT)
        self.score_label = Label(self.game, bg='White', text=self.score, font=('Arial', 20))
        self.time = Label(self.game, fg='red', width=20, font=("", "18"))
        self.time.pack()

        "Cracion de la ventana donde va a salir los tops del score"
        self.ventanascore = Toplevel(self.game)
        self.ventanascore.title("Top Scores")
        self.ventanascore.geometry("1200x900+390+40")
        self.ventanascore.resizable(width=NO, height=NO)
        self.C_score = Canvas(self.ventanascore, width=1200, height=900, bg="Pink")
        self.C_score.place(x=0, y=0)
        self.ventanascore.withdraw()

        "creacion de los botones que vana  llevar a reiniciar el juego y los top de scores, de igual forma creacion de la ventana de derrota o victoria"
        self.lose_label = Label(self.game, bg='#FFFFFF')
        self.lose_button = Button(self.game, text='Reiniciar', bg='Pink', activebackground='#FFFFFF', border='0', relief=FLAT, command=self.start)
        self.score_button = Button(self.game, text='Scores', bg='pink', activebackground='#FFFFFF', border='0', relief=FLAT, command=self.ventascore)
        "Creacion de la ventana donde se va a mostrar el username ingresado en la pantalla principal"
        self.Username_label=Label(self.game,bg="pink", text="Usuario: " +str(data.get()), font=("Arial", 20))
        self.Username_label.place (x=50, y=50)
        "creacion de la ventana del nivel actual"
        self.Nivel_label=Label(self.game, bg= "White", text="", font=("Arial", 20))


        self.start()
        self.game.mainloop()
    "se define la funcion para obtener el usuario de la pantalla principal"
    def DocuGame(self):
        help(self.highscore)
        help(self.imprimirscore)
        help(self.cronometro)
        help(self.__init__)
        help(self.start)
        help(self.lose)
        help(self.spawnconstante)
        help(self.spawn)

    def usuario(self):  # funcion que obtiene el usuario y lo garda en una variable
        global data
        self.name = self.data.get()

    "Funcion del cronometro"
    def cronometro(self, h=0, m=0, s=0):#Funcion encargada del cronometro
        if s >= 60:
            s = 0
            m = m + 1
            if m >= 60:# Verificamos si los segundos y los minutos son mayores a 60 y Verificamos si las horas son mayores a 24
                m = 0
                h = h + 1
                if h >= 24:
                    h = 0
        self.time['text'] = str(h) + ":" + str(m) + ":" + str(s)#Muestra el cronometro en pantalla
        self.proceso = self.time.after(1000, self.cronometro, (h), (m), (s + 1))#Inicia cuenta regresiva

    "La funcion donde va a imprimir en una nueva venta, solamente los mejores 7 scores desde un archivo .json"
    def imprimirscore(self):

        with open('puntajes.json') as file:  # abre el doc de puntajes
            scores = json.load(file)
        self.C_score.create_text(self.C_score.winfo_width() / 2, 320,
                         text=str(scores["Nombres"][0]) + " " + str(scores["Scores"][0]), fill="Black",
                         font="Arial")  # crea un texto con el jugador con el punteje mas alto
        self.C_score.create_text(self.C_score.winfo_width() / 2, 350,
                         text=str(scores["Nombres"][1]) + " " + str(scores["Scores"][1]), fill="Black",
                         font="Arial")  # segundo puntaje mas alto
        self.C_score.create_text(self.C_score.winfo_width() / 2, 380,
                         text=str(scores["Nombres"][2]) + " " + str(scores["Scores"][2]), fill="Black",
                         font="Arial")  # tercer puntaje mas alto
        self.C_score.create_text(self.C_score.winfo_width() / 2, 410,
                         text=str(scores["Nombres"][3]) + " " + str(scores["Scores"][3]), fill="Black",
                         font="Arial")  # cuarto mas alto
        self.C_score.create_text(self.C_score.winfo_width() / 2, 440,
                         text=str(scores["Nombres"][4]) + " " + str(scores["Scores"][4]), fill="Black",
                         font="Arial")  # quinto mas alto
        self.C_score.create_text(self.C_score.winfo_width() / 2, 470,
                         text=str(scores["Nombres"][5]) + " " + str(scores["Scores"][5]), fill="Black",
                         font="Arial")  # sexto mas alto
        self.C_score.create_text(self.C_score.winfo_width() / 2, 500,
                         text=str(scores["Nombres"][6]) + " " + str(scores["Scores"][6]), fill="Black",
                         font="Arial")  # setimo mas alto

    "Funcion que va a ser llamada por el boton de scores"
    def ventascore(self):
        self.game.withdraw()
        self.ventanascore.deiconify()
        self.imprimirscore()


    "Inicio del juego con los valores de las variables y la creacion de las ventanas de score, nivel y el fondo"
    def start(self):
        global Dificultad
        self.lose_label.place_forget()
        self.lose_button.place_forget()
        self.score_button.place_forget()
        self.status = True
        self.player_position = 1
        self.car_y = 0
        self.roca_y = 0
        self.score = 0
        self.NivelActual=0
        self.DificultadInicial= Dificultad
        self.DificultadActual=0
        self.VelocidadNivel=0
        self.MarchaActual=1
        self.y = 0
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.player.place(x=171, y=603)
        self.posx=171
        self.posy=603
        self.score_label.place(x=347, y=50, width=113)
        self.Nivel_label.place(x=225, y=50)
        self.spawn('car')
        self.spawn('roca')
        self.cronometro()
        self.spawnconstante()


    "funcion que va a crear la ventana de derrota o victoria, elimina los objetos y al jugador"
    def lose(self):
        self.lose_label.place(x=24, y=200, width=310, height=120)
        self.score_button.place(x=71, y=295, width=100)
        self.lose_button.place(x=171, y=295, width=100)
        self.car.place_forget()
        self.roca.place_forget()
        self.player.place_forget()
        self.status = False
    "Creacion de todo lo relacionado con los obstaculos"

    def evitarColision(self):
        "Funcion que evalua las posiciones de los obstaculos para que no spawneen en la misma coordenada x"
        if self.car_position != self.roca_position:
            return
        else:
            self.car_position = randint(0, 2)
            return self.evitarColision()


    def spawn(self, obstacle):
        "Spawn de los obstaculos, de tal forma que no spawneen en el mismo eje x en el mismo pixel"
        self.y = 0
        if obstacle == 'roca':
            self.roca_y = randint(0, 100) + 10 * self.y
            self.roca_position = randint(0, 2)
            self.roca.place(x=32 + 139 * self.roca_position, y=self.roca_y)
        if obstacle == 'car':
            self.car_y = randint(0, 100) + 10 * self.y
            self.evitarColision()
            self.car.place(x=32 + 139 * self.car_position, y=self.car_y)


    "Funcion recursiva donde va a tomar en cuenta el nivel actual y así cambiar la velocidad de los obstaculos hasta que pierda o gane, junto con la bonificacion de puntuación"
    def spawnconstante(self):
        global Dificultad
        if self.score >= 60:
            self.lose_label.config(text=f'{data.get()} Ganaste\npuntuación: {self.score}.')
            self.highscore()
            self.lose()
        if self.score >=0 and self.score<=4:
            self.NivelActual = 1
            if self.DificultadInicial == 1:
                self.VelocidadNivel=700
            if self.DificultadInicial == 2:
                self.VelocidadNivel=100
            if self.DificultadInicial == 3:
                self.VelocidadNivel=20

        if self.score >=5 and self.score<=19:
            self.NivelActual = 2
            if self.DificultadInicial ==1:
                self.VelocidadNivel=700
            if self.DificultadInicial ==2:
                self.VelocidadNivel=100
            if self.DificultadInicial ==3:
                self.VelocidadNivel=20
        if self.score==6:
            self.score += 2  # Bonus de puntuación por pasar de nivel

        if self.score >=20 and self.score<=35:
            self.NivelActual=3
            if self.DificultadInicial ==1:
                self.VelocidadNivel=700
            if self.DificultadInicial ==2:
                self.VelocidadNivel=100
            if self.DificultadInicial ==3:
                self.VelocidadNivel=20
        if self.score == 20 :
            self.score += 2  # Bonus de puntuación por pasar de nivel

        if self.score >=36:
            self.NivelActual=3.5
            if self.DificultadInicial ==1:
                self.VelocidadNivel=700
            if self.DificultadInicial ==2:
                self.VelocidadNivel=100
            if self.DificultadInicial ==3:
                self.VelocidadNivel=20
        if self.score == 36:
            self.score += 2  # Bonus de puntuación por pasar de nivel

        "recursividad para la creacion constante de los obstaculos en diferentes caminos, " \
        "de tal forma que va a comparar la posicion actual del obstaculo junto con la del jugador, " \
        "para definir una colision, de no ser así, al final de la pista desaparecen los obstaculos y se le suma un punto al score global"
        if self.status:
            self.y += 1
            self.roca_y += self.movimientovel
            self.car_y += self.movimientovel
            self.roca.place_forget()
            self.roca.place(x=32 + 139 * self.roca_position, y=self.roca_y)
            self.car.place_forget()
            self.car.place(x=32 + 139 * self.car_position, y=self.car_y)
            if self.roca_position == self.player_position and 603 >= self.roca_y >= 400 and self.posy<=500:
                self.lose_label.config(text=f'{data.get()} Has perdido\npuntuación: {self.score}.')
                self.highscore()
                self.lose()
            elif self.roca_position == self.player_position and 650 >= self.roca_y >= 500 and self.posy>=500:
                self.lose_label.config(text=f'{data.get()} Has perdido\npuntuación: {self.score}.')
                self.highscore()
                self.lose()
            if self.car_position == self.player_position and 603 >= self.car_y >= 400 and self.posy<=500:
                self.lose_label.config(text=f'{data.get()} has perdido\npuntuación: {self.score}.')
                self.highscore()
                self.lose()
            elif self.car_position == self.player_position and 650 >= self.car_y >= 500 and self.posy>=500:
                self.lose_label.config(text=f'{data.get()} has peridido\npuntuación: {self.score}.')
                self.highscore()
                self.lose()
            if self.roca_y >= self.height:
                self.spawn('roca')
                self.score += 1
            if self.car_y >= self.height:
                self.spawn('car')
                self.score += 1

            self.Nivel_label["text"]= "Nivel: " +str(self.NivelActual)
            self.score_label['text'] = "Score: " +str(self.score)

            self.game.after(self.VelocidadNivel, self.spawnconstante)
    "Funciones de todas las marchas, de tal forma que tienen un tiempo determinado y se va a ir cambiando el valor para poder aumentar su velocidad "
    def marcha1(self):
        if self.MarchaActual==2:
            self.Hilomarcha()
            self.MarchaActual=1
        elif self.MarchaActual==3:
            self.Hilomarcha()
            self.MarchaActual=1
        elif self.MarchaActual==4:
            self.Hilomarcha()
            self.MarchaActual=1
        else:
            self.MarchaActual=1

    def marcha2(self):

        if self.MarchaActual==1:
            self.MarchaActual=2
            self.Hilomarcha()
            time.sleep(3)
            self.MarchaActual=1

        if self.MarchaActual==3:
            self.MarchaActual=2
            self.Hilomarcha()
            time.sleep(3)
            self.MarchaActual=1
        if self.MarchaActual==1:
            self.MarchaActual=2
            self.Hilomarcha()
            time.sleep(3)
            self.MarchaActual=1


    def marcha3(self):
        if self.MarchaActual==1:
            self.MarchaActual=3
            time.sleep(3)
            self.MarchaActual=2
        if self.MarchaActual == 2:
            self.MarchaActual = 3
            time.sleep(3)
            self.MarchaActual = 2
        if self.MarchaActual == 4:
            self.MarchaActual = 3
            time.sleep(3)
            self.MarchaActual = 2

    def marcha4(self):
        if self.MarchaActual==1:
            self.MarchaActual=4
            time.sleep(3)
            self.MarchaActual=3
        if self.MarchaActual == 2:
            self.MarchaActual = 4
            time.sleep(3)
            self.MarchaActual = 3
        if self.MarchaActual == 3:
            self.MarchaActual = 4
            time.sleep(3)
            self.MarchaActual = 3
    "hilo de las marchas para así no detener el juego cuando se hace el cambio de velocidad"
    def musicaMarcha(self):
        marchasound=vlc.MediaPlayer("Marcha.mp3")
        marchasound.play()
    def Hilomarcha(self):
        hilomarchacambio = threading.Thread(target=self.musicaMarcha)
        hilomarchacambio.start()
    def Hilo1(self):
        hiloFondo = threading.Thread(target=self.marcha1)
        hiloFondo.start()
    def Hilo2(self):
        hiloFondo = threading.Thread(target=self.marcha2)
        hiloFondo.start()
    def Hilo3(self):
        hiloFondo = threading.Thread(target=self.marcha3)
        hiloFondo.start()
    def Hilo4(self):
        hiloFondo = threading.Thread(target=self.marcha4)
        hiloFondo.start()




    "Funciones donde se va a mover de posiciones segun que marcha tenga actualmente"
    def Arriba(self):
        if self.MarchaActual==1:
            if self.player_position == 0:
                self.player.place(x=32,y=503)
                self.posx = 32
                self.posy = 503
                self.player_position=0
            elif self.player_position == 1:
                self.player.place(x=171, y=503)
                self.posx = 171
                self.posy = 503
                self.player_position = 1
            elif self.player_position==2:
                self.posx = 310
                self.posy = 503
                self.player.place(x=310, y=503)
                self.player_position = 2
            else:
                return print("limite de pista arriba")
        if self.MarchaActual==2:
            if self.player_position == 0:
                self.player.place(x=32,y=403)
                self.posx = 32
                self.posy = 403
                self.player_position=0
            elif self.player_position == 1:
                self.player.place(x=171, y=403)
                self.posx = 171
                self.posy = 403
                self.player_position = 1
            elif self.player_position==2:
                self.posx = 310
                self.posy = 403
                self.player.place(x=310, y=403)
                self.player_position = 2


        if self.MarchaActual==3:
            if self.player_position == 0:
                self.player.place(x=32,y=303)
                self.posx = 32
                self.posy = 303
                self.player_position=0
            elif self.player_position == 1:
                self.player.place(x=171, y=303)
                self.posx = 171
                self.posy = 303
                self.player_position = 1
            elif self.player_position==2:
                self.posx = 310
                self.posy = 303
                self.player.place(x=310, y=303)
                self.player_position = 2

        if self.MarchaActual==4:
            if self.player_position == 0:
                self.player.place(x=32,y=103)
                self.posx = 32
                self.posy = 103
                self.player_position=0
            elif self.player_position == 1:
                self.player.place(x=171, y=103)
                self.posx = 171
                self.posy = 103
                self.player_position = 1
            elif self.player_position==2:
                self.posx = 310
                self.posy = 103
                self.player.place(x=310, y=103)
                self.player_position = 2

    def abajo(self):
        if self.player_position == 0:
            self.player.place(x=32,y=603)
            self.posx = 32
            self.posy = 603
            self.player_position=0
        if self.player_position == 1:
            self.player.place(x=171, y=603)
            self.posx = 171
            self.posy = 603
            self.player_position = 1
        if self.player_position==2:
            self.player.place(x=310, y=603)
            self.posx = 310
            self.posy = 603
            self.player_position = 2

    def left(self):
        if self.player_position == 0:
            pass
        elif self.player_position == 1 and self.posx==171 and self.posy==503:
                self.player.place(x=32, y=503)
                self.posx=32
                self.posy=503
                self.player_position=0
        elif self.player_position == 1 and self.posx==171 and self.posy==603:
                self.player.place(x=32, y=603)
                self.posx = 32
                self.posy = 603
                self.player_position=0
        elif self.player_position == 2 and self.posx==310 and self.posy==503:
                self.player.place(x=171, y=503)
                self.posx = 171
                self.posy = 503
                self.player_position = 1
        elif self.player_position == 2 and self.posx==310 and self.posy==603:
                self.player.place(x=171, y=603)
                self.posx = 171
                self.posy = 603
                self.player_position = 1
        else:
            return print("Debugeando")

    def derecha(self):
        if self.player_position == 2:
            pass
        elif self.player_position == 0 and self.posx == 32 and self.posy == 503:
            self.player.place(x=171, y=503)
            self.posx = 171
            self.posy = 503
            self.player_position = 1
        elif self.player_position == 1 and self.posx == 171 and self.posy == 503:
            self.player.place(x=310, y=503)
            self.posx = 310
            self.posy = 503
            self.player_position = 2
        elif self.player_position == 0 and self.posx == 32 and self.posy == 603:
            self.player.place(x=171, y=603)
            self.posx = 171
            self.posy = 603
            self.player_position = 1
        elif self.player_position == 1 and self.posx == 171 and self.posy == 603:
            self.player.place(x=310, y=603)
            self.posx = 310
            self.posy = 603
            self.player_position = 2
        else:
            return print("limite de pista derecha")

    "La funcion donde va a comparar los resultados anteriores y el actual para imprimirlo en una nueva venta, solamente los mejores 7 scores desde un archivo .json"
    def highscore(self):  # funcion que comprueba si se deben guardar
        with open('puntajes.json') as file:  # abre el doc
            puntajes = json.load(file)
            name=data.get()

        if self.score > puntajes['Scores'][0]:  # si el puntaje es mayor al mas alto lo guarda y corre todos un espacio sacando al quinto

            puntajes['Scores'] = [self.score] + puntajes['Scores'][:-1]
            puntajes["Nombres"] = [name] + puntajes["Nombres"][:-1]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][0]:  # si es igual no lo guarda
            pass

        elif self.score > puntajes['Scores'][1]:  # si es mayor al segundo deja al primero y corre los demas un espacio

            puntajes['Scores'] = puntajes['Scores'][0:1] + [self.score] + puntajes['Scores'][1:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:1] + [name] + puntajes["Nombres"][1:-1]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][1]:  # si es igual no lo guarda
            pass

        elif self.score > puntajes['Scores'][2]:  # si es mayor al tercero deja el 1 y 2 y corre los demas un espacio

            puntajes['Scores'] = puntajes['Scores'][0:2] + [self.score] + puntajes['Scores'][2:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:2] + [name] + puntajes["Nombres"][2:-1]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][2]:  # si es igual no lo guarda
            pass

        elif self.score > puntajes['Scores'][3]:  # si es mayor al cuarto deja los primeros y corre un espacio

            puntajes['Scores'] = puntajes['Scores'][0:3] + [self.score] + puntajes['Scores'][3:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:3] + [name] + puntajes["Nombres"][3:-1]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][3]:  # si es igual no lo guarda
            pass

        elif self.score > puntajes['Scores'][4]:  # si es mayor al cuarto deja los primeros y corre un espacio

            puntajes['Scores'] = puntajes['Scores'][0:4] + [self.score] + puntajes['Scores'][4:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:4] + [name] + puntajes["Nombres"][4:-1]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][4]:
            pass

        elif self.score > puntajes['Scores'][5]:

            puntajes['Scores'] = puntajes['Scores'][0:5] + [self.score] + puntajes['Scores'][5:-1]
            puntajes["Nombres"] = puntajes["Nombres"][0:5] + [name] + puntajes["Nombres"][5:-1]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][5]:
            pass

        elif self.score > puntajes['Scores'][6]:  # si es mayor al ultimo lo reemplaza

            puntajes['Scores'] = puntajes['Scores'][0:6] + [self.score]
            puntajes["Nombres"] = puntajes["Nombres"][0:6] + [name]
            with open('puntajes.json', 'w') as file:
                json.dump(puntajes, file)
        elif self.score == puntajes['Scores'][6]:  # si es igual no se guarda
            pass








def Atras():#Funcion para la ventana dificultad
    ventanabout.withdraw()



def about():#Funcion para la ventana creditos
    ventanabout.deiconify()

def UsuarioGod():
    global name
    name=data.get()

def Dificultadprin():
    global Dificultad
    Dificultad=1
    ventanaDificultad.destroy()

def Dificultadmedia():
    global Dificultad
    Dificultad=2
    ventanaDificultad.destroy()

def Dificultadavanzada():
    global Dificultad
    Dificultad=3
    ventanaDificultad.destroy()

def Dificultaexperta():
    global Dificultad
    Dificultad=4
    ventanaDificultad.destroy()

def FunDificultad():
    ventanaDificultad.deiconify()

def prejuego():#Funcion encargada en verificar el login y la dificultad, para así poder iniciar el juego
    global Dificultad
    if Dificultad >=1:
        ventana.destroy()
        Game()
    if Dificultad==0:
        tkinter.messagebox.showinfo("Dificultad","Seleccione la dificultad primero")
        return ventana.destroy()

def DocuAutomatica():
    help(musicaInicial)
    help(prejuego)
    help(cargarImg)

ventana=Tk()
ventana.title("Brick Car racing game")
ventana.geometry("1200x900+390+40")
ventana.resizable(width=NO, height=NO)
#Crear imagen de fondo
C_menu=Canvas(ventana, width=1200, height=900, bg='black')
C_menu.place(x=0, y=0)
C_menu.fondo=cargarImg('menu.png')
imgCanvas= C_menu.create_image(0,0, anchor=NW, image= C_menu.fondo)
#Ventana usuario
data=StringVar()
textUsuario= Entry(C_menu,textvariable=data)
textUsuario.place(x=500,y=500)
saveUsuario=Button(C_menu, text= "Guardar Usuario", command=UsuarioGod)
saveUsuario.place (x=550, y=550)



##############Ventana Ayuda##################
ventanabout=Toplevel(ventana)#Ventanda de creditos
ventanabout.title("About")
ventanabout.geometry("1200x900+390+40")
ventanabout.resizable(width= NO, height=NO)
C_about=Canvas(ventanabout,width=1200, height=900,bg="Pink")
C_about.place(x=0, y=0)
C_about.fondo=cargarImg("About.png")
imgAbout=C_about.create_image(0,0, anchor=NW, image=C_about.fondo)
ventanabout.withdraw()

############VentanaDificultad#############
ventanaDificultad=Toplevel(ventana)
ventanaDificultad.title("Seleccione Dificultad")
ventanaDificultad.geometry("1200x900+390+40")
ventanaDificultad.resizable(width=NO,height=NO)
C_dificultad=Canvas(ventanaDificultad,width=1200,height=900, bg="Pink")
C_dificultad.place(x=0,y=0)
ventanaDificultad.withdraw()

selecdificultad=Button(C_menu,width=8,height=4,text="dificultad",command=FunDificultad).place(x=800,y=600)
facil=Button(ventanaDificultad,width=10, height=6,text="Facil",command=Dificultadprin).place(x=200,y=100)
medio=Button(ventanaDificultad,width=10, height=6,text="medio",command=Dificultadmedia).place(x=200,y=200)
dificil=Button(ventanaDificultad,width=10, height=6,text="avanzado",command=Dificultadavanzada).place(x=200,y=300)






PlayAbout=Button(C_menu,width=6,height=2,bg="Pink",text="Crèditos",command=about).place(x=1100, y=800)
Jugar=Button(C_menu, width=6,height=2,bg="Red",text="Empezar",command=lambda:prejuego()).place(x=800,y=500)
PlayAtras=Button(C_about,width=6,height=2,bg="Pink",text="Volver atrás", command=lambda: Atras()).place(x=1100, y=800)








DocuAutomatica()
HiloInicialMusica()
ventana.mainloop()