import React, {useEffect, useState} from "react";
import Webcam from "react-webcam";

const COLORS = ["yellow", "green", "blue", "red", "purple", "pink", "gray"]
const TYPES = ["standard", "cat", "little_devil"]

export default function Video (props){
    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);
    const [colors, setColors] = useState([]);
    const [types, setTypes] = useState([true]);
    const [continue_, setContinue_] = useState(true);
    console.log(props.user)

    useEffect(()=>{
        let colors_arr = []
        let types_arr = []
        for (let color of COLORS){
            colors_arr.push(<option key={color} value={color}>{color}</option>)
        }
        for (let type of TYPES){
            types_arr.push(<option key={type} value={type}>{type}</option>)
        }
        setColors(colors_arr)
        setTypes(types_arr)
    },[])


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

        }

    }, [webcamRef, setImgSrc]);
    const capture = React.useCallback(async () => {
        const imageSrc = webcamRef.current.getScreenshot();

        const response = await fetch(`http://127.0.0.1:5000/convert_image?color=${document.querySelector('#color').value}&type=${document.querySelector('#type').value}`, {
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
            <select id="color">
                {colors}
            </select>
            <select id="type">
                {types}
            </select>
            <button onClick={()=>{capture()}}>preload</button>
            <button onClick={()=> window.location.reload()}>stop preload</button>
            <button onClick={save_gif}>create_gif</button>
            <button onClick={()=> {
                fetch(`http://127.0.0.1:5000/save_gif/${props.user['_id']}`).then(res => {
                    window.location.reload()
                })

            }}>save gif</button>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/png"
            />

            {imgSrc && (
                <img
                    src={imgSrc}
                />
            )}
        </>

    );
};
