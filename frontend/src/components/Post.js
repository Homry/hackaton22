import React from "react";
import {saveAs} from 'file-saver'

export default function Post(props){
    return(
        <div>
            <p>{props.you} create emotion</p>
            <img src={props.link}/>
            <a href='#' onClick={()=>saveAs(props.link)}>Download</a>
        </div>
    )
}