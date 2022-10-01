import { ProSidebar, Menu, MenuItem} from 'react-pro-sidebar';
import 'react-pro-sidebar/dist/css/styles.css';
import { Link } from "react-router-dom";
import {Container, Row} from "react-bootstrap";

export default function Basic(props) {
    return (<Container >
            <Row >
                <td>
                    <ProSidebar style={{height: "100vh", left: -1, bottom: -22}}>
                        <Menu iconShape="square">
                            <img src="prof.png" style={{height:100, width: 100}} alt="YOUR PICT"/>
                            <h1>Cyberducks</h1>
                            <hr/>
                            <MenuItem onClick={()=> window.location.href = '/chat'}>Сообщения </MenuItem>
                            <MenuItem onClick={()=> window.location.href = '/video'}>Видео </MenuItem>
                            <MenuItem onClick={()=> window.location.href = '/storage'}>Галерея </MenuItem>
                            <MenuItem onClick={()=> window.location.href = '/'}>Профиль </MenuItem>
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
                <td >
                    <div style={{bottom: 0}}>
                        {props.children}
                    </div>

                </td>


            </Row>

        </Container>

    );
}