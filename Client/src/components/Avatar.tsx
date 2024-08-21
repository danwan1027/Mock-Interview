import { useEffect, useRef, useState } from 'react';
import { Configuration, NewSessionData, StreamingAvatarApi } from '@heygen/streaming-avatar';
import '../App.css';
import '../interview_questioning.css';
import { CanvasRender } from "../components/canvas-render";

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
  

  const addNumbers = () => {
    axios.post('http://127.0.0.1:3001/api/add', {
      num1: 5,
      num2: 10
    })
      .then(response => {
        setSumResult(response.data.result);
      })
      .catch(error => {
        console.error('There was an error adding the numbers!', error);
      });
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

  async function grab() {
    await updateToken();

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
    await avatar.current.speak({ taskRequest: { text: text, sessionId: data?.sessionId } }).catch((e) => {
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
        {helloMessage}
      </div>
      <div className="images" >
        <div className="image_frame" >
          <video playsInline autoPlay width={300} ref={mediaStream} style={{ display: 'none' }} onCanPlay={() => {
            setCanPlay(true)
          }} />
          {canPlay && <CanvasRender videoRef={mediaStream} />}
        </div>

        <div className="image_frame">
          camera show here
        </div>



      </div>
      <input className="InputField" placeholder='Type something for the avatar to say' value={text} onChange={(v) => setText(v.target.value)} />
      <button className="continue-btn" onClick={grab}>啟動</button>
      <button className="continue-btn" onClick={handleSpeak}>說話</button>
      <button className="continue-btn">繼續</button>
    </div>

    // {/* <div className="HeyGenStreamingAvatar">
    //   <div>
    //   <button onClick={addNumbers}>Add Numbers</button>
    //   {sumResult !== null && <h2>Result: {sumResult}</h2>}
    // </div>
    // </div> */}
  );
}

export default Avatar;