import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './index.css';
import { FiAlignJustify } from "react-icons/fi";
import { FiEdit } from "react-icons/fi";
import { FiSlack } from "react-icons/fi";
import { FcDecision } from "react-icons/fc";
import { FcDribbble } from "react-icons/fc";
import { FcLink } from "react-icons/fc";
import { FcBinoculars } from "react-icons/fc";
import { FcLightAtTheEndOfTunnel } from "react-icons/fc";

function App() {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [modelType, setModelType] = useState('rag'); // Default model type
    const [sidebarOpen, setSidebarOpen] = useState(false); // State to toggle sidebar
    const [suggestions, setSuggestions] = useState([
        "Pouvez-vous me donner des détails sur le Master en Informatique ?",
        "Quels sont les programmes offerts à la faculté ?",
        "Y a-t-il des conférences prévues ce mois-ci ?",
        "Comment puis-je accéder à la bibliothèque de la faculté ?",
        "Y a-t-il des clubs ou des associations étudiantes ?",

    ]);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Load the initial model on component mount
        const loadModel = async () => {
            try {
                const res = await axios.post('http://localhost:5000/load_model', { model_type: modelType });
                console.log(res.data.message); // Handle success
            } catch (error) {
                console.error('Error loading model:', error);
            }
        };
        loadModel();
    }, [modelType]); // Only run on initial mount and when modelType changes

    useEffect(() => {
        // Scroll to the bottom of the messages container
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (query.trim() === '') return; // Prevent submitting empty queries
    
        // Add user query to messages
        setMessages((prevMessages) => [...prevMessages, { sender: 'user', text: query }]);
    
        try {
            const res = await axios.post('http://localhost:5000/query', { query });
            // Extract the response part from the model's answer
            const responseText = res.data.response.split('✅Réponse :')[1].trim();
            // Add response to messages
            setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: responseText }]);
        } catch (error) {
            console.error('Error querying model:', error);
        } finally {
            setQuery(''); // Clear the input field
        }
    };

    const handleModelChange = (e) => {
        setModelType(e.target.value);
    };

    const handleNewChat = () => {
        // Clear messages and query
        setMessages([]);
        setQuery('');
    };

    const handleSuggestionClick = async (suggestion) => {
        try {
            // Add user query to messages
            setMessages((prevMessages) => [...prevMessages, { sender: 'user', text: suggestion }]);
            setSuggestions([]); // Remove all suggestions
            const res = await axios.post('http://localhost:5000/query', { query: suggestion });
            // Extract the response part from the model's answer
            const responseText = res.data.response.split('✅Réponse :')[1].trim();
            // Add response to messages
            setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: responseText }]);
        } catch (error) {
            console.error('Error querying model:', error);
        } finally {
            setSuggestions([]); // Remove all suggestions
        }
    };

    return (
        <div className="flex min-h-screen bg-gray-900 text-white">
            {/* Sidebar */}
            <div className={`${sidebarOpen ? 'w-64' : 'w-16'} transition-all duration-300 bg-gray-800 p-4 shadow-lg relative`}>
                <button onClick={handleNewChat} className="bg-indigo-600 text-white p-2 rounded-full shadow-md focus:outline-none mb-4">
                    <FiEdit />
                </button>

                {/* Rest of the sidebar content */}
                {sidebarOpen && (
                    <div>
                        <label className="block text-sm font-medium text-gray-300"></label>
                        <select
                            value={modelType}
                            onChange={handleModelChange}
                            className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-gray-700 text-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm select-options"
                        >
                            <option value="rag">
                                RAG 
                            </option>
                            <option value="fine_tuned">
                                Fine-tuned Model
                            </option>
                            {/* Add more options with descriptions as needed */}
                        </select>

                        {/* Welcome text and link at the bottom of the sidebar */}
                        <div className="block absolute bottom-4 left-1 right-1 text-center">
                            <FiSlack className="inline-block mr-2" />
                            <p>Welcome to Your Virtual Assistant</p>
                            <p>Faculté des Sciences et Techniques de Tanger</p>
                            <a href="https://fstt.ac.ma/Portail2023/" target="_blank" rel="noopener noreferrer" className="text-indigo-400">Visit the main site</a>
                        </div>
                    </div>
                )}
            </div>
            <button 
                onClick={() => setSidebarOpen(!sidebarOpen)} 
                // Call handleNewChat function to start a new chat
                className="bg-indigo-990 text-white p-2 rounded-full shadow-md focus:outline-none mb-4"
            >
                <FiAlignJustify />
            </button>
            {/* Main Content */}
            <div className="flex-1 flex flex-col items-center justify-between p-20 shadow-lg">
                <div className="w-full max-w-4xl flex flex-col space-y-4 p-10 overflow-y-auto bg-gray-900 no-scrollbar" style={{ height: '80vh' }}>
                    {/* Suggestions */}
                    <div className="w-full max-w-lg flex center space-x-4 mb-4">
                        {suggestions.map((suggestion, index) => (
                            <div 
                                key={index} 
                                onClick={() => handleSuggestionClick(suggestion)} 
                                className="p-4 top-10 left-5 rounded-lg shadow-md bg-gray-700 text-white cursor-pointer w-full text-center relative" // Added 'relative' class for positioning
                                style={{ Width: '100vh !important' }} // Increased maxWidth to 75%
                            >
                                <div className="relative">
                                    {index === 0 && <FcBinoculars className="top-0 left-0 right-0 mx-auto" />}
                                    {index === 1 && <FcDribbble className="top-0 left-0 right-0 mx-auto" />}
                                    {index === 2 && <FcLink className="top-0 left-0 right-0 mx-auto" />}
                                    {index === 3 && <FcDecision className="top-0 left-0 right-0 mx-auto" />}
                                    {index === 4 && <FcLightAtTheEndOfTunnel className="top-0 left-0 right-0 mx-auto" />}
                                    <span>{suggestion}</span>
                                </div>
                            </div>
                        ))} 
                    </div>
                    {/* Chat messages */}
                    {messages.map((msg, index) => (
                        <div 
                            key={index} 
                            className={`p-4 rounded-lg shadow-md max-w-lg ${
                                msg.sender === 'user' ? 'ml-auto bg-indigo-900 text-white' : 'mr-auto bg-gray-800 text-gray-300'
                            }`}
                        >
                            {msg.text}
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={handleSubmit} className="absolute bottom-0 left-0 w-full p-4  flex justify-center shadow-lg">
                    <div className="flex items-center w-full max-w-xl space-x-2" style={{ marginBottom: '40px' }}>
                        <textarea 
                            value={query} 
                            onChange={(e) => setQuery(e.target.value)} 
                            placeholder="Enter your query" 
                            className="block w-full py-2 px-3 border border-gray-300 bg-gray-700 text-gray-300 rounded-l-full shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm resize-none"
                            rows={1}
                            style={{ minHeight: '40px', maxHeight: '150px', overflowY: 'auto' }}
                        />
                        <button 
                            type="submit" 
                            className="py-2 px-3 bg-indigo-600 text-white font-semibold rounded-r-full shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm.707-10.293a1 1 0 00-1.414 0L6.5 10.5a1 1 101.414 1.414L9 10.828V14a1 1 0 102 0v-3.172l1.086 1.086A1 1 0 1013.5 10.5l-2.793-2.793a1 1 0 00-1.414 0z" clipRule="evenodd" />
                            </svg>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default App;

