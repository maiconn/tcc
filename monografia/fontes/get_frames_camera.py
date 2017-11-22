def get_frames():
    with picamera.PiCamera() as camera:
        time.sleep(2)
        stream = io.BytesIO()
        camera.resolution = (160, 120)
        for foo in camera.capture_continuous(stream, 'jpeg',
                                             use_video_port=True):
            if BaseCamera.stopped:
                break
            stream.seek(0)
            yield stream.read()
            stream.seek(0)
            stream.truncate()


            