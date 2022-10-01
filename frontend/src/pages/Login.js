import React, {useState, useEffect} from "react";
import './style.css'

export default function Login() {

    function login() {
        if (email !== '' && password !== '') {
            let value_for_req = {
                'email': email,
                'password': password
            }
            fetch('http://127.0.0.1:5000/user/singup', {
                method: "POST",
                body: JSON.stringify(value_for_req),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            }).then(function(response) {
                return response.json();
            }).then(function(res){
                setEmail('');
                setPassword('')
            })

        }
    }
    function singup(){
        if (email !== '' && password !== '' && name !== ''){
            let value_for_req = {
                'email': email,
                'password': password,
                'name': name
            }
            fetch('http://127.0.0.1:5000/user/singup', {
                method: "POST",
                body: JSON.stringify(value_for_req),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            }).then(function(response) {
                return response.json();
            }).then(function (res){
                if (res['error'] !== undefined){
                    setSingupHiddenVal(res['error']);
                    setSingupHidden(false)
                } else {
                    setSingupHiddenVal('');
                    setSingupHidden(true);
                }
                console.log(res);
                setEmail('');
                setPassword('')
                setName('')
            })

        }
    }

    const [isLogin, setLogin] = useState(false);
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [singupHidden, setSingupHidden] = useState(true);
    const [singupHiddenVal, setSingupHiddenVal] = useState('')


    if (isLogin === false){
        return (
            <div className="card-wrapper">
                <div className="card">
                    <h1 className="center">Create an Account</h1>
                    <form name="signup_form">
                        <label htmlFor="name">Name</label>
                        <input type="text" name="name" className="field" required onChange={event => setName(event.target.value)}/>
                        <label htmlFor="email">Email</label>
                        <input type="email" name="email" className="field" required onChange={event => setEmail(event.target.value)}/>
                        <label htmlFor="password">Password</label>
                        <input type="password" name="password" className="field" required onChange={event => setPassword(event.target.value)}/>
                        <p className="error" hidden={singupHidden} >{singupHiddenVal}</p>
                        <input type="button" value="singup"  onClick={singup} className="btn"/>
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
                    <form name="login_form">
                        <label htmlFor="email">Email</label>
                        <input type="email" name="email" className="field" required  onChange={event => setEmail(event.target.value)}/>
                        <label htmlFor="password">Password</label>
                        <input type="password" name="password" className="field"  required onChange={event => setPassword(event.target.value)}/>
                        <input type="button" value="login" onClick={login} className="btn"/>
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
