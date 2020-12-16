import cv2 
import numpy as np

def extractChannel(image,channel):
    return image[:,:,channel]

def applyKernel(image, kernel,strides=1):
    kernel = np.flipud(np.fliplr(kernel))
    xKernShape = kernel.shape[0] 
    yKernShape = kernel.shape[1] 
    output = np.zeros((image.shape[0], image.shape[1]))
    for y in range(image.shape[1]):
        if y > image.shape[1] - yKernShape: 
            break
        if y % strides == 0:
            for x in range(image.shape[0]):
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    if x % strides == 0:
                        #apply convolution
                        output[x, y] = (kernel * image[x: x + xKernShape, y: y + yKernShape]).sum()
                except:
                    break
    print(output.shape)
    return output

def write_imag_to_file(imag,file_name):
    f = open(file_name, "w")
    for line in imag:
        for el in line:
            f.write(str(el)+" ")
        f.write("\n")
    f.close()

if __name__ == '__main__':

    #path to input image
    inp=cv2.imread('input.jpg')
    
    #write_imag_to_file(out,"inp.txt")

    split_imag=[]

    kernel_sharpen = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    kernel_iden = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    kernel_blurr_3 = np.array([[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]])
    kernel_blurr_4 = np.array([[1/16, 1/16, 1/16, 1/16], [1/16, 1/16, 1/16, 1/16], [1/16, 1/16, 1/16, 1/16], [1/16, 1/16, 1/16, 1/16]])
    kernel_remove=np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    #kernel = np.array([[1, 0, -1], [0, -1, 1], [-1, 1, 0]])
    kernel_edge = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    #kernel = np.array([[-1, -1, -1, -1], [-1, 3, 3, -1], [-1, 3, 3,-1],[-1, -1, -1,-1]])
    kernel=[]
    kernel.append(kernel_sharpen)#b
    kernel.append(kernel_sharpen)#g
    kernel.append(kernel_sharpen)#r

    #different kernels for each color channel
    for i in range(3):
        image = extractChannel(inp,i)
        output = applyKernel(image, kernel[i])
        split_imag.append(output)

    print(np.array(split_imag).shape)

    print(str(len(split_imag[0]))+" "+str(len(split_imag[0][0])))


    #combine convoluted channels back into a single image
    conv=np.zeros([len(split_imag[0]), len(split_imag[0][0]),3], dtype=int)
    for w in range(len(split_imag[0])):
        for h in range(len(split_imag[0][0])):
            r=split_imag[2][w][h]
            g=split_imag[1][w][h]
            b=split_imag[0][w][h]
            conv[w][h]=[b,g,r]
            
    #write_imag_to_file(conv,"out.txt")
    print(conv.shape)

    #output image name
    cv2.imwrite('output.jpg', conv)
