""" Uses camera and takes images for documentation of motion """
import requests
import time
from PIL import Image
import StringIO

user = "bergro"
pwd = "1240"


def fetch_snapshot_image():
    u = 'http://192.168.2.60/snapshot.cgi'
    r = requests.get(u, auth=(user, pwd), stream=True)
    if r.status_code == 200:
        imageData = StringIO.StringIO()
        imageData.write(r.raw)
        imageData.seek(0)
        return imageData
    return None


def compare(buffer1, buffer2, threshold=0):
    """
        diffs images by pixels and exits if diffs exceeds threshold
        code taken from script written by brainflakes posted at raspberry
        forum. http://www.raspberrypi.org/phpBB3/viewtopic.php?t=45235
    """
    # Count changed pixels
    changedPixels = 0
    print "In compare"
    for x in xrange(0, 100):
        # Scan one line of image then check sensitivity for movement
        for y in xrange(0, 75):
            # Just check green channel as it's the highest quality channel
            pixdiff = abs(buffer1[x, y][1] - buffer2[x, y][1])
            if pixdiff > threshold:
                changedPixels += 1


if __name__ == "__main__":
    print "Starting camera surv"
    counter = 0
    prev_img = None
    while counter < 50:
        img = fetch_snapshot_image()
        print "found img: %s" % img
        if img is not None and prev_img is not None:
            print "Doing comparison"
            im = Image.open(img)
            buf = im.load()
            prev_im = Image.open(prev_img)
            prev_buf = prev_im.load()
            print "Diff in images is: %s" % compare(prev_img, img)
            im.close()
            prev_im.close()
        prev_img = img
        time.sleep(1)
