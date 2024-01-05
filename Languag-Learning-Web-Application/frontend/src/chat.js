import React, { useState, useEffect, useRef } from 'react';
// main.css is just the tailwind required css imports
import './main.css';
// for css styling the chat bubbles and message frame
import './chat.css';

// Wonder how chat apps powered by ai works? here is a simple rundown.

// Chat is the frontend functional component that renders the chat page
function Chat() {

// ** useState is a react hook that allows state usage in functional components
//** [] means storing in an array, '' means soring in a string 

// chat is the state that holds the chat history
const [chat, setChat] = useState([]);
// message is the state that holds the message that the user is typing
const [message, setMessage] = useState('');
// messagesEndRef is a reference to the last message in the chat
// so a function (scrollToBottom) can be called to scroll to the bottom of the chat
// it is null when first initialized, because when users first enter the chat they 
// cannot have sent any messages yet. The property is mutable though!
const messagesEndRef = useRef(null);

const scrollToBottom = () => {
    // scrollIntoView is a function that scrolls to the element
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
}

// Scroll to the bottom of the chat when the component first renders
// useEffect is a react hook that runs a function when the component renders
// in this case, it runs the scrollToBottom function when the component chat renders
useEffect(() => {
    scrollToBottom();
}, [chat]); // this part refers to the component. its chat here 
// if this isn't here, once all the past messages render you will have to manually scroll down. :(

// Fetch chat history when the component mounts
useEffect(() => {
    fetchChatHistory();
}, []); // Empty dependency array means this effect runs only *once* on mount
// because this runs non mount and before the interval,
// the time it takes for the past messages to load upon page load is the same

const fetchChatHistory = async () => {
    try {
        // uses fetch api to make a get request to the django backend
        // why this link? because of how the urls are defined
        // in the backend, the view that handles getting the chat history from db in lang_chat/views.py is
        // defined as path('chat/', views.chat, name='chat') in lang_app/urls.py.
        // i used 8000 as the port for django backend
        // i used 8080 as the port for react frontend
        // they need to be ran simultaneously for the webpage to work!!
        
        // frontend and backend communication 
        // fetch request -> http://localhost:8000/chat/ -> lang_app/urls.py -> lang_chat/views.py -> lang_chat/serializers.py -> lang_chat/models.py -> lang_chat/views.py -> lang_app/urls.py -> frontend/src/chat.js


        // the fetch request returns a Promise, which resolves to the response object HERE.
        // the promise is essentially, a promise that the backend will give 
        // the frontend a reply, but it needs time to do so.

        // the await keyword pauses the async function of fetchChatHistory until the promise is resolved, i.e. gets the response,
        // because we need this important info, i mean that is why i wrote the function in the first place

        // once the promise is resolved, the response object is stored in the response variable
        const response = await fetch('http://localhost:8000/chat/')

            // if the response there is error while fetching the response,
            // the catch block will catch the error and throw a new error
            // a Network error message is also thrown at the same time
            // error handling is a good practice to understand where and what went wrong
            // and because the error messages are desigend to be distinct from each other,
            // it will make the application easier to debug. better to hone in on what area is calling the error
            // a general 404 error would be like finding a needle in a haystack (been there, done that, it sucks)
            .catch((error) => {
                throw new Error(`Network error: ${error.message}`);
            }); // this error happens when the server was never reached. something went south. 
        
        // the ok property of the response object is a boolean that indicates whether the response was successful
        // if it is successful, the promise is resolved, and the response object is passed to the next line
        // if it is NOT (!) successful (i.e. not response.ok), a new error is thrown with a new message. 
        // a status code is assigned to unscuccessful responses, so the error message will be like "Server error: 404"
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        } // this error happens when the server is reached, but the server had problem processing the request.

        // under successful response, 
        // the reponse is passed here, passed to the json() method 
        // which will parse the response into json format, and stores it in data. 
        // same thing, the action requires several business days (jk), so it requires await
        const data = await response.json();
        // parsing to json is makes accessing the data easier
        // it is kind of like a dictionary, but it is a json object
        // dictionaries are great because you can access the data with the key

        // Update component's state with the received data
        // same thing here, messages is a key in the data json object, which is the parsed json object
        // remember the react hooks defined at the start?
        // setChat is the function that updates the chat state, 
        // so here the messages is passed to the setChat function, which updates the chat state
        setChat(data.messages);

    // if the try block fails, the catch block will catch the error and throw a new error
    // this happened to me MANY TIMES when i was configuring the backend and figuring out how it actually works,
    // so i had to go back and forth between the frontend and backend to see what went wrong.
    // it could be anything ranging from a missing slash in the fetch api url, to a typo in the backend, to just downright bad view design
    // genereally its backend errors. 
    } catch (error) {
        console.error('Error fetching chat history:', error);
    }
};

