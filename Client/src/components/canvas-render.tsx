import React, { useEffect, useRef } from 'react';
import styles from './styles.module.css';

type CanvasRenderProps = {
  style?: React.CSSProperties;
  videoRef: React.RefObject<HTMLVideoElement>;
};

export function CanvasRender(props: CanvasRenderProps) {
  const { videoRef, style } = props;
  const refCanvas = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!refCanvas.current) return;
    if (!videoRef.current) return;

    // Set the canvas size to be larger than the video size for higher resolution
    const scaleFactor = 2; // Adjust this factor for higher resolution
    refCanvas.current.width = videoRef.current.videoWidth * scaleFactor;
    refCanvas.current.height = videoRef.current.videoHeight * scaleFactor;
    const ctx = refCanvas.current.getContext('2d');
    let show = true;

    function processFrame() {
      if (!refCanvas.current) return;
      if (!videoRef.current) return;
      if (!ctx) return;
      if (!show) return;

      // Draw the current frame of the video on the canvas
      ctx.drawImage(videoRef.current, 0, 0, refCanvas.current.width, refCanvas.current.height);
      ctx.filter = 'blur(1px)'; // Apply a slight blur to smooth edges
      ctx.getContextAttributes().willReadFrequently = true;

      // Get image data from canvas
      const imageData = ctx.getImageData(0, 0, refCanvas.current.width, refCanvas.current.height);
      const data = imageData.data;

      // Process image data, remove green background
      for (let i = 0; i < data.length; i += 4) {
        const red = data[i];
        const green = data[i + 1];
        const blue = data[i + 2];

        // Refined green detection threshold
        if (green > 100 && red < 90 && blue < 90 && green > red + 30 && green > blue + 30) {
          data[i + 3] = 0; // Set the green background to transparent
        }
      }

      // Put the processed image data back into the canvas
      ctx.putImageData(imageData, 0, 0);

      // Continue processing the next frame
      requestAnimationFrame(processFrame);
    }

    // Start processing video frames
    processFrame();

    return () => {
      show = false;
    };
  }, [videoRef]);

  return <canvas className={styles.wrap} style={style} ref={refCanvas} />;
}
