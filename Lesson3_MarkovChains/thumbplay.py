import sys
import os
import Image
import pickle

if __name__ == '__main__':
    count = 0

    NUM_BLOCKS = 145
    BLOCK_SIZE = 10
    try:
        averages = pickle.load(open('averages.pickle'))
    except IOError:
        averages = {}

    print len(averages.keys())
    
    out_size = (NUM_BLOCKS*BLOCK_SIZE, NUM_BLOCKS*BLOCK_SIZE)
    out_im = Image.new("RGB", out_size, "black")
    out_pix = out_im.load()

    for filename in os.listdir('./thumbs/'):
        print filename

        if filename in averages.keys():
            avg = averages[filename]
        else:
            im = Image.open('./thumbs/' + filename)
            (x_size, y_size) = im.size
            pixels = {'r':[], 'g':[], 'b':[] }
            for x in range(x_size):
                for y in range(y_size):
                    try:
                        (r, g, b) = im.getpixel((x, y))
                        pixels['r'].append(float(r))
                        pixels['g'].append(float(g))
                        pixels['b'].append(float(b))
                    except TypeError:
                        pass

            try:
                avg = (int(sum(pixels['r'])/len(pixels['r'])), 
                      int(sum(pixels['g'])/len(pixels['g'])),
                      (int(sum(pixels['b'])/len(pixels['b']))))
            except ZeroDivisionError:
                avg = (0,0,0)

            averages[filename] = avg

        if count < NUM_BLOCKS:
            x_count = count
            y_count = 0
        else:
            x_count = count % NUM_BLOCKS
            y_count = int(count / NUM_BLOCKS)

        print x_count
        print y_count

        for out_x in range(x_count*BLOCK_SIZE, (x_count*BLOCK_SIZE+BLOCK_SIZE)):
            for out_y in range(y_count*BLOCK_SIZE, (y_count*BLOCK_SIZE+BLOCK_SIZE)):
                out_pix[out_x,out_y] = avg

        count += 1
        if (count % 100) == 1:
            print "saving!"
            pickle.dump(averages, open('averages.pickle','wb'))

    out_im.show()
    out_im.save("averages.png")
    pickle.dump(averages, open('averages.pickle','wb'))
