import VideoFromDevice from "../components/VideoFromDevice";
import {useEffect, useState} from "react";
import Post from "../components/Post";


export default function Storage(props) {
    const [users, setUsers] = useState(null)
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/getAllUsers/${props.user['_id']}`).then(res=> res.json())
            .then(res => {
                setUsers(res['users']);
                console.log(res['users']);
            })
    },[])
    if (users !== null){
        return (
            <>
                {Array.from(Array(users.length)).map((_, index) => (
                    <div>
                        <a href={`/page/${users[index]['_id']}`}> {users[index]['name']}</a>
                    </div>

                ))}
            </>
        )
    }



}
