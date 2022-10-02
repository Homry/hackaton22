import VideoFromDevice from "../components/VideoFromDevice";
import {useEffect, useState} from "react";

export default function Storage(props) {
    console.log(props.user['_id'])
    const [links, setLinks] = useState({'links':[]});
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/get_gifs/${props.user['_id']}`).then(res=> res.json())
            .then(res => {
                setLinks(res);
                console.log(res.length)
            })
    }, [])
    return (
        <>
            {
                Array.from(Array(links['links'].length)).map((_, index) => (
                    <div>
                        <img src={links['links'][index]}/>
                        <a href={links['download'][index]}>Скачать</a>
                    </div>

                ))
            }

        </>
    );
}
