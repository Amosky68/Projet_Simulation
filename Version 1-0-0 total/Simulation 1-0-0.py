import arcade
from math import sqrt,acos,sin
from time import time
from random import randint
from random import random
from copy import copy
import csv




class Constante():  # Toute les constantes Sont Ici
    Bordure_x = 1620  # largeur de l'écran en pixel   (1620)
    Bordure_y = 900  # longueur de l'écran en pixel   (900)
    G_Constant = 6.6743 * 10**(-11)  # Constante Gravitationnel de Newton
    Version = "1.0.0" # Version a changer a chaque fois que le programme est poster sur le drive 
    pi = 3.1415926535
    radians = pi / 180




class Gravity():    # class qui s'occupe de toutes les calcul de gravitation

    # distance en metre
    # acceleration en N


    def acceleration(x1,y1,x2,y2,m2,gravity):          # donne l'acceleration qu'a subbit l'objet 

        distance = sqrt((x1-x2)**2 + (y1-y2) **2)
        x_acceleration =  gravity * m2 * (x2 - x1)/ (distance*distance*distance)  # n*n*n est 3X plus rapide que n**3
        y_acceleration =  gravity * m2 * (y2 - y1)/ (distance*distance*distance)
        return x_acceleration , y_acceleration


    def speed(x1,y1,m1,x2,y2,m2,speed_x,speed_y,gravity,delta_time):             # donne la vitesse final de l'objet 

        x_acceleration , y_acceleration = Gravity.acceleration(x1,y1,x2,y2,m2,gravity)
        speed_x += x_acceleration * delta_time 
        speed_y += y_acceleration * delta_time
        return speed_x,speed_y




class Physical_Screen():    # gere le changement de repère (physique a l'écran / écran a physique)

    """ Calcul de l'espace Physique -> Espace Ecrab 

    Xe: Coordonnées debut écran dans l'espace physique
    X : Coordonnées dans l'espace physique
    X': Coordonnées dans l'espace ecran


    Phy->Ecran : X'=(X-Xe)*Zoom
    Ecran->Phy : X=(X'/Zoom + Xe)
    """

    # Calcul les coordonnées dans le repere ecran (depuis les coordonnées dans le repère physique)
    def to_screen(Xe,Ye,X,Y,Zoom):
        return (X-Xe)*Zoom, (Y-Ye)*Zoom

    # Calcul les coordonnées dans le repere Physique (depuis les coordonnées dans le repère écran)
    def to_physic(Xe,Ye,X,Y,Zoom):
        return X/Zoom+Xe,Y/Zoom+Ye

    # Calcul origine de l'écran connaissant les coordonnées physique du milieu et le zoom
    def orgin_from_center_phy(X,Y,Zoom,bordure_x,bordure_y):
        return X-bordure_x/(2*Zoom),Y-bordure_y/(2*Zoom)




class Button():
    def __init__(self,left,right,up,down,instruction = '',screen_condition = str,type = "long",color = (128,128,128),color_on = (0,255,0),color_off = (255,0,0),outline_color=(80,80,80),text_color=(0,0,0),text="",text_size=20,activated=True):
        self.left   = left  # coordonées du boutons
        self.right = right
        self.up   = up
        self.down = down
        self.instruction = instruction  # instruction donnée
        self.screen_condition = screen_condition    # condition a respecter pour qu'il soit afficher a l'écran
        self.activated = activated
        self.text = text
        self.text_size = text_size
        self.color_off = color_off  # pour un objet de type "long" , la couleur quand il est éteint
        self.color_on = color_on    # quand il est activé
        self.outline_color = outline_color
        self.text_color = text_color

        if type == "long" :     # si c'est un bouton de type  ON/OFF :
            self.type = "long"
            if activated == True :
                self.color = self.color_on
            else :
                self.color = self.color_off


        elif type == "short" :   # si c'est un simple bouton : 
            self.type = "short"
            self.color = color



    def active(self,object):
        
        if object.type == "long" :

            if object.activated == True:  # quand on clique dessus , la couleur change et sont état aussi
                object.color = object.color_off
                object.activated = False
            else :
                object.color = object.color_on
                object.activated = True

            return eval(object.instruction) # on renvoie l'instruction 


        elif object.type == "short" :

            return eval(object.instruction) # on renvoie l'instruction 




class Label():
    def __init__(self,left,right,up,down,text="",text_size=15,text_color=(255,255,255),outline_color=(90,90,90),outline_size=10,in_color=(0,0,0),active_color=(125,0,0),screen_condition='True',activated=False,tilt_angle=0,writing_only=False,type=""):

        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.text= text
        self.text_size = text_size
        self.text_color = text_color
        self.outline_size = outline_size
        self.outline_color = outline_color
        self.in_color = in_color
        self.active_color = active_color
        self.screen_condition= screen_condition
        self.activated = activated
        self.tilt_angle = tilt_angle
        self.writing_only = writing_only
        self.type = type


    def on_click(object_list,mouse_x,mouse_y,text):

        pass

        


class Objects():    # création d'un objet 
    def __init__(self,mass,position_x,position_y,speed_x,speed_y,name="",color=(0,192,255),density = 5520,id=0,type='asteroid',texture=arcade.load_texture("C:\Users\Elève\Documents\Amaury\python\Projet Simulation NSI\Version 1-0-0 total\Textures without background\No_textures-removebg-preview.png"),texture_size=0.01) :
        self.mass = mass  # en kg 
        self.density = density # kg/m³
        self.speed_x = speed_x  # en m/s
        self.speed_y = speed_y  # en m/s
        self.color = color 
        self.position_x = position_x  # postition en m 
        self.position_y = position_y  # postition en m 
        self.name = name
        self.radius = (3*mass/(4*Constante.pi*self.density))**(1/3)   # em metres
        self.colision_counter = 0
        self.near_body_id = 0
        self.id = id
        self.acceleration = 0
        self.texture = texture 
        self.texture_size = texture_size
        self.type = type
        self.last_positions = []
        




