import './login.scss';
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import { APIService } from '../../services';

export interface LoginProps { }

export const LoginPage: React.FunctionComponent<LoginProps> = () => {
    const loggingIn = false;
    const [username, setUsername] = useState('');

    // need to be able to login
    let navigate = useNavigate();
    const login = () => {
        APIService.signIn(username).then(() => {
            navigate("/chat/lobby");
        });
    }

    return (
        <div id='container'>
            <div className='login'>
                <div className='welcome-card'>
                    <h1>
                        welcome to <span className='app-name'>the chat site</span>
                    </h1>
                    <h2>Please login or <Link to='/sign-up'>sign up</Link></h2>
                    <label>
                        Username
                        <input type='text' value={username} onChange={(e) => setUsername(e.target.value.toLowerCase())} />
                    </label>
                    <button type='submit' onClick={login}>
                        Submit
                    </button>
                </div>
            </div>
        </div>
    );
};
