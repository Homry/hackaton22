import { ProSidebar, Menu, MenuItem} from 'react-pro-sidebar';
import 'react-pro-sidebar/dist/css/styles.css';
import { Link } from "react-router-dom";
import {Container, Row} from "react-bootstrap";

export default function Basic(props) {
    return (<Container style={{marginTop: -24}}>
            <Row >
                <td>
                    <ProSidebar style={{height: "100vh", left: -1, bottom: -22}}>

                        <Menu iconShape="square">
                            <img src="prof.png" style={{height:100, width: 100}} alt="YOUR PICT"/>
                            <h1>Cyberducks</h1>
                            <hr/>
                            <MenuItem>Сообщения <Link to="/chat" /></MenuItem>
                            <MenuItem>Видео <Link to="/video" /></MenuItem>
                            <MenuItem>Галерея <Link to="/storage" /></MenuItem>
                            <MenuItem>Профиль <Link to="/mypage" /></MenuItem>
                            <footer
                                style={{
                                    position: "fixed",
                                    bottom: 0,
                                }}
                            >
                                © Cyberducks Team :3
                            </footer>
                        </Menu>
                    </ProSidebar>
                </td>
                <td>
                    {props.children}
                </td>


            </Row>

    </Container>

);
}
