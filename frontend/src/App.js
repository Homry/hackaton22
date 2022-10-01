import { Route, BrowserRouter, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Chat from "./pages/Chat";
import Video from "./pages/Video";
import Storage from "./pages/Storage";
import MyPage from "./pages/MyPage";
import Basic from "./pages/Basic";

function App() {
  return (
      <BrowserRouter>
          <Routes>
              <Route path="/login" element={<Login/>}>
              </Route>
              <Route path="/chat" element={<Chat/>}>
              </Route>
              <Route path="/video" element={<Video/>}>
              </Route>
              <Route path="/storage" element={<Storage/>}>
              </Route>
              <Route path="/mypage" element={<MyPage/>}>
              </Route>
              <Route path="/basic" element={<Basic/>}>
              </Route>
          </Routes>
      </BrowserRouter>
  );
}

export default App;
