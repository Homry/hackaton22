import React, {useEffect, useState} from "react";
import Webcam from "react-webcam";


const COLORS = {"yellow": "Желтый", "green": "Зеленый", "blue": "Синий", "red": "Красный", "purple": "Фиолетовый", "pink": "Розовый", "gray": "Серый"}
const TYPES = {"standard": "Стандартный", "cat":"Кот", "little_devil":"Дьяволенок"}

export default function Video (props){
    const webcamRef = React.useRef(null);
    const [imgSrc, setImgSrc] = React.useState(null);
    const [colors, setColors] = useState([]);
    const [types, setTypes] = useState([true]);
    const [continue_, setContinue_] = useState(true);

    useEffect(()=>{
        let colors_arr = []
        let types_arr = []
        for (let color of Object.keys(COLORS)){
            colors_arr.push(<option key={color} value={color}>{COLORS[color]}</option>)
        }
        for (let type of Object.keys(TYPES)){
            types_arr.push(<option key={type} value={type}>{TYPES[type]}</option>)
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
        if (continue_){
            save_gif()
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
        if (continue_){
            capture();
        }

    }, [webcamRef, setImgSrc]);

    return (

        <>

            <table>
                <tbody>
                <tr>
                    <select style={{background: "#333", color: "white"}} id="color">
                        {colors}
                    </select>
                    <select style={{background: "#333", color: "white"}} id="type">
                        {types}
                    </select>
                    <button style={{background: "#333", color: "white"}} onClick={()=>{capture()}}>Сгенерировать эмоцию</button>
                    <button style={{background: "#333", color: "white"}} onClick={()=> window.location.reload()}>Остановить</button>
                    <button style={{background: "#333", color: "white"}} onClick={save_gif}>Начать запись гифки</button>
                    <button style={{background: "#333", color: "white"}} onClick={()=> {
                        fetch(`http://127.0.0.1:5000/save_gif/${props.user['_id']}`).then(res => {
                            window.location.reload()
                        })
                    }}>Сохранить гифку</button>
                </tr>
                </tbody>
            </table>

            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/png"
                height={600}
            />

            {imgSrc && (
                <img
                    src={imgSrc}
                />
            )}
        </>

    );
};
