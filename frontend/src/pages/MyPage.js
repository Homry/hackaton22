import {useEffect, useState} from "react";
import Post from "../components/Post";

export default function MyPage(props) {
    console.log(props.user)
    const [links, setLinks] = useState({'links':[]});
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/get_gifs/${props.user['_id']}`).then(res=> res.json())
            .then(res => {
                setLinks(res);

            })
    }, [])
    return (<div>
            {
                Array.from(Array(links['links'].length)).map((_, index) => (
                    <div>
                        <Post link={links['links'][index]} you={'you'}></Post>
                    </div>

                ))
            }
        </div>


    );
}
