import { Route, BrowserRouter, Routes } from "react-router-dom";
import React, {useEffect, useState} from "react";
import Login from "./login/Login";
import Chat from "./pages/Chat";
import Video from "./pages/Video";
import Storage from "./pages/Storage";
import MyPage from "./pages/MyPage";
import useToken from "./login/useToken";
import Basic from "./pages/Basic";


function App() {
   const {token, setToken} = useToken();
    console.log("token___", token)
    if (!token){
       return ( <Login setSession={setToken}/>)
    }

  return (
      <BrowserRouter>
          <Routes>

              <Route path="/chat" element={<Chat user={token}/>}/>
              <Route path="/video" element={<Video user={token}/>}/>
              <Route path="/storage" element={<Storage user={token}/>}/>
              <Route path="/" element={<MyPage user={token}/>}/>
              <Route path="/basic" element={<Basic user={token}/>}/>


          </Routes>
      </BrowserRouter>
  );
}

export default App;
