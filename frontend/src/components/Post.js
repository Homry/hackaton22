import React from "react";
import {saveAs} from 'file-saver'

export default function Post(props){
    return(
        <div>
            <p>{props.you} create emotion</p>
            <img style={{left: "33%"}} src={props.link}/>
            {props.you === 'you' &&
                <a style={{background: "#04AA6D", color: "white", left: "33%"}} href='#' onClick={()=>saveAs(props.link)}>Download</a>
            }

        </div>
    )
}