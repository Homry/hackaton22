import VideoFromDevice from "../components/VideoFromDevice";
import {useEffect, useState} from "react";

export default function Storage(props) {
    console.log(props.user['_id'])
    const [links, setLinks] = useState([]);
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/get_gifs/${props.user['_id']}`).then(res=> res.json())
            .then(res => {
                setLinks(res['links']);
                console.log(res['links'])
            })
    }, [])
    return (
        <>
            {
                Array.from(Array(links.length)).map((_, index) => (
                    <img src={links[index]}/>
                ))
            }

        </>
    );
}
