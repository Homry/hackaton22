import React, {useEffect, useState} from "react";
import Webcam from "react-webcam";


export default function Video (props){
    useEffect(() => {
        fetch(`http://127.0.0.1:5000/delete_img/${props.user['_id']}`).then()
    }, [props.user])

    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);
    const [continue_, setContinue_] = useState(true);
    console.log(props.user)
    const save_gif = React.useCallback(async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        const response = await fetch(`http://127.0.0.1:5000/convert_image/${props.user['_id']}`, {
            method: "POST",
            body: JSON.stringify(imageSrc),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        const content = await response.blob();
        setImgSrc(URL.createObjectURL(content))
        console.log(continue_)
        if (continue_){
            save_gif()
        }

    }, [webcamRef, setImgSrc]);
    const capture = React.useCallback(async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        const response = await fetch(`http://127.0.0.1:5000/convert_image`, {
            method: "POST",
            body: JSON.stringify(imageSrc),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
        const content = await response.blob();
        setImgSrc(URL.createObjectURL(content))
        console.log(continue_)
        if (continue_){
            capture();
        }

    }, [webcamRef, setImgSrc]);

    return (

        <>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/png"
            />
            <button onClick={capture}>preload</button>
            <button onClick={()=> window.location.reload()}>stop preload</button>
            <button onClick={save_gif}>create_gif</button>
            <button onClick={()=> {
                fetch(`http://127.0.0.1:5000/save_gif/${props.user['_id']}`).then(res => {
                    window.location.reload()
                })

            }}>save gif</button>
            {imgSrc && (
                <img
                    src={imgSrc}
                />
            )}
        </>

    );
};
