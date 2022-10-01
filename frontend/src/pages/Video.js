import React from "react";
import Webcam from "react-webcam";
import axios from "axios";

export default function Video (props){
    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);

    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        console.log(typeof(imageSrc))

        fetch(`http://127.0.0.1:5000/convert_image`, {
            method: "POST",
            body: JSON.stringify(imageSrc),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }).then(function (response){
            console.log('image res = ',response);
        })

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