useEffect(() => {
    // the setInterval function is a function which is used for calling a function every x milliseconds

    // the setInterval function creates a ticking timebomb, NOT a timer 
    // because each timebomb is assigned an Id, stored in the variable intervalId
    // the ids are UNIQUE and specific to each timebomb,
    // so the variable is cleared upon the initiation of the nested function.
    const intervalId = setInterval(async () => {

        // Fetch chat history...
        fetchChatHistory();

    }, 1000); // the function is called every 5 seconds (5000ms)
    // the time it takes for new messages to load though,
    // to be real is not really dependent here but is rather dependent on the backend
    // on how fast the backend can respond to the request
    // the fetchChatHistory will fetch the past messages, but if there's no new messages nothing happens
    // its just here to make sure that the chat is updated

    // the interval is cleared when the component is unmounted, to prevent memory leaks
    // unmounted as in the user leaves the page (for examples, going to the login page)

    // it takes 6 seconds for a response to load, regardless of the interval
    // an improvement would be using websockets

    // Clear the interval when the component is unmounted
    return () => clearInterval(intervalId);
    // Optional: Implement WebSocket, i didn't do that

}, []); // this effect also runs once on mount, same as fetchChatHistory
        // running it initiates the setInterval function

const sendMessage = async () => {
    // message is the state variable that holds the message
    // trim() removes whitespace from both ends of a string
    // === is strict equality, it checks if the message is an empty string ''
    // if it is an empty string, it returns and does not send the message
    if (message.trim() === '') return; // prevents sending blank messages

    // set the Message statevariable to an empty string upon initiating sendMessage in the frontend
    // clears the input field regardless of whether it is a blank message or not
    setMessage(''); // Clear the message input immediately
    // without this, the message will be sent but the input field will not be cleared
    // in the message box you'll have to manually delete the message lol (cmd + a, delete)

    // same thing as fetchChatHistory, a request has to be made to the backend
    // but this time it is a POST request, not a GET request
    // i didn't specify the method in fetchChatHistory because it is a GET request by default
    // but here i am specifying the method to be POST

    // get requests are used to get data from the backend
    // post requests are used to send data to the backend

    // the fetch function takes in the url and the options object {}
    // the url is local host 8000, the django backend / chat, 
    // because that is where the view that handles the post request is defined

    // the options object (inside {}) is the object that contains the data that is sent to the backend
    // it specifies the method, headers, and body of the request
    // method can be GET, POST, PUT, DELETE, etc.
    // headers is the header of the request, i.e. the content type
    // body is the data that is sent to the backend, in this case the message
    // the message is the state variable updated when the setMessage function is called in the frontend
    // eventhough I did initialise message as a string, it is still a state variable, so it is an object
    // message object has to be stringified into a JSON string to be sent to the backend
    // same thing as fetchChatHistory, the response is stored in the response variable

    const response = await fetch('http://localhost:8000/chat/', { // Update the URL to match your Django URL configuration
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });

    // the response is parsed into json format and stored in data
    const data = await response.json(); // Read the response body here

    // if the reponse is okay (response.ok = True)
    if (response.ok) {
        // Add the new message to the existing chat state, initialised as an empty array
        // chat => is a function that updates the chat state
        // updated with [...chat, ...data.messages], which is a new array
        // the new array is the old array (chat) and the new message (data.messages)
        // ...chat is a spread operator, which is for including all elements from chat, likewise for ...data.messages, in the new array
        setChat(chat => [...chat, ...data.messages]); // Use the data from response.json()

        // Scroll to the bottom of the chat
        scrollToBottom();

    // if the response is not okay (response.ok = False)
    } else {
        // the response will be parsed an stored in errorData
        const errorData = await response.json();
        // the error message, with the error part of the errorData object will be logged in the console
        console.error('Failed to send message:', errorData.error);
    }
};

return (
    <div className="flex h-screen bg-gray-100">
        {/* the aside tag is the left side of the chat. Side bar. */}
        <aside className="w-64 bg-white shadow-md">
            <div className="p-4 border-b">
                <button className="flex items-center space-x-2 text-gray-700">
                    <i className="fas fa-plus"></i>
                    {/* Placeholder for adding new chats */}
                    <span>New chat</span>
                </button>
            </div>
            <nav className="p-4">
                <ul>
                    <li className="flex items-center space-x-2 p-2 hover:bg-gray-200 cursor-pointer">
                        <i className="fas fa-coffee"></i>
                        {/* Placeholder for created chats belonging to a user */}
                        <span>Starbucks with Barista</span>
                    </li>
                    <li className="flex items-center space-x-2 p-2 hover:bg-gray-200 cursor-pointer">
                        <i className="fas fa-city"></i>
                        <span>New York City with Pedestrian</span>
                    </li>
                    <li className="flex items-center space-x-2 p-2 hover:bg-gray-200 cursor-pointer">
                        <i className="fas fa-film"></i>
                        <span>Movie Theatre with Receptionist</span>
                    </li>
                    <li className="p-2 text-blue-600 cursor-pointer">View All Chats</li>
                </ul>
            </nav>
            <div className="p-4 border-t">
                <button className="flex items-center space-x-2 text-gray-700">
                    <i className="fas fa-book"></i>
                    {/* Placeholder for dictionary page*/}
                    <span>Dictionary</span>
                </button>
            </div>
            <div className="p-4 border-t">
                <ul>
                    {/* Placeholder for page functionality functions */}
                    <li className="flex items-center space-x-2 p-2 text-gray-700 cursor-pointer">
                        <i className="fas fa-trash-alt"></i>
                        <span>Clear conversations</span>
                    </li>
                    <li className="flex items-center space-x-2 p-2 text-gray-700 cursor-pointer">
                        <i className="fas fa-moon"></i>
                        <span>Dark mode</span>
                    </li>
                    <li className="flex items-center space-x-2 p-2 text-gray-700 cursor-pointer">
                        <i className="fas fa-user"></i>
                        <span>My account</span>
                    </li>
                    <li className="flex items-center space-x-2 p-2 text-gray-700 cursor-pointer">
                        <i className="fas fa-sign-out-alt"></i>
                        <span>Log out</span>
                    </li>
                </ul>
            </div>
        {/* the aside tag for the right side of the page, the chat. */}
        </aside>
        <main className="flex flex-col flex-1">
            <div className="flex items-center justify-between p-4 border-b border-gray-200">
                {/* Placeholder for the chat name. 
                    preferrably I'd like it to display chat_name, after I write the views
                    to map messages into chats belonging to a specific user. */}
                <h2 className="text-xl font-semibold">Chat Name</h2>
                <div className="flex items-center">
                    <button className="p-2 rounded-full hover:bg-gray-200">
                        <i className="fas fa-question-circle"></i>
                    </button>
                    <button className="ml-2 p-2 rounded-full hover:bg-gray-200">
                        <i className="fas fa-cog"></i>
                    </button>
                </div>
            </div>
            <div className="flex-grow overflow-auto">
                <div className="chat-messages">
                    {/* function for iterating over the array of the chat state. 
                    The intial array is set in the fetchChatHistory function, by setChat(data.messages); (line 102), 
                    and updated when the sendMessage function is called, with setChat(chat => [...chat, ...data.messages]); (line 199)
                    
                    the map method takes callback functions as arguments.
                    callback functions are functions that are passed as arguments to another function,
                    and executed inside the outer function only when the outer function finishes execution.
                    
                    the callback function is the entire (msg,index) => (div tag, which is the chat bubble),
                    and takes in the element (msg) and the index of the element (index) as arguments.
                    this function itself is an argument to the map method, 
                    and is called for each element in the chat array.
                    
                    the callback function uses msg and index from the chat array to create a jsx element for each message. 
                    the jsx element is the div tag, which is the chat bubble.
                    
                    chat.map() is called on the chat array. Each element calls the the callback function,  and the messages in the element is called by the name msg. 
                    the naming doesn't really matter. I can name is it hello or whatever, but msg as in message just makes sense in this context. 
                    index is the actual second parameter of the map function, so it just makes sense */}
                    {chat.map((msg, index) => (
                            // god usernaming is so funny. i changed the backend and forgot to change this, 
                            // had sender instead of sender_username and had non styled messages 
                            // the naming has to match what the backend is sending
                            
                            // the key property is a unique identifier for each element in the array
                            // index is used here because the messages may not be unique, and is just an accessible property
                            // the className is set to either ai-message or user-message, depending on the sender
                            // the sender can be informed by the sender__username property of the msg object
                            // check the backend: lang_chat/views.py. the JsonReponse is 'messages'. That is what fetched here, 
                            // as the msg object 
                            <div key={index} className={`message ${msg.sender__username === 'ai' ? 'ai-message' : 'user-message'}`}>
                                <div className="message-info text-sm text-gray-500">
                                    {/* displays the sender username availale in msg */}   
                                    <span>{msg.sender__username}</span>

                                    {/* just a dot to keep the username and date apart. */}
                                    <span> · </span>

                                    {/* displays the timestamp available in msg as a time object.
                                    set the timestap in msg as a dateTime object. {} is used to embed javascript in jsx.
                                    It is not shown on the actual webpage, but used for SEO purposes

                                    THEN create a new Date object using msg.timestamp, converting it to a string with local time 
                                    locale is determined by OS settings. the string is what is actually displayed on the webpage.
                                    It is possible to not include dateTime={msg.timestamp} and still have it work, but its just good practice. 
                                    
                                    the time saved in the database is in UTC like "2024-01-03 22:41:03.462729+00" */}

                                    <time dateTime={msg.timestamp}>{new Date(msg.timestamp).toLocaleTimeString()}</time>
                                </div>
                                {/* displays the message text available in msg */}
                                <p className="message-text mt-1">{msg.message_text}</p>
                            </div>
                        ))}
                    {/* this is the div tag that is referenced in the scrollToBottom function (line 25)
                    automaticall scrolls to the most recent message */}
                    <div ref={messagesEndRef} />
                    </div>
                </div>

            <div className="chat-input border-t p-4">
                <button 
                    {/* a button which calls the sendMessage function once clicked */}
                    className="send-button"
                    onClick={sendMessage}
                    title="Send"
                >
                    <i className="fas fa-paper-plane"></i>
                </button>
                <input
                    type="text"
                    {/* sets the value in the input field to the message state variable,
                    so it always reflect what is currently in the field */}
                    value={message}
                    
                    {/* event handler that gets called whenever the user types into the field
                    (i.e. the field is *changed*)
                    e.target triggers and event, and e.target.value is whatever the user has typed 
                    sets the message state variable as e.target.value 
                
                    essentially, whenever the user types something into the input field, 
                    update the message state variable to be whatever the user has typed */}
                    onChange={e => setMessage(e.target.value)}

                    {/* event handler that gets called whenever the user presses the enter key 
                    if the key is pressed, the sendMessage() function is called 
                    the message can be sent by either clicking the send button or enter key,
                    because of onChange. sendMessage sends the value in message state variable */}
                    onKeyDown={e => {
                        if (e.key === 'Enter') {
                            sendMessage();
                            // prevents the default action of an enter key action from happening, 
                            // which in a text box, is the addition of a new line
                            // essntially rerouting the function of the 'enter' key to serve as a send button
                            e.preventDefault();
                        }
                    }}
                    placeholder="Type a message..."
                />
            </div>
        </main>
    </div>   
);
}

export default Chat;