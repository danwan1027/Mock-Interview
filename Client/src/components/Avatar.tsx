import { useEffect, useRef, useState } from 'react';
import { Configuration, NewSessionData, StreamingAvatarApi } from '@heygen/streaming-avatar';
import '../App.css';
import '../interview_questioning.css';
import { CanvasRender } from "../components/canvas-render";
import { Interface } from 'readline';

function Avatar() {
  const [stream, setStream] = useState<MediaStream>();
  const [debug, setDebug] = useState<string>();
  const [text, setText] = useState<string>("");
  const [avatarId, setAvatarId] = useState<string>("");
  const [voiceId, setVoiceId] = useState<string>("");
  const [data, setData] = useState<NewSessionData>();
  const [initialized, setInitialized] = useState(false); // Track initialization
  const mediaStream = useRef<HTMLVideoElement>(null);
  const avatar = useRef<StreamingAvatarApi | null>(null);
  const mediaRecorder = useRef<MediaRecorder | null>(null);
  const audioChunks = useRef<Blob[]>([]);
  const [canPlay, setCanPlay] = useState(false)


  const [helloMessage, setHelloMessage] = useState('');
  const [sumResult, setSumResult] = useState(null);
  const [imgSrc, setImgSrc] = useState<string>('');

  // 前端紀錄面試資料
  let count: number = 1;
  const [questionText, setQuestionText] = useState<string>(''); // 這裡定義 questionText 狀態
  const [interviewId, setInterviewId] = useState<string>('');
  const [questionId, setQuestionId] = useState<string>('');

  //面試校系
  const [department, setDepartment] = useState<string>('');
  const [school, setSchool] = useState<string>('');



  useEffect(() => {
    ///////////////////////////// talk with flask  /////////////////////////////
    fetch('http://127.0.0.1:3001/api/hello')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then(data => {
        setHelloMessage(data.message);
      })
      .catch(error => {
        console.error('There was an error fetching the greeting!', error);
      });
  }, []);

  const startRecording = async () => {
    try {
      await fetch('http://127.0.0.1:3001/start_recording');
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };
  const stopRecording = async () => {
    try {
      await fetch('http://127.0.0.1:3001/stop_recording',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ interview_id: interviewId, question_id: questionId, questionText: questionText, school: school, department: department})
      });
    } catch (error) {
      console.error('Error ending recording:', error);
    }
  };

  const startCamera = () => {
    fetch('http://127.0.0.1:3001/start_camera', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ count: count , school: school, department: department})
    })
      .then(response => response.json())
      .then(data => {
        setInterviewId(data.interview_id);
        setQuestionText(data.question);
        setQuestionId(data.question_id);
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

  ///////////////////////////// talk with flask  /////////////////////////////


  async function fetchAccessToken() {
    try {
      const response = await fetch('http://localhost:3001/get-access-token', {
        method: 'POST'
      });
      const result = await response.json();
      const token = result.token; // Access the token correctly
      console.log('Access Token:', token); // Log the token to verify
      return token;
    } catch (error) {
      console.error('Error fetching access token:', error);
      return '';
    }
  }

  async function activate() {
    await updateToken();
    startCamera();
    count++;

    if (!avatar.current) {
      setDebug('Avatar API is not initialized');
      return;
    }

    try {
      const res = await avatar.current.createStartAvatar(
        {
          newSessionRequest: {
            quality: "low",
            avatarName: avatarId,
            voice: { voiceId: '4158cf2ef85d4ccc856aacb1c47dbb0c' }
            // Joon-insuit-20220821  josh_lite3_20230714
            // voice: { voiceId: '3b1633a466c44379bf8b5a2884727588' }
          }
        }, setDebug);
      setData(res);
      setStream(avatar.current.mediaStream);
    } catch (error) {
      console.error('Error starting avatar session:', error);
    }
  };

  async function updateToken() {
    const newToken = await fetchAccessToken();
    console.log('Updating Access Token:', newToken); // Log token for debugging
    avatar.current = new StreamingAvatarApi(
      new Configuration({ accessToken: newToken })
    );

    const startTalkCallback = (e: any) => {
      console.log("Avatar started talking", e);
    };

    const stopTalkCallback = (e: any) => {
      console.log("Avatar stopped talking", e);
    };

    console.log('Adding event handlers:', avatar.current);
    avatar.current.addEventHandler("avatar_start_talking", startTalkCallback);
    avatar.current.addEventHandler("avatar_stop_talking", stopTalkCallback);

    setInitialized(true);
  }


  async function handleSpeak() {
    if (!initialized || !avatar.current) {
      setDebug('Avatar API not initialized');
      return;
    }
    //將要念的文字設定為textToSpeak，並透過question_text賦值
    const textToSpeak = questionText || 'No question to ask';
    await avatar.current.speak({ taskRequest: { text: textToSpeak, sessionId: data?.sessionId } }).catch((e) => {
      setDebug(e.message);
    });
  }




  useEffect(() => {
    async function init() {
      const newToken = await fetchAccessToken();
      console.log('Initializing with Access Token:', newToken); // Log token for debugging
      avatar.current = new StreamingAvatarApi(
        new Configuration({ accessToken: newToken, jitterBuffer: 200 })
      );
      setInitialized(true); // Set initialized to true
    };
    init();
  }, []);

  useEffect(() => {
    if (stream && mediaStream.current) {
      mediaStream.current.srcObject = stream;
      mediaStream.current.onloadedmetadata = () => {
        mediaStream.current!.play();
        setDebug("Playing");
      }
    }
  }, [mediaStream, stream]);



  return (
    <div className="container">
      {debug}

      <div className="question">
        {questionText}
      </div>
      <div className="images" >
        <div className="image_frame" >
          <video playsInline autoPlay width={300} ref={mediaStream} style={{ display: 'none' }} onCanPlay={() => {
            setCanPlay(true)
          }} />
          {canPlay && <CanvasRender videoRef={mediaStream} />}
        </div>

        <div className="image_frame">
          {imgSrc ? (
            <img
              id="video-stream"
              className="video-stream"
              src={imgSrc}
              alt="Video Stream"
            />
          ) : null}
        </div>
      </div>
      {/* <input className="InputField" placeholder='Type something for the avatar to say' value={text} onChange={(v) => setText(v.target.value)} /> */}
      <div className="button-container">
        <div>
          <button className="btn" onClick={activate} >啟動</button>
          <button className="btn" onClick={handleSpeak}>說話</button>
          <button className="btn" onClick={startRecording}>開始回答</button>
          <button className="btn" onClick={stopRecording}>結束回答</button>
        </div>
        <div>
          <button className="btn" >繼續</button>
          <button className="btn" onClick={endCamera}>結束</button>
        </div>
      </div>


    </div>

  );
}

export default Avatar;