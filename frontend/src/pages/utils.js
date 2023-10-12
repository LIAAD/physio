
export const sendQuery = (last_question, history) => {
    const url = new URL("/pipeline", process.env.REACT_APP_FETCH_URL)

    return fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'chat': {
                'last_question': last_question,
                'history': history
            }
        })
    }).then(res => res.json())
}

export const processResponse = (res) => {
    const answer = res['answer'] ?? {}
    const exercises = res['exercises'] ?? []
    const medications = res['medications'] ?? []

    return [answer, exercises, medications]
}