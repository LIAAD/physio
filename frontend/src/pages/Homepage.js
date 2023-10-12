import React from 'react'
import { useState } from 'react'
import FirstQuestion from './FirstQuestion';
import FollowingQuestions from './FollowingQuestions';
import AlertError from './AlertError';


const Homepage = (props) => {

    const [messages, setMessages] = useState([])

    const [error, setError] = useState('')

    if (messages.length == 0)
        return (
            <>
                {error && <AlertError message='Error Sending Question' />}
                <FirstQuestion setMessages={setMessages} error={error} setError={setError} />
            </>
        )
    else
        return (
            <>
                {error && <AlertError message='Error Sending Question' />}
                <FollowingQuestions messages={messages} setMessages={setMessages} error={error} setError={setError} />
            </>
        )
}

export default Homepage