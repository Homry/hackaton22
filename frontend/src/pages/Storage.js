import VideoFromDevice from "../components/VideoFromDevice";
import {useEffect} from "react";

export default function Storage(props) {
    console.log(props.user['_id'])
    
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/get_gifs/${props.user['_id']}`).then(res=> res.json())
            .then(res => console.log(res))
    }, [])
    return (
            <h1>hello</h1>
    );
}