class MyGame(arcade.Window):    # partie principal du programme , toute les action se passe ici

    def __init__(self, width, height, title):
        super().__init__(Constante.Bordure_x, Constante.Bordure_y , "N-Body-Simulation  " + Constante.Version)

        """ initialisation des variables, listes etc..."""

        #self.set_update_rate(.002)  # définit le fps max a 200
        self.Simulation_speed =  84600  # chaque seconde dans la vie reel , n seconde se seront passer dans la simulation
        self.objects = []   # liste de tout les objets en orbite 


        self.langue = "english" # définit la langue du programme
        # dernier id : 44
        self.vocabulaire = {"français" : ["systeme solaire","vide","100 obj aléatoire","parametre","retour","contrôles","choix de simulation","échap","quitter le programme","espace","pause/play","haut/bas", "augmente/diminue la vitesse",
                                         "crée un nouvel objet / annule","paramètres vidéo","Active/désactive les textures","Active mode cycle","désactive le mode cycle","Active/désactive la version","Active/désactive coordonées","Active/désactive les fps",
                                         "Active/désactive les trajectoires","Active/désactive la visibilité des objets","temps simulé : ","vitesse de simulation : "," Années Lumière","caractéristiques","appuyez sur Entrée","Masse (kg) : ","Densité (kg/m³) : ","Vitesse (m/s): ",
                                         " Type : "," ID  : ","Couleur (r,g,b) : ","Nom : ","Masse : ","Densité : ","Vitesse : ","Accélération : ","Couleur  : ","Nom : ","Rayon : ","ID  : ","Type : ","Langues"], 

                            "english" : ["solar system","empty","100 random obj ","settings","back","controls_setting","simulation choice","escape","exit the game","space","pause/play","up/down","increase/decrease simulation speed ",
                                         "creat a new object / cancel","video settings","enable/disable textures","enable cycle mode","disable cycle mode","enable/disable version","enable/disable coordinates","enable/disable fps",
                                         "enable/disable trajectory","enable/disable visible objects","simulated time : ","simulation speed : "," Light Years","features","Press Enter to create","Mass (kg) : ","Density (kg/m³) : ","Speed (m/s): ",
                                         "Planet type : ","Planet ID  : ","Color (r,g,b) : ","Planet Name : ","Mass : ","Density : ","Speed : ","Acceleration : ","Color  : ","Name : ","Radius : ","ID  : ","Type : ","Languages"]}

        # ajout des objets dans la simulation (temporaire le temps que les fichiers soit mis en place)
        
        #self.objects.append(Objects(7.6*10**22,384000000,0,0,0,density=3340,name="moon"))
         
        self.initialize_objects("solar_system")
        
        #for i in range(50):
        #    mass = random()**2 * 5 + 19
        #    self.objects.append(Objects(10**mass,randint(-10**9,10**9),randint(-10**9,10**9),0,0,color=(randint(0,255),randint(0,255),randint(0,255)),id=i+2,density=random()*10000))
        #for i in range(50):
        #    mass = random()**2 * 6 + 22
        #    self.objects.append(Objects(10**mass,randint(-10**9,10**9),randint(-10**9,10**9),0,0,color=(randint(0,255),randint(0,255),randint(0,255)),id=i+102,density=random()*10000,type='exoplanet'))

    
        #self.recalculate_colision_counters(.005)

        self.size = 1


        # variable de position et de zoom de la caméra (centre de l'écran)
        self.screen_x = 0   # position x de la camera 
        self.screen_y = 0   # position y de la camera
        self.mouse_pos_x = 0    # position x de la souris
        self.mouse_pos_y = 0    # position y de la souris
        self.zoom = .0000005  # zoom de la caméra    (.00004 = 12742 km sur 500 pixel) soit (zoom de 1 = 500 m )


        # variable pour le clavier
        self.up = False
        self.down = False

        self.initialize_buttons()
        

        #self.boutons.append(Button(1100,1300,Constante.Bordure_y-50,Constante.Bordure_y-150,'self.boutton_texture()','(self.new_planet_statu == "caracteristique")',type="short",color=(30,90,90),text="Textures",text_size=20,outline_color=(125,125,125)))

        self.initialize_labels()



        # variable pour le suivit d'objet
        self.planet_menu = False
        self.following_object = -1  # comporte l'id de l'objet que l'on suis (-1 = aucun objet)


        # variable pour les fps 
        self.fps = 60
        self.fps_list = []
        self.visible_fps = True

        #variable pour les nouvelles planettes 
        self.new_planet_statu = 'none' # statu de la nouvelle planette | 'none' 'click' 'direction' 'caracteristique' 
        self.new_planet_x = 0
        self.new_planet_y = 0
        self.new_planet_speed_x = 0
        self.new_planet_speed_y = 0
        self.new_planet_cos = 0
        self.new_planet_sin = 0
        self.new_planet_speed = 0    #self.speed(self.new_planet_speed_x,self.new_planet_speed_y)
        self.new_planet_mass = 0
        self.new_planet_name = 'new_planet'
        self.new_planet_density = 5520
        self.new_planet_error = ""
        self.new_planet_error_timer = 0
        self.new_planet_color = (255,255,255)
        self.new_planet_id = self.create_new_id()
        self.new_planet_type = "asteroid"


        # autres variables divers 
        self.visible_coordonates = True
        self.visible_version = True
        self.simulated_time = 0
        self.cycle = 0
        self.enable_cycle = False
        self.realistic_textures = True
        self.allways_visible_objects = True
        self.visible_trajectory = True
        self.tick_period = 10
        self.tick = self.tick_period
        self.type_list = ["exoplanet","asteroid","easteregg","egg","sun","mercure","venus","earth","mars","jupiter","saturn","uranus","neptune","pluto"]
        self.statu = "pause"        # défini si la sim. est en pause , dans un menu etc...   |  'pause' ' simulating' 'label'
        self.menu = "choosing_simulations"    # définit quel menu est ouvert  | 'simulating' 'setting' 'video_setting' 'controls_setting' 'languages_setting' 'caracteristique' 'choosing_simulations' 
        self.mode = "none"          # définit si un mode est activé | 'none'  'new_planet'



        self.define_textures(self.objects)
        


    def on_draw(self):  # Partie graphique 
        
        """ Partie graphique du programme | tout ce qui s'affiche a l'écran se passe ici """

        arcade.start_render()  # annihile le contenu de l'image précédente 

         # Variables / texte a ne jamais changer :
        Xe,Ye = Physical_Screen.orgin_from_center_phy(self.screen_x  ,  self.screen_y ,  self.zoom, Constante.Bordure_x , Constante.Bordure_y )   # fait le changement de point de vue (le centre de l'écran)
            

        if self.menu == "simulating":  



            for body in self.objects :  # affiche les objets sur l'écran 
                pos_x , pos_y = Physical_Screen.to_screen(Xe,Ye,body.position_x , body.position_y,self.zoom)


                # affiche la trajectoire des planetes 
                if self.visible_trajectory :
                    for i in range(0,len(body.last_positions)-2) :
                        line_x , line_y = Physical_Screen.to_screen(Xe , Ye , body.last_positions[i][0] , body.last_positions[i][1],self.zoom)
                        end_pos_x , end_pos_y = Physical_Screen.to_screen(Xe , Ye , body.last_positions[i+1][0] , body.last_positions[i+1][1],self.zoom)
                        color = body.color
                        b = list(color)
                        b.append(50)
                        color = tuple(b)
                        arcade.draw_line(line_x , line_y , end_pos_x , end_pos_y , color = color , line_width=3)


                if self.realistic_textures :
                    texture = body.texture
                    scale = float(body.texture_size )
                    arcade.draw_scaled_texture_rectangle(pos_x , pos_y, texture, abs(body.radius) * scale * self.zoom * self.size, 0)
                else : 
                    arcade.draw_circle_filled( pos_x , pos_y , abs(body.radius) * self.zoom * self.size , body.color)

                if self.allways_visible_objects :
                    arcade.draw_point(pos_x , pos_y , body.color , 1)

                


            # Texte à afficher en dernier :
               


            arcade.draw_text(self.vocabulaire[self.langue][24] + self.Unites(self.Simulation_speed,"time") + " / sec",Constante.Bordure_x - 400 , 50,(120,120,120),15) 

            if self.enable_cycle == True :  # si le mode cycle est activé , on affichera le nombre de cycle et pas le temps total simuler
                arcade.draw_text("Cycles : " + str(self.cycle),Constante.Bordure_x - 400 , 80,(120,120,120),15)
            else :
                arcade.draw_text(self.vocabulaire[self.langue][23] + self.Unites(self.simulated_time,"time"),Constante.Bordure_x - 400 , 80,(120,120,120),15)

            if self.statu == "pause" :
                arcade.draw_text("Pause" ,Constante.Bordure_x - 400 , 110,(120,120,120),15)



            # dessine l'échelle 

            scale_color = (92,92,192)   # couleur de l'échelle
            arcade.draw_line(Constante.Bordure_x/2 + 220, 50, Constante.Bordure_x/2 - 220, 50,   scale_color  , 7)  # ligne
            arcade.draw_triangle_filled(Constante.Bordure_x/2 + 250, 50,Constante.Bordure_x/2 + 220, 60,Constante.Bordure_x/2 + 220, 40 , scale_color)   # fleches
            arcade.draw_triangle_filled(Constante.Bordure_x/2 - 250, 50,Constante.Bordure_x/2 - 220, 60,Constante.Bordure_x/2 - 220, 40 , scale_color)
            arcade.draw_text(self.Unites(1/self.zoom*500,"length"),Constante.Bordure_x/2 - 50,60,scale_color,15)    # nombre


            # dessine le planete_menu
            
            if self.planet_menu :   
                for obj in self.objects :   # parcoure tout les objets

                    if obj.id == self.following_object :    # si c'est le bon id :

                        arcade.draw_rectangle_filled(Constante.Bordure_x , Constante.Bordure_y/2 , 600 , 600 , (180,180,180,70))
                        rounded_mass , exponent = int(str(int(obj.mass))[:4])/1000 , len(str(int(obj.mass)))-1
                        arcade.draw_text(self.vocabulaire[self.langue][35] + str(rounded_mass) + "* 10^" + str(exponent) + " kg" , Constante.Bordure_x-285 , Constante.Bordure_y/2+250 , (0,0,0) , 15)

                        arcade.draw_text(self.vocabulaire[self.langue][36] + str(int(obj.density)) + " kg/m³" , Constante.Bordure_x-285 , Constante.Bordure_y/2+210 , (0,0,0) , 15)
                        arcade.draw_text(self.vocabulaire[self.langue][37] + self.Unites(self.speed(obj.speed_x,obj.speed_y),"speed") , Constante.Bordure_x-285 , Constante.Bordure_y/2+170 , (0,0,0) , 15)
                        arcade.draw_text(self.vocabulaire[self.langue][38] + str(round(obj.acceleration,2)) + "m/sec²" , Constante.Bordure_x-285 , Constante.Bordure_y/2+130 , (0,0,0) , 15)

                        
                        colors = obj.color 
                        arcade.draw_text(self.vocabulaire[self.langue][39] + str(int(colors[0]))+ "," + str(int(colors[1]))+ "," + str(int(colors[2])) , Constante.Bordure_x-285 , Constante.Bordure_y/2+90 , (0,0,0) , 15)
                        arcade.draw_text(self.vocabulaire[self.langue][40] + obj.name , Constante.Bordure_x-285 , Constante.Bordure_y/2+50 , (0,0,0) , 15)
                        arcade.draw_text(self.vocabulaire[self.langue][41] + str(round(obj.radius/1000,2)) + " km" , Constante.Bordure_x-285 , Constante.Bordure_y/2+10 , (0,0,0) , 15)
                        arcade.draw_text(self.vocabulaire[self.langue][42] + str(obj.id) , Constante.Bordure_x-285 , Constante.Bordure_y/2-30 , (0,0,0) , 15)
                        arcade.draw_text(self.vocabulaire[self.langue][43] + obj.type , Constante.Bordure_x-285 , Constante.Bordure_y/2-70 , (0,0,0) , 15)





        elif self.menu == "video_setting" :

            arcade.draw_text(self.vocabulaire[self.langue][20] ,  200  ,  180 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][19] ,  200  ,  305, color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][18] ,  200  ,  430, color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][15],200 , 680 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][22], 1000 , 180 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][21], 1000 , 305 , color=(0,145,255) , font_size=18)


            if self.enable_cycle == True :  # si le mode cycle est activé , on affichera le nombre de cycle et pas le temps total simuler
                arcade.draw_text(self.vocabulaire[self.langue][17] ,  200  ,  555, color=(0,145,255) , font_size=18)
            else :
                arcade.draw_text(self.vocabulaire[self.langue][16] ,  200  ,  555, color=(0,145,255) , font_size=18)




        elif self.menu == "controls_setting" :
            arcade.draw_text(self.vocabulaire[self.langue][13],  210  ,  190 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][12] ,  210  ,  315 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][10] ,  210  ,  440 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][8] ,  210  ,  565 , color=(0,145,255) , font_size=18)
            arcade.draw_text(self.vocabulaire[self.langue][6],210  ,  690 , color=(0,145,255) , font_size=18)




        if self.mode == "new_planet" :
            fog_opacity = 110

            if self.new_planet_statu == 'click' :
                arcade.draw_rectangle_filled(Constante.Bordure_x/2,Constante.Bordure_y/2,Constante.Bordure_x,Constante.Bordure_y,(50,50,50,fog_opacity))
                arcade.draw_circle_filled(self.mouse_pos_x,self.mouse_pos_y,25,(255,0,0))


            if self.new_planet_statu == 'direction' :
                arcade.draw_rectangle_filled(Constante.Bordure_x/2,Constante.Bordure_y/2,Constante.Bordure_x,Constante.Bordure_y,(50,50,50,fog_opacity))
                pos_x , pos_y = Physical_Screen.to_screen(Xe,Ye,self.new_planet_x,self.new_planet_y,self.zoom)
                arcade.draw_circle_filled(pos_x , pos_y,25,(255,0,0))

                dist = self.distance(pos_x,pos_y,self.mouse_pos_x,self.mouse_pos_y)

                if dist != 0 :
                    sinus = (self.mouse_pos_y-pos_y)/dist
                    cosinus = (self.mouse_pos_x-pos_x) / dist
                else :
                    sinus = 1
                    cosinus = 1


                size = 10
                position_x = self.mouse_pos_x - cosinus*size
                position_y = self.mouse_pos_y - sinus*size

                arcade.draw_line(pos_x,pos_y,position_x,position_y,scale_color,3)

                x1 = position_x + size*cosinus
                y1 = position_y + size*sinus
                x2 = position_x + size*sinus
                y2 = position_y - size*cosinus
                x3 = position_x - size*sinus
                y3 = position_y + size*cosinus

                arcade.draw_triangle_filled(x1,y1,x2,y2,x3,y3,scale_color)

            if self.new_planet_statu == 'caracteristique' :
                arcade.draw_text(self.vocabulaire[self.langue][27] , 650 ,Constante.Bordure_y-120,font_size=25, width=600, align="center",anchor_x="center", anchor_y="center")
                if self.new_planet_error_timer > 0 : arcade.draw_text(self.new_planet_error , 650 ,Constante.Bordure_y-170,font_size=15, width=600, align="center",anchor_x="center", anchor_y="center",color=(192,20,20))
                arcade.draw_text(self.vocabulaire[self.langue][28],150,  Constante.Bordure_y-350,font_size=20)
                arcade.draw_text(self.vocabulaire[self.langue][29],150,  Constante.Bordure_y-550,font_size=20)
                arcade.draw_text(self.vocabulaire[self.langue][30],150,  Constante.Bordure_y-750,font_size=20)
                arcade.draw_text(self.vocabulaire[self.langue][31],950,  Constante.Bordure_y-150,font_size=20)
                arcade.draw_text(self.vocabulaire[self.langue][32],950,  Constante.Bordure_y-350,font_size=20)
                arcade.draw_text(self.vocabulaire[self.langue][33],950,  Constante.Bordure_y-550,font_size=20)
                arcade.draw_text(self.vocabulaire[self.langue][34],950,  Constante.Bordure_y-750,font_size=20)






        """choses a afficher tout le temps """


        for boutons in self.boutons :   
            if eval(boutons.screen_condition) :  # les boutons ne s'affiche que si leur condition est respecter
                arcade.draw_rectangle_filled((boutons.left+boutons.right)/2,(boutons.up+boutons.down)/2,abs(boutons.left-boutons.right),abs(boutons.up-boutons.down),boutons.color)
                arcade.draw_lrtb_rectangle_outline(boutons.left , boutons.right , boutons.up , boutons.down , boutons.outline_color , 7)
                arcade.draw_text(boutons.text , (boutons.left+boutons.right)/2 - len(boutons.text) * boutons.text_size / 3.2 , (boutons.up+boutons.down)/2-(.4*boutons.text_size), boutons.text_color,boutons.text_size)


        for label in self.labels :
            if eval(label.screen_condition) :

                if label.activated :
                    arcade.draw_rectangle_filled((label.left+label.right)/2,(label.up+label.down)/2,abs(label.left-label.right),abs(label.up-label.down),color=label.active_color,tilt_angle=label.tilt_angle)
                else :
                    arcade.draw_rectangle_filled((label.left+label.right)/2,(label.up+label.down)/2,abs(label.left-label.right),abs(label.up-label.down),color=label.in_color,tilt_angle=label.tilt_angle)
                arcade.draw_rectangle_outline((label.left+label.right)/2,(label.up+label.down)/2,abs(label.left-label.right),abs(label.up-label.down),color=label.outline_color,border_width=label.outline_size,tilt_angle=-label.tilt_angle)
                arcade.draw_text(label.text , (label.left+label.right)/2 - len(label.text) * label.text_size / 3.2 , (label.up+label.down)/2-(.4*label.text_size) , label.text_color , label.text_size)

        
        if self.visible_coordonates :
            mouse_x_screen,mouse_y_screen = self.mouse_pos_x,self.mouse_pos_y   # détermine les coordonée X,Y du curseur de la souris dans le repère physique
            arcade.draw_text("x : " + str(mouse_x_screen) ,50,55,(120,120,120),15)    #affiche les coordonées du curseur
            arcade.draw_text("Y : " + str(mouse_y_screen) ,50,75,(120,120,120),15) 


        if self.visible_fps and self.menu != "caracteristique" and self.menu != "choosing_simulations":
            arcade.draw_text("fps : " + str(self.fps) ,120,Constante.Bordure_y - 50,(120,120,120),15)     #affiche les fps 


        if self.visible_version :    
            arcade.draw_text("Version : " + Constante.Version,50,35,(120,120,120),15)    #affiche la version du programme en bas a droite du porgramme 



    def on_update(self, delta_time):   # toute les action qui se passent en boucle se calcul ici
        
        """ partie principal du programme """




        """calcul de la physique de chaque objets"""

        if self.statu == "simulating":
            self.cycle += 1 



            """calcul de la gravitation"""



            for index1,body in enumerate(self.objects) :     # calculde la gravité 
                backup_speed = self.speed(body.speed_x,body.speed_y)
                
                for index2, body2 in enumerate(self.objects) :  # par rapport a un autre objets
                    if index1 != index2 and body2.type != 'asteroid' :
                                                                    # calcul la nouvelle vitesse de l'objet 
                        body.speed_x , body.speed_y = Gravity.speed(body.position_x,body.position_y,body.mass,body2.position_x,body2.position_y,body2.mass,body.speed_x,body.speed_y,Constante.G_Constant,delta_time*self.Simulation_speed)

                body.acceleration = abs((self.speed(body.speed_x,body.speed_y) - backup_speed)/(delta_time*self.Simulation_speed))
                body.position_x += body.speed_x * delta_time * self.Simulation_speed  # acctualisation des postition de l'objet
                body.position_y += body.speed_y * delta_time * self.Simulation_speed


            self.simulated_time += delta_time * self.Simulation_speed   # acctualise la durée total simuler~


            if self.tick == 0 :
                for body in self.objects:
                    if len(body.last_positions) <= 1000/self.tick_period:
                        body.last_positions.append((body.position_x, body.position_y))
                    else :
                        body.last_positions.pop(0)
                        body.last_positions.append((body.position_x, body.position_y))


            """ calcul des collisions """
            
            self.colisions()

    

        """ Action diverse à éffectuer  """


        if self.planet_menu :           # problème d'id !!
            for object in self.objects :

                if object.id == self.following_object :
                    
                    self.screen_x = object.position_x
                    self.screen_y = object.position_y




        if self.up :    # si la touche Up est presser , la vitesse de simulation augmente 
            self.Simulation_speed *= 1 + (.8 * delta_time)
        
        if self.down :  # si la touche Down est presser , la vitesse de simulation diminue
            self.Simulation_speed /= 1 + (.8 * delta_time)



        # calcul les fps 
        
        if len(self.fps_list) > 5 :
            self.fps_list.pop(0)

        self.fps_list.append(delta_time)
    

        self.fps = round(1/(sum(self.fps_list)/len(self.fps_list)),1)    # nombre de fps
        self.new_planet_error_timer -= delta_time 

        if self.tick > 0 :
            self.tick -= 1 
        else : 
            self.tick = self.tick_period



    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):  #   modifie la valeur du centre de l'écran 
        self.screen_x -= dx / self.zoom                         #   dans les coordonées physique en fonction 
        self.screen_y -= dy / self.zoom                         #   du déplacement de la souris 



    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):  # réduit / augmente le niveau de zoom si on scroll vers le bas ou vers le haut
        if scroll_y > 0 : 
            self.zoom /= 0.92   # rapproche la camera 
        elif scroll_y < 0 :
            self.zoom *= 0.92   # éloigne la caméra



    def on_mouse_motion(self, x, y, dx, dy):    # si la souris bouge sur l'écran :
        self.mouse_pos_x = x    # coordonées x de la souris 
        self.mouse_pos_y = y    # coordonées y de la souris 
        


    def on_key_press(self, symbol, modifiers):  # quand une touche du clavier est activer 


        if symbol == arcade.key.SPACE and self.statu != 'label' : # met pause a la simulation
            if self.statu == "simulating" :
                self.statu = "pause"
            elif self.statu == "pause" :
                self.statu = "simulating"

        if symbol == arcade.key.ESCAPE :   # ferme la fenetre 
            arcade.exit()

        if symbol == arcade.key.UP :        # augmente la vitesse de simulation
            self.up = True
        if symbol == arcade.key.DOWN :      # diminue la vitesse de simulation
            self.down = True


        if self.statu == 'label' :  

            for label in self.labels :
                if label.activated :    # si le label est activé :


                    if 97 <= symbol <= 123  :    # si on ne supprime pas, j'ajoute la lettre 
                        label.text += chr(symbol) 

                    elif (modifiers == 24 or modifiers == 17 ) and 48 <= symbol <= 57 : # si la touche shift ou lock est activer et que l'on appuis sur les touches de 0 a 9 , j'ajoute la lettre
                        label.text += chr(symbol)

                    elif (modifiers != 24 or modifiers != 17 ) and symbol == 54 : # si on appuis sur la touche - : je l'ajoute 
                        label.text += "-"

                    elif (modifiers != 24 or modifiers != 17 ) and symbol == 53 : # si on appuis sur la touche ( : je l'ajoute 
                        label.text += "("

                    elif (modifiers != 24 or modifiers != 17 ) and symbol == 41 : # si on appuis sur la touche ) : je l'ajoute 
                        label.text += ")"

                    elif (modifiers != 24 or modifiers != 17 ) and symbol == 44 : # si on appuis sur la touche , : je l'ajoute 
                        label.text += ","

                    elif (modifiers != 24 or modifiers != 17 ) and symbol == 59 : # si on appuis sur la touche ; je l'ajoute
                        label.text += "."

                    elif (modifiers != 24 or modifiers != 17 ) and symbol == 56 : # si on appuis sur la touche _ je l'ajoute 
                        label.text += "_"

                    elif symbol == arcade.key.SPACE :
                        label.text += " "

                    elif label.text != "" and symbol == 65288 :     # je supprime le dernier elément du texte 
                        label.text = label.text[:-1]

        else :
            if symbol == arcade.key.A and self.menu != "choosing_simulations":
                if self.mode == 'none' :
                    self.mode = 'new_planet'
                    self.new_planet_setup()
                    self.new_planet()
                else :
                    self.mode = 'none'
                    self.new_planet_statu = "none"
                    self.menu = "simulating"
                    self.statu = "pause" 

            if symbol == arcade.key.ENTER :
                if self.mode == 'new_planet' :

                    
                    if self.new_planet_type not in self.type_list :
                        self.new_planet_type = "asteroid"


                    self.objects.append(Objects(self.new_planet_mass,self.new_planet_x,self.new_planet_y,self.new_planet_speed_x,self.new_planet_speed_y,
                                                name=self.new_planet_name,color=self.new_planet_color,density=self.new_planet_density,id=self.new_planet_id,type=self.new_planet_type))
                    

                    self.mode = 'none'
                    self.new_planet_statu = "none"
                    self.menu = "simulating"
                    self.statu = "pause" 
                    self.define_textures(self.objects)

            if symbol == arcade.key.P : # choisis la simulation 
                self.menu = "choosing_simulations"
                self.new_planet_statu = 'none'

                    

    def on_key_release(self, symbol, modifiers):


        if symbol == arcade.key.UP :        
            self.up = False
        if symbol == arcade.key.DOWN :      
            self.down = False



    def on_mouse_release(self, x, y, button, modifiers ):
        
        if self.boutons == [] : # si il n'y a pas de boutons , on ne fait rien
            pass
        else :
            for boutons in self.boutons:  #liste tout les boutons 

                if (boutons.right > x > boutons.left) and (boutons.up > y > boutons.down) :  # si on a cliquer a l'interieur du boutons :
                    
                    if eval(boutons.screen_condition) : # et que la condition est respecter
                        Button.active(self,boutons)     # on execute l'instruction
                        break   # on n'appuis que sur 1 bouton en même temps


        if self.labels == [] : # si il n'y a pas de labels , on ne fait rien 
            pass
        else :
            for label in self.labels:  #liste tout les boutons 

                if (label.left < x < label.right) and (label.down < y < label.up) :  # si on a cliquer a l'interieur du label :
                    if eval(label.screen_condition) and label.writing_only == False : # et que la condition est respecter


                        if label.activated :
                            label.activated = False
                            self.statu = 'pause'
                            
                            if label.type == "new_planet_mass" :
                                value, error = self.scientific_to_decimal(label.text)
                                if error == "none" :
                                    self.new_planet_mass = value
                                else :
                                    self.new_planet_error = "syntaxe mass label error"
                                    self.new_planet_error_timer = 5
                                    label.text = str(self.new_planet_mass)

                            if label.type == "new_planet_density" :
                                value, error = self.scientific_to_decimal(label.text)
                                if error == "none" :
                                    self.new_planet_density = value
                                else :
                                    self.new_planet_error = "syntaxe density label error"
                                    self.new_planet_error_timer = 5
                                    label.text = str(self.new_planet_density)

                            if label.type == "new_planet_speed" :
                                value, error = self.scientific_to_decimal(label.text)
                                if error == "none" :
                                    self.new_planet_speed_x = value * self.new_planet_cos
                                    self.new_planet_speed_y = value * self.new_planet_sin

                                else :
                                    self.new_planet_error = "syntaxe speed label error"
                                    self.new_planet_error_timer = 5
                                    label.text = str(self.speed(self.new_planet_speed_x,self.new_planet_speed_y))

                            if label.type == "new_planet_name" :
                                self.new_planet_name = label.text

                            if label.type == "new_planet_color" :
                                value, error = self.color_to_rgb(label.text)
                                if error == "none" :
                                    self.new_planet_color = value
                                else :
                                    self.new_planet_error = "syntaxe color label error"
                                    self.new_planet_error_timer = 5
                                    label.text = str(self.new_planet_color)

                            if label.type == "new_planet_id" :
                                if self.check_new_planet_id(int(label.text)) == False :   # si l'id n'existe pas on remplace l'id de la nouvelle planet 
                                    self.new_planet_id = label.text
                                else :
                                    self.new_planet_error = "This id already exists"
                                    self.new_planet_error_timer = 5
                                    label.text = str(self.new_planet_id)

                            if label.type == "new_planet_type" :
                                if label.text in self.type_list :
                                    self.new_planet_type = label.text
                                else :
                                    self.new_planet_error = "this type do not exist"
                                    self.new_planet_error_timer = 5
                                    label.text = "asteroid" 
                                    self.new_planet_type = "asteroid"
                                    


                        else :
                            label.activated = True
                            self.statu = 'label'


        
        if self.menu == "simulating" and self.mode == 'none' :

            Xe,Ye = Physical_Screen.orgin_from_center_phy(self.screen_x  ,  self.screen_y ,  self.zoom, Constante.Bordure_x , Constante.Bordure_y )
            x_coo , y_coo = Physical_Screen.to_physic(Xe , Ye , x , y ,self.zoom)   # détermine les coordonées physique du clique
            found = False   

            for object in self.objects :  # parcoure tout les objets de la simulation 
                if self.distance(x_coo,y_coo,object.position_x,object.position_y) <= object.radius :  # si on a cliquer sur un objet :
                    self.planet_menu = True     # on active le menu_planete 
                    self.following_object = object.id   # on suis l'objet n°index
                    found = True
                    break

            if found == False :  # si on clique dans le vide on enleve le menu_planete
                self.planet_menu = False
                self.following_object = -1 # -1 signifit aucun objet
                    

        if self.mode == "new_planet" and button == arcade.MOUSE_BUTTON_LEFT :
            Xe,Ye = Physical_Screen.orgin_from_center_phy(self.screen_x  ,  self.screen_y ,  self.zoom, Constante.Bordure_x , Constante.Bordure_y )   # fait le changement de point de vue (le centre de l'écran)

            if self.new_planet_statu == "click" :
                self.new_planet_x , self.new_planet_y = Physical_Screen.to_physic(Xe,Ye,self.mouse_pos_x,self.mouse_pos_y,self.zoom)
                self.new_planet()

            elif  self.new_planet_statu == "direction" :
                pos_x , pos_y = Physical_Screen.to_screen(Xe,Ye,self.new_planet_x,self.new_planet_y,self.zoom)
                legth = self.distance(pos_x,pos_y,self.mouse_pos_x,self.mouse_pos_y)

                if legth != 0 :
                    sinus = (self.mouse_pos_y-pos_y)/legth
                    cosinus = (self.mouse_pos_x-pos_x) / legth
                else :
                    sinus = 1
                    cosinus = 1

                self.new_planet_cos = cosinus
                self.new_planet_sin = sinus

                self.new_planet()



    def new_planet(self) : 


        if self.new_planet_statu == "none" : 
            self.new_planet_statu = "click" 
            self.statu = "pause"

        elif self.new_planet_statu == "click" :
            self.new_planet_statu = "direction" 

        elif self.new_planet_statu == "direction" :
            self.new_planet_statu = "caracteristique"
            self.menu = "caracteristique"

        else :
            self.new_planet_statu = "none"
            
        

    def new_planet_setup(self) :

        #variable pour les nouvelles planettes 
        self.new_planet_statu = 'none' # statu de la nouvelle planette | 'none' 'click' 'direction' 'caracteristique' 
        self.new_planet_x = 0
        self.new_planet_y = 0
        self.new_planet_speed_x = 0
        self.new_planet_speed_y = 0
        self.new_planet_cos = 0
        self.new_planet_sin = 0
        self.new_planet_speed = 0    #self.speed(self.new_planet_speed_x,self.new_planet_speed_y)
        self.new_planet_mass = 0
        self.new_planet_name = 'new_planet'
        self.new_planet_density = 5520
        self.new_planet_error = ""
        self.new_planet_error_timer = 0
        self.new_planet_color = (255,255,255)
        self.new_planet_id = self.create_new_id()

        for label in self.labels:  #liste tout les boutons 

            if label.type == "new_planet_mass" :
                label.text = str(self.new_planet_mass)

            if label.type == "new_planet_density" :
                label.text = str(self.new_planet_density)

            if label.type == "new_planet_speed" :
                label.text = str(self.speed(self.new_planet_speed_x,self.new_planet_speed_y))

            if label.type == "new_planet_name" :
                label.text = self.new_planet_name

            if label.type == "new_planet_color" :
                label.text = str(self.new_planet_color)

            if label.type == "new_planet_id" :
                label.text = str(self.new_planet_id)



    def closer(self,index,posx,posy,Body = list) :

        
        if len(Body) < 2 :
            return -1,-1    # si la distance est négative , cela veut dire qu'il ne faut rien faire

        else :
            
            
            mini = self.distance(posx,posy,Body[0].position_x,Body[0].position_y)   # initialise la valeur minimal au premiere objet de la liste
            if mini == 0 :
                mini = self.distance(posx,posy,Body[1].position_x,Body[1].position_y)   # si la valeur minimal était de 0 , on recomence avec un autre valeur
            numerator = 0

            for ind,obj in enumerate(Body) : # parcoure toute la liste de valeur
                
                if index != ind :
                    distance = self.distance(posx,posy,obj.position_x,obj.position_y)
                    if distance <= mini :
                        mini = distance # distance minimal 
                        numerator = ind # id de l'objet le plus proche

            return numerator,mini



    def distance2(self,x1,y1,x2,y2):
        return (x2-x1) * (x2-x1) + (y2-y1) * (y2-y1)



    def distance(self,x1,y1,x2,y2):
        return sqrt((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1))



    def vector_sum(self,Sx1,Sy1,Sx2,Sy2):
        speed1 = sqrt(Sx1**2+Sy1**2)
        speed2 = sqrt(Sx2**2+Sy2**2)
        return speed1+speed2



    def speed(self,speed_x,speed_y):
        return sqrt(speed_x*speed_x  +  speed_y*speed_y)



    def Qmoyenne(self,mass1,a,mass2,b):
        return (mass1*a + mass2*b)/(mass1+mass2)



    def colisions2(self,delta_time):    # Inutilisable
        """ acctualise les compteurs des Objets """

        
        for index,body in enumerate(self.objects) : # check tout les objet

                
                if body.colision_counter < 0 : # si le conteur == 0 :

                    body2 = self.objects[body.near_body_id]
                    distance = self.distance(body.position_x , body.position_y, body2.position_x , body2.position_y)    # calcul la distance par rapport au deuxieme objet
                    

                    if distance < (body.radius + body2.radius) and body.near_body_id != index :    # si les deux objets se touchent on crée un nouvel objet avec les nouvelles caracteristique
                        masse = body.mass + body2.mass
                        densite = self.Qmoyenne(body.mass , body.density  ,  body2.mass , body2.density)    # définition des caractéristique des objets
                        speed_x = self.Qmoyenne(body.mass , body.speed_x  ,  body2.mass , body2.speed_x)
                        speed_y = self.Qmoyenne(body.mass , body.speed_y  ,  body2.mass , body2.speed_y)
                        pos_x = self.Qmoyenne(body.mass , body.position_x  ,  body2.mass , body2.position_x)
                        pos_y = self.Qmoyenne(body.mass , body.position_y  ,  body2.mass , body2.position_y)
                        color_r = self.Qmoyenne(body.mass , body.color[0]  ,  body2.mass , body2.color[0])
                        color_g = self.Qmoyenne(body.mass , body.color[1]  ,  body2.mass , body2.color[1])
                        color_b = self.Qmoyenne(body.mass , body.color[2]  ,  body2.mass , body2.color[2])

                        if body.mass > body2.mass :
                            name = body.name 
                        else : 
                            name = body2.name 

                        self.objects.remove(body) # détruit les deux anciens objets 
                        self.objects.remove(body2)
                        self.objects.append(Objects(masse,pos_x,pos_y,speed_x,speed_y,name,(color_r,color_g,color_b),density=densite))  # crée le nouvel objet
                        


                        self.recalculate_colision_counters(delta_time)
                        break


                    else :  #  recalcule le conteur et l'objet le plus proche
                        plus_proche = self.closer(index,body.position_x,body.position_y,self.objects)
                        if plus_proche[1] != -1 : # si la distance est négative , cela veut dire qu'il ne faut rien faire
                            body.near_body_id = plus_proche[0]
                            

                            G1 = (Gravity.acceleration(body.position_x,body.position_y,body2.position_x,body2.position_y,body2.mass,Constante.G_Constant))
                            G2 = (Gravity.acceleration(body.position_x,body.position_y,body2.position_x,body2.position_y,body.mass,Constante.G_Constant))


                            attraction = abs(self.vector_sum(G1[0],G1[1],G2[0],G2[1]))
                            speed = abs(self.vector_sum(body.speed_x,body.speed_y,body2.speed_x,body2.speed_y))
                            distance = plus_proche[1] - body.radius - body2.radius
                            
                            delta = speed*speed-4*attraction*distance
                            if delta >= 0 :
                                x1 = (-speed-sqrt(delta))/(2*attraction)
                                x2 = (-speed+sqrt(delta))/(2*attraction)

                                if x1 > x2 :
                                    body.colision_counter = x1
                                else : 
                                    body.colision_counter = x2

                            print(f"{body.name} : {delta} {body.colision_counter}")

                            

                else : # diminue le conteur de 1 
                    body.colision_counter -= delta_time
                    print(f"{body.name} : {body.colision_counter}")



    def colisions(self):
        for index1,body in enumerate(self.objects) :     # calculde la gravité         

                for index2, body2 in enumerate(self.objects) :  # par rapport a un autre objets
                    if index2 > index1 :

                        if self.distance(body.position_x , body.position_y , body2.position_x , body2.position_y) < ( body.radius + body2.radius) :
                            
                            masse = body.mass + body2.mass
                            densite = self.Qmoyenne(body.mass , body.density  ,  body2.mass , body2.density)    # définition des caractéristique des objets
                            speed_x = self.Qmoyenne(body.mass , body.speed_x  ,  body2.mass , body2.speed_x)
                            speed_y = self.Qmoyenne(body.mass , body.speed_y  ,  body2.mass , body2.speed_y)
                            pos_x = self.Qmoyenne(body.mass , body.position_x  ,  body2.mass , body2.position_x)
                            pos_y = self.Qmoyenne(body.mass , body.position_y  ,  body2.mass , body2.position_y)
                            color_r = self.Qmoyenne(body.mass , body.color[0]  ,  body2.mass , body2.color[0])
                            color_g = self.Qmoyenne(body.mass , body.color[1]  ,  body2.mass , body2.color[1])
                            color_b = self.Qmoyenne(body.mass , body.color[2]  ,  body2.mass , body2.color[2])

                            if body.mass > body2.mass :
                                name = body.name 
                                id = body.id
                                type = body.type
                                if body.type == 'asteroid' :
                                    texture = body.texture
                                    size = body.texture_size
                                    self.objects.remove(body) # détruit les deux anciens objets 
                                    self.objects.remove(body2)
                                    self.objects.append(Objects(masse,pos_x,pos_y,speed_x,speed_y,name,(color_r,color_g,color_b),density=densite,id=id,type=type,texture=texture,texture_size=size)) # crée le nouvel objet 
                                else :
                                    self.objects.remove(body) # détruit les deux anciens objets 
                                    self.objects.remove(body2)
                                    self.objects.append(Objects(masse,pos_x,pos_y,speed_x,speed_y,name,(color_r,color_g,color_b),density=densite,id=id,type=type))  # crée le nouvel objet
                            
                            else : 
                                name = body2.name 
                                id = body2.id
                                type = body2.type
                                if body2.type == 'asteroid' :
                                    texture = body2.texture
                                    size = body2.texture_size
                                    self.objects.remove(body) # détruit les deux anciens objets 
                                    self.objects.remove(body2)
                                    self.objects.append(Objects(masse,pos_x,pos_y,speed_x,speed_y,name,(color_r,color_g,color_b),density=densite,id=id,type=type,texture=texture,texture_size=size)) # crée le nouvel objet 
                                else :
                                    self.objects.remove(body) # détruit les deux anciens objets 
                                    self.objects.remove(body2)
                                    self.objects.append(Objects(masse,pos_x,pos_y,speed_x,speed_y,name,(color_r,color_g,color_b),density=densite,id=id,type=type))  # crée le nouvel objet
                            

                            

                            
                            self.define_textures(self.objects)
                            break



    def recalculate_colision_counters(self,delta_time):     # Inutilisable
        for idea,planet in enumerate(self.objects) :    # actualise toute les planetes et recalcule le conteur et l'objet le plus proche
            plus_proche = self.closer(idea,planet.position_x,planet.position_y,self.objects) 
            if plus_proche[1] != -1 : # si la distance est négative , cela veut dire qu'il ne faut rien faire

                planet.near_body_id = copy(plus_proche[0])   # id de la planete la plus proche  
                planet2 = copy(self.objects[planet.near_body_id]) # définit la planete la plus proche
                
                
                G1 = (Gravity.acceleration(planet.position_x,planet.position_y,planet2.position_x,planet2.position_y,planet2.mass,Constante.G_Constant))
                G2 = (Gravity.acceleration(planet.position_x,planet.position_y,planet2.position_x,planet2.position_y,planet.mass,Constante.G_Constant))
                
                attraction = abs(self.vector_sum(G1[0],G1[1],G2[0],G2[1]))
                speed = abs(self.vector_sum(planet.speed_x,planet.speed_y,planet.speed_x,planet.speed_y))
                distance = plus_proche[1]
                
                delta = speed*speed-4*attraction*distance
                if delta >= 0 :
                    planet.colision_counter = (-speed+sqrt(delta))/(2*attraction)



    def color_to_rgb(self,x = str):

        if x[0] == "(" and x[-1] == ")" :

            comma_pos = []
            for index,value in enumerate(x):  # parcoure la liste 

                if (( 48 <= ord(value) <= 57 ) or ( ord(value) == 40) or ( ord(value) == 41 ) or ( ord(value) == 44))  == False:   # si in caractere n'est pas normal, on fait une erreur 
                    return 0 , "syntaxe"


                if ord(value) == 44 :   # si c'est une virgule, on suvegarde sa position 
                    comma_pos.append(index)


            if len(comma_pos) != 2 :    # si il n'y a pas 2 vigules, on envoie une erreur 
                return (0,0,0) , "syntaxe"

            elif len(comma_pos) == 2 :  # si il y a 2 virgules, on regarde les valeurs des nombres et on renvoie le résultat
                x1 = int(x[1:comma_pos[0]]) % 256
                x2 = int(x[comma_pos[0]+1:comma_pos[1]]) % 256
                x3 = int(x[comma_pos[1]+1:len(x)-1]) % 256

                return (x1,x2,x3) , "none"
                
        else :
            return (0,0,0) , "syntaxe"



    def scientific_to_decimal(self,x = str):

        e_count = 0
        if x == "" :    # si la liste est vide, on evoie une erreur 
            return 0 , "syntaxe" 

        for index,value in enumerate(x):  # parcoure la liste 

            if ord(value) ==  101 :  # compte le nombre de e 
                place = index 
                e_count += 1 

            if (( 48 <= ord(value) <= 57 ) or ( ord(value) == 101) or ( ord(value) == 45 ) or ( ord(value) == 46))  == False:   # si in caractere n'est pas normal, on fait une erreur 
                return 0 , "syntaxe"

        if e_count == 0 :   # si il n'y a pas d'exposant, on retourne le flotant normalement 
            return float(x), "none"

        elif e_count == 1:   # si tout est correct, on retourne le nombre souhaiter 
            mantissa = float(x[:place])
            exponent = float(x[place+1:])
            return mantissa * 10**exponent , "none"

        else :  # si il y a trop de e , on envoie une erreur 
            return 0 , "syntaxe"
            


    def check_new_planet_id(self,x):
        id_list = []
        for obj in self.objects :
            id_list.append(obj.id)

        return (x in id_list) # si l'id existe déja, on retourne True sinon, False



    def create_new_id(self):

        id_list = []
        for obj in self.objects :   # crée une liste avec tout les id de tout les objets 
            id_list.append(obj.id)


        for new in range(1000000):
            if new not in id_list : # on cherche des nombre jusqu'a ce qu'il y en ai un correcte puis on le renvoie
                return new   
            


    def define_textures(self,Objects):
        asteroid_textures_list = []
        for Object in Objects :
            distance = 442
            rgb = Object.color 
            with open('Textures.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|') 
                for index,row in enumerate(spamreader):

                    if Object.name == row[4] : 
                        texture = row[0]
                        size = row[1]
                        Object.texture = arcade.load_texture(texture)
                        Object.texture_size = size
                        break

                    if row[2] == 'True' and Object.type == 'exoplanet' and row[4] == 'exoplanet': 
                        distance_rgb = self.rgb_Distance(rgb,row[3])
                        if distance_rgb < distance:   
                            texture = row[0]
                            size = row[1]
                            distance = distance_rgb

                    if Object.type == 'asteroid' and row[4] == 'asteroid':
                        asteroid_textures_list.append((row[0],row[1]))
                        

            if Object.type == 'asteroid' and Object.texture == arcade.load_texture("Textures without background/No_textures-removebg-preview.png") :
                rand = asteroid_textures_list[randint(0, len(asteroid_textures_list)-1)]
                Object.texture = arcade.load_texture(rand[0])
                Object.texture_size = rand[1]

            elif Object.type == 'exoplanet' :
                Object.texture = arcade.load_texture(texture)
                Object.texture_size = size



    def rgb_Distance(self,rgb,rgb2):
        rgb2 = rgb2[1:-1]
        virgules = []
        for i,a in enumerate(rgb2) :
            if a == ',' : virgules.append(i)

        x = int(rgb2[0:virgules[0]])
        y = int(rgb2[virgules[0]+1:virgules[1]])
        z = int(rgb2[virgules[1]+1:])

        a,b,c = int(rgb[0]) , int(rgb[1]) , int(rgb[2])


        return sqrt((a-x)**2 + (b-y)**2 + (c-z)**2)



    def Unites(self,x,mode):    # convertie un nombre en unité

        if mode == "length" :     # la valeur de x est en metre
            if x > 0 : positif = 1
            else : positif = -1

            x = abs(x)

            if x <= 1 :
                return str(round(positif*x/.01,2)) + " Cm"

            elif 1 <= x < 1000 :
                return str(round(positif*x,2)) + " m"

            elif 1000 <=  x < 1000000000 :
                return str(round(positif*x/1000,2)) + " Km" 

            elif 1000000000 <= x < 1000000000000 :  # 10 ** 9
                return str(round(positif*x/(10 ** 9),2)) + " M Km" 

            elif 1000000000000 <= x < 9460000000000000 :   # 10 ** 12
                return str(round(positif*x/(10 ** 12),2)) + " G Km" 

            elif x > 9460000000000000 :    #9.46 * 10**15
                return str(round(positif*x/(9.46*10**15),2)) + self.vocabulaire[self.langue][25] 

            else : 
                return "Undefined"



        if mode == "time" :     # la valeur de x est en seconde

            if x <= 1 :
                return str(round(x*1000,2)) + " ms"

            elif 1 <= x < 60 :
                return str(round(x,2)) + " s"

            elif 60 <= x < 3600 :
                return str(round(x/60,2)) + " min"

            elif 3600 <= x < 86400:
                return str(round(x/3600,2)) + " h"

            elif 86400 <= x < 2592000 :
                return str(round(x/86400,2)) + " days"

            elif 2592000 <= x < 31104000 :
                return str(round(x/2592000,2)) + " months"

            elif 31104000 <= x:
                return str(round(x/31104000,2)) + " years"

            else : 
                return "Undefined"



        if mode == "speed" :     # la valeur de x est en m/s 

            if x < 1 :
                return str(round(x*100,2)) + " cm/s"
            
            elif 1 <= x < 1000 : 
                return str(round(x/1,2)) + " m/s"
            
            elif 1000 <= x < 1000000 : 
                return str(round(x/1000,2)) + " km/s"
            
            elif 1000000 <= x :
                return str(round(x/1000000,2)) + " Mega-m/s"



    def initialize_objects(self,name) : # initialise les objects du system en fonction du nom donné 
        self.objects = []

        if name == "solar_system" :
            self.objects.append(Objects(1.998*10**30,0,0,0,0,name="sun",color=(221, 179, 21),density=1410,type="sun",id=0))
            self.objects.append(Objects(3.285*10**23,57.9*10**9,0,0,47000,name="mercure",color=(90,90,90),density=5430,type="mercure",id=1))
            self.objects.append(Objects(4.8*10**24,-9.14*10**9,107.5*10**9,-34800,-3000,name="venus",color=(120,120,50),density=5240,type="venus",id=2))
            self.objects.append(Objects(5.9*10**24,-25873578*10**3,146736355*10**3,-29544,-5209,name="earth",color=(20,20,180),density=5520,type="earth",id=3)) 
            self.objects.append(Objects(7.35*10**22,-25943037*10**3,147130278*10**3,-30529,-5383,name="moon",color=(120,120,120),density=3340,type="moon",id=30))
            self.objects.append(Objects(6.39*10**23,-123.6*10**9,-190*10**9,20100,-13000,name="mars",color=(180,90,20),density=3930,type="mars",id=4))
            self.objects.append(Objects(1.8*10**27,716*10**9,-304*10**9,5000,11966,name="jupiter",color=(197,127,51),density=1330,type="jupiter",id=5))
            self.objects.append(Objects(5.6*10**26,1045*10**9,-975*10**9,6540,7020,name="saturn",color=(244,168,83),density=687,type="saturn",id=6))#
            self.objects.append(Objects(8.6*10**25,2086*10**9,2014*10**9,-4716,4884,name="uranus",color=(123,178,227),density=1270,type="uranus",id=7))
            self.objects.append(Objects(1.024*10**26,4466*10**9,-548*10**9,661,5392,name="neptune",color=(56,68,227),density=1640,type="neptune",id=8))

        elif name == "empty" :
            self.objects = []

        elif name == "random1" :
            self.Simulation_speed = 3600
            for i in range(50):
                mass = random()**2 * 5 + 19
                sx , sy = randint(-1500,1500),randint(-1500,1500)
                self.objects.append(Objects(10**mass,randint(-10**9,10**9),randint(-10**9,10**9),sx , sy,color=(randint(0,255),randint(0,255),randint(0,255)),id=i+2,density=random()*10000,type='asteroid'))
            for i in range(50):
                mass = random()**2 * 5 + 22
                sx , sy = randint(-1500,1500),randint(-1500,1500)
                self.objects.append(Objects(10**mass,randint(-10**9,10**9),randint(-10**9,10**9),sx , sy,color=(randint(0,255),randint(0,255),randint(0,255)),id=i+102,density=random()*10000,type='exoplanet'))


        self.statu = "pause"        
        self.menu = "simulating"    
        self.mode = "none"
        self.define_textures(self.objects)



    def initialize_buttons(self):
        self.boutons = []
        self.boutons.append(Button(0  ,  100  ,  Constante.Bordure_y  ,  Constante.Bordure_y-100  ,  'self.back()','(self.menu != "simulating" and self.menu != "choosing_simulations")',type="short",color=(220, 24, 24),text=self.vocabulaire[self.langue][4],text_size=18))
        self.boutons.append(Button(0  ,  100  ,  Constante.Bordure_y  ,  Constante.Bordure_y-100  ,  'self.setting()','(self.menu == "simulating")',type="short",color=(192,192,192),text=self.vocabulaire[self.langue][3],text_size=16))
        self.boutons.append(Button(100  ,  250  ,  300  ,  150  ,  'self.video_setting()','(self.menu == "setting")',type="short",color=(192,192,192),text=self.vocabulaire[self.langue][14],text_size=13))
        self.boutons.append(Button(100  ,  250  ,  500  ,  350  ,  'self.controls_setting()','(self.menu == "setting")',type="short",color=(192,192,192),text=self.vocabulaire[self.langue][5],text_size=13))
        self.boutons.append(Button(100  ,  250  ,  700  ,  550  ,  'self.languages_setting()','(self.menu == "setting")',type="short",color=(192,192,192),text=self.vocabulaire[self.langue][44],text_size=13))

        # video settings
        self.boutons.append(Button(100  ,  175  ,  225  ,  150  ,  'self.fps_button()','(self.menu == "video_setting")',type="long"))
        self.boutons.append(Button(100  ,  175  ,  350  ,  275  ,  'self.coordonates_button()','(self.menu == "video_setting")',type="long"))
        self.boutons.append(Button(100  ,  175  ,  475  ,  400  ,  'self.version_button()','(self.menu == "video_setting")',type="long"))
        self.boutons.append(Button(100  ,  175  ,  600  ,  525  ,  'self.cycle_button()','(self.menu == "video_setting")',type="long",color_on=(30,190,255),color_off=(220, 240, 24),activated=False))
        self.boutons.append(Button(100  ,  175  ,  725  ,  650  ,  'self.activate_textures_button()','(self.menu == "video_setting")',type="long"))
        self.boutons.append(Button(900  ,  975  ,  225  ,  150  ,  'self.allways_visible_objects_button()','(self.menu == "video_setting")',type="long"))
        self.boutons.append(Button(900  ,  975  ,  350  ,  275  ,  'self.visible_trajectory_button()','(self.menu == "video_setting")',type="long"))

        # controls setting
        self.boutons.append(Button(100  ,  195  ,  245  ,  150  ,  'self.do_nothing_button()','(self.menu == "controls_setting")',type="short",color=(0,255,0),text_color=(0,145,255),text_size=16,text='A'))
        self.boutons.append(Button(100  ,  195  ,  370  ,  275  ,  'self.do_nothing_button()','(self.menu == "controls_setting")',type="short",color=(0,255,0),text_color=(0,145,255),text_size=16,text=self.vocabulaire[self.langue][11]))
        self.boutons.append(Button(100  ,  195  ,  495  ,  400  ,  'self.do_nothing_button()','(self.menu == "controls_setting")',type="short",color=(0,255,0),text_color=(0,145,255),text_size=16,text=self.vocabulaire[self.langue][9]))
        self.boutons.append(Button(100  ,  195  ,  620  ,  525  ,  'self.do_nothing_button()','(self.menu == "controls_setting")',type="short",color=(0,255,0),text_color=(0,145,255),text_size=16,text=self.vocabulaire[self.langue][7]))
        self.boutons.append(Button(100  ,  195  ,  745  ,  650  ,  'self.do_nothing_button()','(self.menu == "controls_setting")',type="short",color=(0,255,0),text_color=(0,145,255),text_size=16,text='P'))

        # choix de simulations 
        self.boutons.append(Button(435  ,  585  ,  750  ,  600  ,  'self.initialize_objects("solar_system")','(self.menu == "choosing_simulations")',type="short",color=(239,131,0,170),text_color=(0,145,255),text_size=15,text=self.vocabulaire[self.langue][0]))
        self.boutons.append(Button(735  ,  885  ,  750  ,  600  ,  'self.initialize_objects("empty")','(self.menu == "choosing_simulations")',type="short",color=(239,131,0,170),text_color=(0,145,255),text_size=15,text=self.vocabulaire[self.langue][1]))
        self.boutons.append(Button(1035  ,  1185  ,  750  ,  600  ,  'self.initialize_objects("random1")','(self.menu == "choosing_simulations")',type="short",color=(239,131,0,170),text_color=(0,145,255),text_size=15,text=self.vocabulaire[self.langue][2]))

        # choix de la langue 
        self.boutons.append(Button(100  ,  250  ,  500  ,  350  ,  'self.langue_button("français") ','(self.menu == "languages_setting")',type="short",color=(128,128,128),text="français",text_size=13))
        self.boutons.append(Button(100  ,  250  ,  700  ,  550  ,  'self.langue_button("english") ','(self.menu == "languages_setting")',type="short",color=(128,128,128),text="english",text_size=13))



    def initialize_labels(self):
        # crée les Labels 
        self.labels = []
        self.labels.append(Label(0,250,Constante.Bordure_y,Constante.Bordure_y-100,in_color=(30,30,30),screen_condition='(self.new_planet_statu == "caracteristique")',text=self.vocabulaire[self.langue][26],text_size=20,writing_only=True,type="new_planet_title"))
        self.labels.append(Label(0,250,Constante.Bordure_y,Constante.Bordure_y-100,in_color=(30,30,30),screen_condition='(self.menu == "choosing_simulations")',text="simulations",text_size=20,writing_only=True,type="choosing_simulation_title"))
        self.labels.append(Label(400,600,Constante.Bordure_y-700,Constante.Bordure_y-800,text="0",in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',  outline_color=(125,125,125),text_size=20,type="new_planet_speed"))
        self.labels.append(Label(400,600,Constante.Bordure_y-500,Constante.Bordure_y-600,text="5520",in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',  outline_color=(125,125,125),text_size=20,type="new_planet_density"))
        self.labels.append(Label(400,600,Constante.Bordure_y-300,Constante.Bordure_y-400,text="0",in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',  outline_color=(125,125,125),text_size=20,type="new_planet_mass"))
        self.labels.append(Label(1200,1400,Constante.Bordure_y-700,Constante.Bordure_y-800,text="",in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',outline_color=(125,125,125),text_size=20,type="new_planet_name"))
        self.labels.append(Label(1200,1400,Constante.Bordure_y-500,Constante.Bordure_y-600,text="(255,255,255)",in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',outline_color=(125,125,125),text_size=20,type="new_planet_color"))
        self.labels.append(Label(1200,1400,Constante.Bordure_y-300,Constante.Bordure_y-400,text=str(self.create_new_id()),in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',outline_color=(125,125,125),text_size=20,type="new_planet_id"))
        self.labels.append(Label(1200,1400,Constante.Bordure_y-100,Constante.Bordure_y-200,text="asteroid",in_color=(30,90,90),active_color=(30,90,30),screen_condition='(self.new_planet_statu == "caracteristique")',outline_color=(125,125,125),text_size=20,type="new_planet_type"))




#### Fonctions pour les boutons 


    def boutton_texture(self):
        pass



    def setting(self):
        if self.menu == "simulating" :
            self.menu = "setting"  
        else :
            self.menu = "simulating"
            
        self.statu = "pause"



    def video_setting(self):
        self.menu = "video_setting"



    def controls_setting(self):
        self.menu = "controls_setting"



    def languages_setting(self):
        self.menu = "languages_setting"



    def fps_button(self):
        self.visible_fps = not(self.visible_fps)



    def coordonates_button(self):
        self.visible_coordonates = not(self.visible_coordonates)



    def back(self):
        if self.menu == "setting" :
            self.menu = "simulating"
        elif self.menu == "video_setting":
            self.menu = "setting"
        elif self.menu == "controls_setting":
            self.menu = "setting"
        elif self.menu == "languages_setting":
            self.menu = "setting"



    def version_button(self):
        self.visible_version = not(self.visible_version)



    def cycle_button(self):
        self.enable_cycle = not(self.enable_cycle)



    def activate_textures_button(self):
        self.realistic_textures = not(self.realistic_textures)



    def allways_visible_objects_button(self):
        self.allways_visible_objects = not(self.allways_visible_objects)



    def visible_trajectory_button(self) :
        self.visible_trajectory = not(self.visible_trajectory)



    def langue_button(self,langue):
        self.langue = langue
        self.initialize_buttons()
        self.initialize_labels()



    def do_nothing_button(self):
        pass


game = MyGame(Constante.Bordure_x, Constante.Bordure_y , "N-Body-Simulation")
arcade.run()

