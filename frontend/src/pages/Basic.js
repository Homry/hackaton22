import { ProSidebar, Menu, MenuItem } from 'react-pro-sidebar';
import 'react-pro-sidebar/dist/css/styles.css';
import { Link } from "react-router-dom";
import {Container, Row} from "react-bootstrap";

export default function Basic(props) {
    return (<Container style={{marginTop: -21}}>
            <Row >
                <td>
                    <ProSidebar style={{height: "100vh", left: -1, bottom: -1}}>
                        <Menu iconShape="square">
                            <MenuItem>Сообщения <Link to="/chat" /></MenuItem>
                            <MenuItem>Видео <Link to="/video" /></MenuItem>
                            <MenuItem>Галерея <Link to="/storage" /></MenuItem>
                            <MenuItem>Профиль <Link to="/mypage" /></MenuItem>
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
