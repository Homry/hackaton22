import React, {useState} from "react";
import Webcam from "react-webcam";



export default function Video (props){
    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);
    const [link, setLink] = useState(null);

    const capture = React.useCallback(async () => {
        const imageSrc = webcamRef.current.getScreenshot();
        console.log(typeof (imageSrc))

        const response = await fetch(`http://127.0.0.1:5000/convert_image`, {
            method: "POST",
            body: JSON.stringify(imageSrc),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        const content = await response.blob();
        console.log(content)
        setImgSrc(URL.createObjectURL(content))

    }, [webcamRef, setImgSrc]);

    return (
        <>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/png"
            />
            <button onClick={capture}>Capture photo</button>
            {imgSrc && (
                <img
                    src={imgSrc}
                />
            )}
        </>

    );
};
