import { useState } from 'react';

function CameraControl() {
  const [imgSrc, setImgSrc] = useState<string>('');

  const startCamera = () => {
    fetch('http://127.0.0.1:3001/start_camera')
      .then(response => response.text())
      .then(() => {
        setImgSrc("http://127.0.0.1:3001/video_feed");
      })
      .catch(error => console.error('Error starting camera:', error));
  };

  const endCamera = () => {
    fetch('http://127.0.0.1:3001/just_end_camera')
      .then(response => response.text())
      .then(() => {
        setImgSrc('');  // Clear the image source to stop displaying the video
      })
      .catch(error => console.error('Error ending camera:', error));
  };

  return { imgSrc, startCamera, endCamera };
}

export default CameraControl;
