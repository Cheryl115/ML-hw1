import random
import numpy as np
import matplotlib.pyplot as plt  
import time

def rand_seed(m, b, num=2):
    # create empty list
    x_coor = []
    y_coor = []
    label = []
    # positive and negtive point number
    pos_num = int(num / 2)
    neg_num = num - pos_num
    # random create point
    for i in range(pos_num):
        x = random.randint(0, num)
        r = random.randint(1, num)
        y = m * x + b - r
        # save the coordinate of x and y
        x_coor.append(x)
        y_coor.append(y)
        # save label, right=1, left=0
        label.append(1 if m >= 0 else -1)

    for i in range(neg_num):
        x = random.randint(0, num)
        r = random.randint(1, num)
        y = m * x + b + r
        x_coor.append(x)
        y_coor.append(y)
        label.append(-1 if m >= 0 else 1)
    return x_coor, y_coor, label

def PLA(x_coor, y_coor, label):
    # x: 1 * 30 y: 1 * 30 label: 1*30 
    # w: 1*2
    
    w = np.array([1,1])
    x_t = np.array([x_coor,y_coor])
    j = 0
    cnt = 0 # iteration
    while j < len(label):
        #print(j)
        for i in range(len(label)):
            cnt += 1

            if ((np.dot(w,x_t[:,i]))*label[i])<0:
                w = w + label[i]*x_t[:,i]
                j = 0
            elif j < len(label):
                j += 1
            else:
                # print(w)
                break
    


    return w.reshape(-1, 1), cnt

def error_rate(x_t,label,w):
    error = 0.0
    for i in range(len(label)):
        if ((np.dot(w,x_t[:,i]))*label[i])<0:
            error = error +1.0
    return error

def POCKET(x_coor, y_coor, label):
    # x: 1 * 30 y: 1 * 30 label: 1*30 
    # w: 1*2
    
    w = np.array([1,1])
    x_t = np.array([x_coor,y_coor])
    rand_sort = range(len(label))
    rand_sort = random.sample(rand_sort, len(label))
    
    j = 0
    error_w = error_rate(x_t,label,w)
    while (j<len(label)):
        #print(j)
        #print(len(label))
        for i in range(len(label)):
            k = rand_sort[i]
            if ((np.dot(w,x_t[:,k]))*label[k])<0:
                wt = w + label[k]*x_t[:,k]
                error_wt = error_rate(x_t,label,wt)
                j = 0

                if error_wt < error_w:
                    w = wt
                    break

            elif j < len(label):
                j += 1

            else:
                break

    
    #print(error_w)
    return w.reshape(-1, 1)

if __name__ == '__main__':
    tot_cnt = 0
    for turn in range(1, 4):
        plt.figure(turn)

        # set value of m and b 
        m, b = 1, 2
        # plot the function curve
        x = np.arange(30)   # x = [0, 1,..., 29]
        y = m * x + b
        plt.plot(x, y)
        # plot the random point
        # blue for positive and red for negative
        x_coor, y_coor, label = rand_seed(m, b, num=30)
        plt.plot(x_coor[:15], y_coor[:15], 'o', color='blue')
        plt.plot(x_coor[15:], y_coor[15:], 'o', color='red')
        plt.savefig('origin.jpg')

        w, cnt = PLA(x_coor,y_coor,label)
        # print(w.shape)
        
        # print(np.dot(w.T, tmp).shape)
        tmp = - (w[0] / w[1]) * x
        # print(tmp.shape)
        tot_cnt += cnt
        print(f'{turn}: {cnt}')

        plt.plot(x, tmp, color='#FF8888')
        plt.savefig(f'pla_t{turn}.jpg')

    print(f'average iteration: {tot_cnt/3:.2f}')


    # Pocket v.s. PLA
    turn += 1
    plt.figure(turn)

    # set value of m and b 
    m, b = 1, 2
    # plot the function curve
    x = np.arange(2000)   # x = [0, 1,..., 29]
    y = m * x + b
    plt.plot(x, y)
    # plot the random point
    # blue for positive and red for negative
    x_coor, y_coor, label = rand_seed(m, b, num=2000)
    plt.plot(x_coor[:1000], y_coor[:1000], 'o', color='blue')
    plt.plot(x_coor[1000:], y_coor[1000:], 'o', color='red')

    # PLA
    tic = time.process_time()
    w, cnt = PLA(x_coor,y_coor,label)
    tmp = - (w[0] / w[1]) * x
    plt.plot(x, tmp, color='#FF8888')
    toc = time.process_time()
    print(f"Run PLA Alogrithm in {toc - tic:0.4f} seconds")


    # Pocket
    tic = time.process_time()
    wt = POCKET(x_coor,y_coor,label)
    toc = time.process_time()
    print(f"Run POCKET Alogrithm in {toc - tic:0.4f} seconds")

    tmp = - (wt[0] / wt[1]) * x
        # print(tmp.shape)

    plt.plot(x, tmp, color='#3C3C3C')
    plt.savefig(f'pocket_pla.jpg')

    plt.show()
