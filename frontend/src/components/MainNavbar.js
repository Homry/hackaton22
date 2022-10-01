import Styled from "styled-components";

function MainNavbar() {
    return (
        <Wrapper>
            <div className="topnav">
                <a className="active" href="/">Профиль</a>
                <a href="/video">Сгенерировать эмоцию</a>
                <a href="/storage">Галерея</a>
                <a href="/chat">Чат</a>
            </div>
        </Wrapper>
    );
}

export default MainNavbar;

const Wrapper = Styled.section`

/* Add a black background color to the top navigation */
.topnav {
    background-color: #333;
    overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
    float: left;
    color: #f2f2f2;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
    font-size: 17px;
}

/* Change the color of links on hover */
.topnav a:hover {
    background-color: #ddd;
    color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
    background-color: #04AA6D;
    color: white;
}`;