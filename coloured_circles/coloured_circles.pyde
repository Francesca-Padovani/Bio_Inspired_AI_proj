import csv

#setting the width and the height of our sketch pad
w, h = 1000, 1000


#defining the two functions which will allow us to plot the circles inside the setup function
def circle_two(x, y, r):
    circle_count = 10
    
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
    background(255, 255, 255) #setting the background colour
    #importing some global function in the local setup 
    global lista_x 
    global circle_two
    global circle_three
    
    #defining the three roots of interests, each one contains a best swarm 
    root = ["/Users/FrancescaPadovani/Desktop/MAGISTRALE_DATA SCIENCE/SECONDO ANNO/Secondo/BIO-INSPIRED_AI/proj_scripts_versione_finale/sample_colours0.csv", "/Users/FrancescaPadovani/Desktop/MAGISTRALE_DATA SCIENCE/SECONDO ANNO/Secondo/BIO-INSPIRED_AI/proj_scripts_versione_finale/sample_colours1.csv",
         "/Users/FrancescaPadovani/Desktop/MAGISTRALE_DATA SCIENCE/SECONDO ANNO/Secondo/BIO-INSPIRED_AI/proj_scripts_versione_finale/sample_colours2.csv"]
    
    #initializing lists thta will contain the coordinates x,y of the three swarms mentioned above
    lista_x = [] 
    lista_y = []   

    for ele in root:
        
        #reading each file and extracting the coordinates 
        reader = csv.reader(open(ele), delimiter = ',')
        x_vect = []
        y_vect = []
        for row in reader:
            x,y = float(row[1]), float(row[2])
            
            #we don't want overlapping coordinates, hence we exclude them applying this if condition
            if x not in x_vect and y not in y_vect:
                x_vect.append(x)
                y_vect.append(y)

        #I rescale the coordinates
        coordinates_x = [round(num*3.9) for num in x_vect]
        coordinates_y = [round(num*3.9) for num in y_vect]
        lista_x.append(coordinates_x)
        lista_y.append(coordinates_y)
        

    
    for i in range(3):
    
        #for the first swarm set the initial radius and the color 
        if i == 0:
            raggio = 2 
            stroke(10, 10, 200)
            
        #for the second swarm set the initial radius and the color 
        elif i == 1:
            raggio = 6
            stroke(10,200,10)
            
        #for the third swarm set the initial radius and the color     
        elif i == 2:
            stroke(200,10,10)
            raggio = 10
        
    
        coordinates_x = lista_x[i]
        coordinates_y = lista_y[i]
        
        for j in range(len(coordinates_x)):
            circle_three(coordinates_x[j], coordinates_y[j], raggio)
            raggio += 1
        
    save("prova_cerchi10.png")
    
    
