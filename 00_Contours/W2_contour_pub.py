#!/usr/bin/env python3

# Finding contours from an image and publishing to a rostopic

# Import the necessary libraries
import rospy  # Python library for ROS
from sensor_msgs.msg import Image  # Image is the message type
from cv_bridge import CvBridge  # Package to convert between ROS and OpenCV Images
import cv2  # OpenCV library
import numpy as np  # Numpu library
from std_msgs.msg import String
import argparse


def publish_message():

    # Node is publishing to the video_frames topic using
    # the message type Image
    pub = rospy.Publisher('image', Image, queue_size=1000)

    # Node is publishing contours
    pub_contours = rospy.Publisher('contours', String, queue_size=1000)

    # Node is publishing image size
    pub_size = rospy.Publisher('image_size', String, queue_size=1000)

    # Tells rospy the name of the node.
    # Anonymous = True makes sure the node has a unique name. Random
    # numbers are added to the end of the name.blurred
    rospy.init_node('image_pub_py', anonymous=True)

    # the message type Image
    pub_thresh = rospy.Publisher('image_thresh', Image, queue_size=1000)

    # the message type Image Color
    pub_color = rospy.Publisher('image_color', String, queue_size=1000)

    # Go through the loop n times per second
    rate = rospy.Rate(0.2)

    # Used to convert between ROS and OpenCV images
    br = CvBridge()

    # While ROS is still running.
    while not rospy.is_shutdown():

        # Capture image
        image = cv2.imread(
            '/home/angel/ur_ws/src/cv_basics/scripts/image02.JPG')
        print(type(image))

        # if image is loaded
        if image is not None:
            # Print debugging information to the terminal
            rospy.loginfo('publishing image')

            # Resize Image
            scale_percent = 65  # percent of original size
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            resizedArea = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

            # Convert the image to grayscale
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

            # cv2.imshow("Resized image", resized)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Apply binary threshold on the image
            # https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
            ret, thresh = cv2.threshold(gray, 120, 255, 0)
            pub_thresh.publish(br.cv2_to_imgmsg(thresh))
            cv2.imshow("Threshold", thresh)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Apply erosion algorithm to remove small noises
            kernel = np.ones((9, 9), np.uint8)
            img_erosion = cv2.erode(thresh, kernel, iterations=1)
            # cv2.imshow("Erosion", img_erosion)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Apply blurring to soften the edges
            blurred = cv2.GaussianBlur(
                img_erosion, (11, 11), cv2.BORDER_DEFAULT)

            # Find Contours on the blurred image
            a, contours, hierarchy = cv2.findContours(
                blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.imshow("Blurred", blurred)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Remove small contours
            final_contours = []
            for index, cnt in enumerate(contours):
                # if the contour has no other contours inside of it
                if hierarchy[0][index][2] == -1:
                    # if the size of the contour is greater than a threshold
                    if cv2.contourArea(cnt) > 2000:
                        final_contours.append(cnt)

            # simplify the tree structure for contours array
            coordinates = []
            for cnt in final_contours:
                coordinates.append(np.squeeze(cnt, axis=(1,)))

            # simplify the contours (reduce resoloution)
            boundaries = []
            for cnt in coordinates:
                boundaries.append(cv2.approxPolyDP(cnt, 7, True))

            # draw the contours on the image
            for crv in boundaries:
                cv2.drawContours(resized, [crv], 0, (0, 0, 255), 3)
                cv2.drawContours(resizedArea, [crv], 0, (200, 200, 200), 2)
            cv2.imshow('Contours', resized)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # Center of contour
            # compute the center of the contour

            color_msg = ''
            for ind, c in enumerate(contours):
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                print(resized[cY, cX])
                print(resized.shape)

                # Get Colors
                # print (cx, cy)
                (b, g, r) = image[int(cY), int(cX)]
                print(b, g, r)
                colortext = str(b) + "," + str(g) + "," + str(r)
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (cX, cY)
                # fontScale
                fontScale = .4
                # Red color in BGR
                color = (0, 0, 255)
                # Line thickness of 2 px
                thickness = 2
                cv2.putText(resized, colortext, (cX, cY), font,
                            fontScale, color, thickness, cv2.LINE_AA, False)

                color_msg += colortext + ';'

            pub_color.publish(color_msg)

            # draw the contour and center of the shape on the image
            cv2.drawContours(resized, [crv], 0, (0, 0, 255), 3)
            cv2.drawContours(resizedArea, [crv], 0, (200, 200, 200), 2)
            cv2.circle(resized, (cX, cY), 7, (217, 23, 23), -1)

            # Area of contours
            area = cv2.contourArea(contours[True])

            # Display index of contours
            cv2.drawContours(resized, [crv], 0, (0, 0, 255), 3)
            cv2.drawContours(resizedArea, [crv], 0, (200, 200, 200), 2)
            cv2.putText(resized, "#{}".format(ind), (cX - 20, cY + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 252, 252), 2)
            cv2.putText(resizedArea, "#{}".format(
                area), (cX - 20, cY + 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 252, 252), 2)

            cv2.imshow('Center', resized)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            cv2.imshow('Area', resizedArea)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # detect colors of the image

            # Publish the image.
            # The 'cv2_to_imgmsg' method converts an OpenCV image to a ROS image message
            pub.publish(br.cv2_to_imgmsg(image))

            # Publish the coordinates
            final_msg = ''
            for boundary in boundaries:
                simplified = np.squeeze(boundary, axis=(1))
                crds_list = simplified.tolist()
                str_list = []
                for i in simplified:
                    x = i[0]
                    y = i[1]
                    str_list.append(str(x)+','+str(y))
                msg = '+'.join([str(elem) for elem in str_list])
                final_msg += msg + ';'
            pub_contours.publish(final_msg)

            # Publish the image size
            img_size = str(image.shape[0]) + ',' + str(image.shape[1])
            pub_size.publish(img_size)
        else:
            rospy.loginfo('image not found')
        # Sleep just enough to maintain the desired rate
        rate.sleep()


if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass
