import React from 'react';
import ReactDOM from 'react-dom';
import './main.css';
import { useNavigate } from 'react-router-dom';


function Register() {
    const [username, setUsername] = React.useState('');
    const [usernameValid, setUsernameValid] = React.useState(true);
    const [usernameMessage, setUsernameMessage] = React.useState('');

    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [recaptchaToken, setRecaptchaToken] = React.useState('');
    const navigate = useNavigate(); 

    const checkUsername = async () => {
        try {
            const response = await fetch(`http://localhost:8000/register?username=${username}`);
            const data = await response.json();
    
            if (data.isTaken) {
                setUsernameValid(false);
                setUsernameMessage('This username is already taken.');
            } else {
                setUsernameValid(true);
                setUsernameMessage('');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // execute reCAPTCHA  when the use presses login
    // get reCAPTCHA token and include it in the registration request
    const handleRegister = async () => {
        await handleRecaptcha();
    
        fetch('http://localhost:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password, recaptchaToken })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Check the data returned by the server
            if (data.message === 'Registration successful') {
                console.log('Registration successful');
                navigate('/');
            } else if (data.message === 'Username taken') {
                // Handle the case where the username is taken
                setUsernameValid(false);
                setUsernameMessage('Username taken');
            } else {
                console.log('Registration failed', data.error);
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    };
    
    const handleRecaptcha = function() {
        return new Promise((resolve) => {
            grecaptcha.enterprise.ready(function() {
                grecaptcha.enterprise.execute('6LdoATQpAAAAALApLmMpH_v09ituPJEfE2tF2ZPl', {action: 'submit'}).then(function(token) {
                    setRecaptchaToken(token);
                    resolve(); // Resolve the Promise when the reCAPTCHA token is set
                });
            });
        });
    };
    
    return (
        <div className="min-h-screen flex">
            <div className="w-1/2 bg-black text-white flex flex-col justify-center items-start p-20">
                <h1 className="text-6xl font-bold mb-4">Practice Makes Perfect</h1>
                <p className="text-lg">LangAide</p>
            </div>
            <div className="w-1/2 flex justify-center items-center">
                <div className="w-96">
                <h2 className="text-4xl font-bold mb-6">Sign Up <br/> to LangAide</h2>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                    Username
                    </label>
                    <input 
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                    id="username" 
                    type="text" 
                    placeholder="Enter your username"
                    value={username}
                    onChange={e => {
                        setUsername(e.target.value);
                        setUsernameValid(true); // Reset validation state on user input
                    }}
                    onBlur={checkUsername} // Add an onBlur event to check the username when the input loses focus
                    />
                    {!usernameValid && <p className="text-red-500 text-xs italic">{usernameMessage}</p>}
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                    Email
                    </label>
                    <input 
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" 
                    id="email" 
                    type="email" 
                    placeholder="Enter your email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                    Password
                    </label>
                    <input 
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" 
                    id="password" 
                    type="password" 
                    placeholder="Enter your password"
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    />
                </div>
                <div className="flex items-center justify-between">
                    <button 
                    className="bg-black text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full" 
                    type="button"
                    onClick={handleRegister}
                    >
                    Sign Up
                    </button>
                </div>
                <div className="mt-6 text-center">
                    <span className="inline-block align-baseline font-bold text-sm text-black mr-2">
                        Have an account? 
                    </span>
                    <a className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" href="/">
                        Sign in
                    </a>
                </div>
                </div>
            </div>
            </div>
        );
    };


// ReactDOM.render(<Register />, document.getElementById('app'));

export default Register;