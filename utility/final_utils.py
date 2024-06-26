import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns 

sns.set_theme(style='whitegrid')

def read_coordinates(filename,split_idx):
    coordinates = []
    with open(filename,'r') as coord_file:
        while True:
            p = coord_file.readline().strip('\n')
            if p == '':
                break
            try:
                x,y = p.split('\t')
                coordinates.append((float(x),float(y)))
            except ValueError:
                split_idx = int(p)
    left_pupil = coordinates.pop() # last coord
    right_pupil = coordinates.pop() # before last coord 
    upper_right_contour = coordinates[:split_idx]
    upper_left_contour = coordinates[split_idx:]
    return upper_right_contour,upper_left_contour, right_pupil,left_pupil
            

def choose_best_fit_degree(contour,degree):
    x = [c[0]/100 for c in contour]
    y = [c[1]/100 for c in contour]
    p = np.polyfit(x,y,degree)
    return x , np.poly1d(p)

def compute_similarity(right_eye_feature,left_eye_feature,ptotic):
    if ptotic == 'r':
        return f"{round(100 * right_eye_feature / left_eye_feature,2)}%"
    else:
        return f"{round(100 * left_eye_feature / right_eye_feature,2)}%"

def plot_contour(right_contour,left_contour,right_pupil,left_pupil,ptotic,degree,title):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if not ax.yaxis_inverted():
        ax.invert_yaxis()
    
    ax.scatter(right_pupil[0]/100,right_pupil[1]/100,c='r')
    ax.scatter(left_pupil[0]/100,left_pupil[1]/100,c='b')
    

    #################### CHOOSING THE FIT ##########################
    x_right,fx = choose_best_fit_degree(right_contour,degree)
    #print(f"Equation of the right eye : \n {fx}")
    x_left,gx = choose_best_fit_degree(left_contour,degree)
    #print(f"Equation of the left eye: \n {gx}")

    #################### PLOTTING THE FIT ##########################
    x_right_new = np.linspace(min(x_right),max(x_right),100)
    y_right_new = fx(x_right_new)
    
   
    
    ax.plot(x_right_new,y_right_new,c='r')

    x_left_new = np.linspace(min(x_left),max(x_left),100)
    y_left_new = gx(x_left_new)
    ax.plot(x_left_new,y_left_new,c='b')

    
    ## MRD plot line
    ax.plot([right_pupil[0]/100,right_pupil[0]/100], [right_pupil[1]/100,fx(right_pupil[0]/100) ], linestyle='--',color='r')
    ax.plot([left_pupil[0]/100,left_pupil[0]/100], [left_pupil[1]/100,gx(left_pupil[0]/100) ], linestyle='--',color='b')
    
    # PHUL plotline
    ax.plot([x_right_new[np.argmin(fx(x_right_new))],x_right_new[np.argmin(fx(x_right_new))]],[min(fx(x_right_new)),right_pupil[1]/100],linestyle='--',color='r')
    ax.plot([x_left_new[np.argmin(gx(x_left_new))],x_left_new[np.argmin(gx(x_left_new))]],[min(gx(x_left_new)),left_pupil[1]/100],linestyle='--',color='b')
    #plot title
    ax.set_title(title)


    ######################### MRD1 , PHUL , Similarity ############################
    ########################### MRD1 ##################################
    mrd1_right = abs(round(10*(fx(right_pupil[0]/100) - right_pupil[1]/100),2))
    #print(f"MRD1 right eye : {mrd1_right} mm" )

    mrd1_left = abs(round(10*(gx(left_pupil[0]/100) - left_pupil[1]/100),2))
    #print(f"MRD1 left eye : {mrd1_left} mm" )

    ########################### PHUL ##################################
    mrd1phul_right = abs(x_right_new[np.argmin(fx(x_right_new))] - right_pupil[0]/100)
    #print(f"PHUL - MRD1 right_eye: {round(mrd1phul_right,5)*10} mm")

    mrd1phul_left = abs(x_left_new[np.argmin(gx(x_left_new))] - left_pupil[0]/100)

    #print(f"PHUL - MRD1 left_eye: {round(mrd1phul_left,5)*10} mm")

    ########################### SIMILARITY ##################################
    #print(f"Similarity between MRD1 in both eyes :{compute_similarity(mrd1_right,mrd1_left,ptotic)} %")
    #print(f"Similarity between PHUL - MRD1 in both eyes :{compute_similarity(mrd1phul_right,mrd1phul_left,ptotic)} %") 

    return fx,gx,mrd1_right,mrd1_left,mrd1phul_right,mrd1phul_left