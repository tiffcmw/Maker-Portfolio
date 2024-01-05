import React from 'react';
import { useState } from 'react';
import ReactDOM from 'react-dom';
import { Link } from 'react-router-dom';
import './main.css';


function Login() {
    // Initialize email state with empty string
    const [email, setEmail] = React.useState(''); 
    // Initialize password state with empty string
    const [password, setPassword] = React.useState(''); 
    // Initialize errorMessage state with null
    const [errorMessage, setErrorMessage] = useState(null); 

    const login = async () => { // Define login function
        // Get email value from input field
        const email = document.getElementById('email').value; 
         // Get password value from input field
        const password = document.getElementById('password').value;

        // Send POST request to login endpoint
        const response = await fetch('http://localhost:8000/login/', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password }) // Send email and password as JSON payload
        });

        // If response is successful
        if (response.ok) { 
            // Parse response data
            const data = await response.json();
            // Store token in local storage
            localStorage.setItem('token', data.token); 
            // Redirect to the chat page defined in the react router
            window.location.href = '/chat';  
        
        // If response is not successful
        } else {
            // If response contains JSON data
            if (response.headers.get('Content-Type').includes('application/json')) { 
                // Parse error data
                const errorData = await response.json(); 
                // Set error message state with error message from response
                setErrorMessage(errorData.message); 
            // If response does not contain JSON data
            } else {
                // Set error message state with generic error message
                setErrorMessage('An error occurred'); 
            }
        }
    };

    return (
        <div className="min-h-screen flex">
            <div className="w-1/2 bg-black text-white flex flex-col justify-center items-start p-20">
                <h1 className="text-6xl font-bold mb-4">Practice Makes Perfect</h1>
                <p className="text-lg">LangAide</p>
            </div>
            <div className="w-1/2 flex justify-center items-center">
                <div className="w-96">
                    <h2 className="text-4xl font-bold mb-6">Welcome! <br/> to LangAide</h2>
                    <div className="mb-4">
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
                        <div className="mb-4">
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
                        <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center">
                            <input type="checkbox" id="rememberMe" />
                            <label className="text-sm font-bold text-sm text-gray-700 ml-2" htmlFor="rememberMe">
                            Remember me
                            </label>
                        </div>
                        <a className="text-sm font-bold text-sm text-blue-500 hover:text-blue-800" href="#">
                            Forgot password?
                        </a>
                        </div>
                        {errorMessage && <p className="text-red-500 italic">{errorMessage}</p>}
                        <button 
                            className="bg-black text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full" 
                            type="button"
                            onClick={login}
                        >
                            Sign in
                        </button>
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                        <span className="border-b w-1/5 lg:w-1/4"></span>
                        <a href="#" className="text-xs text-center text-gray-500 uppercase">or</a>
                        <span className="border-b w-1/5 lg:w-1/4"></span>
                    </div>
                    <div className="flex items-center justify-between mt-4">
                        <button className="bg-white text-gray-700 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full border border-gray-300 shadow-sm">
                            <i className="fab fa-google mr-2"></i> Sign in with Google
                        </button>
                    </div>
                    <div className="mt-6 text-center">
                    <span className="inline-block align-baseline font-bold text-sm text-black mr-2">
                        Don't have an account? 
                    </span>
                    <a className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" href="/register">
                        Sign up
                    </a>
                    </div>
                </div>
            </div>
        </div>
        
    );
}

// If using webpack to bundle JavaScript and 
// including the bundled JavaScript file in your HTML file with a script tag, 
// then don't need to export the Login component.

// render the Login component to the DOM
// i'm routing into one js
// ReactDOM.render(<Login />, document.getElementById('app'));

export default Login; // in login.js