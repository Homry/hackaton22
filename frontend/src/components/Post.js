import React from "react";

export default function Post(props){
    return(
        <div>
            <p>{props.you} create emotion</p>
            <img src={props.link}/>
        </div>
    )
}