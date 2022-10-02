import { Route, BrowserRouter, Routes } from "react-router-dom";
import React from "react";
import Login from "./login/Login";
import Chat from "./pages/Chat";
import Video from "./pages/Video";
import Storage from "./pages/Storage";
import MyPage from "./pages/MyPage";
import useToken from "./login/useToken";
import MainNavbar from "./components/MainNavbar";
import User from "./pages/User";


function App() {
   const {token, setToken} = useToken();
    if (!token){
       return ( <Login setSession={setToken}/>)
    }

  return (
      <>
      <MainNavbar/>
          <BrowserRouter>
              <Routes>
                  <Route path="/chat" element={<Chat user={token}/>}/>
                  <Route path="/video" element={<Video user={token}/>}/>
                  <Route path="/storage" element={<Storage user={token}/>}/>
                  <Route path="/" element={<MyPage user={token}/>}/>
                  <Route path="/page/:id" element={<User user={token}/>}/>
              </Routes>
          </BrowserRouter>
      </>

  );
}

export default App;
