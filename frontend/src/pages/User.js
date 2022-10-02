import {useEffect, useState} from "react";
import Post from "../components/Post";
import {useParams} from "react-router";

export default function User(props) {
    const {id} = useParams()
    const [links, setLinks] = useState(null);
    const [user, setUser] = useState(false)


    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/get_gifs/${id}`).then(res=> res.json())
            .then(res => {
                setLinks(res);
                console.log(res.length)
            })


    }, [])
    useEffect(()=>{
        fetch(`http://127.0.0.1:5000/getUser/${id}`).then(res=> res.json())
            .then(res => {
                setUser(res['user']);
                console.log(res)
            })
    }, [])

    return (<div>
            {links !== null &&
                Array.from(Array(links['links'].length)).map((_, index) => (
                    <div>
                        <Post link={links['links'][index]} you={'his'}></Post>
                    </div>

                ))
            }
        </div>


    );
}
