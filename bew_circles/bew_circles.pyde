import csv

#defining the height and the width of our sketch pad
w, h = 1000, 1000

#here we define the two functions which will enable us to plot the circles 
def circle_two(x, y, r):
    circle_count = 20
    
    pushMatrix()
    translate(x, y)
    circle(0, 0, r)
    noFill()
    for i in range(circle_count):
        rotate(random(2*PI))
        cent = int(random(0, r/2))

        circle(0, cent, r - (cent * 2))
        
        
    popMatrix()
    
def circle_three(x, y, r):
    circle_count = 10
    
    pushMatrix()
    translate(x, y)
    circle(0, 0, r)
    noFill()
    for i in range(circle_count):
        rotate(random(2*PI))
        cent = int(random(0, r/10))

        circle(0, cent, r - (cent * 2))
        
        
    popMatrix()
    
    

def setup():
    size(w, h)
    background(255, 255, 255) #define the background colour
    
    #import the global functions inside the setup local area
    global circle_two
    global circle_three
    
    #define the directory of the file where the best swarm is stored
    filename = '/Users/FrancescaPadovani/Desktop/MAGISTRALE_DATA SCIENCE/SECONDO ANNO/Secondo/BIO-INSPIRED_AI/proj_scripts_versione_finale/sample_swarm.csv'
    
    #initialize the reader
    reader = csv.reader(open(filename), delimiter = ',')
    
    #iterate through the lines of the file and collect the coordinates (x,y) of the particles
    #store them in two vectors 
    x_vect = []
    y_vect = []
    for row in reader:
        x,y = float(row[1]), float(row[2])
    
        #avoid overlapping positions of the particles 
        if x not in x_vect and y not in y_vect:
            x_vect.append(x)
            y_vect.append(y)
    
    
    #rescale the variables 
    coordinates_x = [round(num*3.8) for num in x_vect]
    coordinates_y = [round(num*3.8) for num in y_vect]

    #you could uncomment the code to try plotting normal circles or circle_two
    
        
    '''for c in range(len(coordinates_x)): 
        cs = 20
        fill(20, 20, 20, 15)
        for i in range(40):
            circle(coordinates_x[c], coordinates_y[c], cs-i*1)
            
            #fill(random(50,255), random(50,255), random(200,255))
            #circle(coordinates_x[c] - 10 , coordinates_y[c] - 10, cs)
        
    
    save("prova_shadow.png")
    
    raggio = 10 
    
    for i in range(len(coordinates_x)):
        circle_two(coordinates_x[i], coordinates_y[i], raggio)
        raggio += 1
        
    save("prova_cerchi2.png")'''
        
    #I choose to plot my cicles with circle_three style
    raggio = 10
    for i in range(len(coordinates_x)):
        circle_three(coordinates_x[i], coordinates_y[i], raggio)
        raggio += 1
        
    save("prova_cerchi9.png")
                       
