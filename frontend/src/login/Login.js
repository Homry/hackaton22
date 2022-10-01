import React, {useState, useEffect} from "react";
import '../pages/style.css'


async function loginUser(credentials, name){
    console.log(`loginUser ${name}, ${credentials}`)
    return fetch(`http://127.0.0.1:5000/user/${name}`, {
        method: "POST",
        body: JSON.stringify(credentials),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(function(response) {
        console.log(`response login - ${response}`);
        return response.json();
    })
}

export default function Login(props) {
    const [isLogin, setLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [singupHidden, setSingupHidden] = useState(true);
    const [singupHiddenVal, setSingupHiddenVal] = useState('')

    const handleSubmit = async e => {
        e.preventDefault();
        let credentials;
        let req;
        if (isLogin){
            req = 'login';
             credentials = {
                'email': email,
                'password': password
            }
        } else{
            req = 'singup';
            credentials = {
                'email': email,
                'password': password,
                'name': name
            }
        }
        const session = await loginUser(credentials, req);
        if (session['error'] !== undefined){
            setSingupHidden(false);
            setSingupHiddenVal(session['error']);
        }
        console.log(session)
        props.setSession(session);
    }

    if (isLogin === false){
        return (
            <div className="card-wrapper">
                <div className="card">
                    <h1 className="center">Create an Account</h1>
                    <form name="signup_form" onSubmit={handleSubmit}>
                        <label htmlFor="name">Name</label>
                        <input type="text" name="name" className="field" required onChange={event => setName(event.target.value)}/>
                        <label htmlFor="email">Email</label>
                        <input type="email" name="email" className="field" required onChange={event => setEmail(event.target.value)}/>
                        <label htmlFor="password">Password</label>
                        <input type="password" name="password" className="field" required onChange={event => setPassword(event.target.value)}/>
                        <p className="error" hidden={singupHidden} >{singupHiddenVal}</p>
                        <input type="submit" value="singup"  className="btn"/>
                        <h2 className="center">or</h2>
                        <button className={'btn'} onClick={() => {
                            setPassword('');
                            setLogin('');
                            setEmail('');
                            setLogin(true);
                            console.log(isLogin)
                        }}> login</button>
                    </form>
                </div>
            </div>
        )
    } else {


        return (
            <div className="card-wrapper">
                <div className="card">
                    <h1 className="center">Log In</h1>
                    <form name="login_form" onSubmit={handleSubmit}>
                        <label htmlFor="email">Email</label>
                        <input type="email" name="email" className="field" required  onChange={event => setEmail(event.target.value)}/>
                        <label htmlFor="password">Password</label>
                        <input type="password" name="password" className="field"  required onChange={event => setPassword(event.target.value)}/>
                        <input type="submit" value="login" className="btn"/>
                        <p className="error" hidden={singupHidden} >{singupHiddenVal}</p>
                        <h2 className="center">or</h2>
                        <button className={'btn'}  onClick={() => {
                            setPassword('');
                            setLogin('');
                            setEmail('');
                            setLogin(false);
                            console.log(isLogin)
                        }} > singup</button>

                    </form>

                </div>
            </div>
        );
    }
}
