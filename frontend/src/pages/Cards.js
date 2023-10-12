import React from 'react'
import { Card, Button } from 'react-bootstrap'
import YouTube from 'react-youtube'; // Import the YouTube component


export const CardMedication = (props) => {
    const medication = props.medication

    const summary = medication['Summary'] || medication['Description'] || 'No summary available'

    const extractIdFromUrl = (url) => {
        return url.split('/')[4]
    }

    return (
        <Card className='card-medication mx-auto mb-3'>
            <Button variant='' href={medication.url}>
                <Card.Img variant="top" className='pt-3 px-2' src={`https://go.drugbank.com/structures/${extractIdFromUrl(medication.url)}/image.svg`} />
                <Card.Body className='pb-3'>
                    <Card.Title>{medication['Generic Name']}*</Card.Title>
                    <Card.Text className='text-justify'>{summary.slice(0, 250)}</Card.Text>
                </Card.Body>
            </Button>
        </Card>

    )
}


export const CardExercise = (props) => {
    const exercise = props.exercise

    const extractYouTubeVideoId = (url) => {
        // Regular expression to match the YouTube video ID
        const regex = /(?:\/embed\/|v=)([\w-]{11})(?:\?|$|&)/;
        const match = url.match(regex);

        if (match && match.length === 2) {
            return match[1]; // Return the extracted YouTube video ID
        } else {
            // Handle invalid URL or no match
            return null
        }

    }

    const videoId = extractYouTubeVideoId(exercise.video_url)

    if (videoId == null)
        return null

    return (
        <Card className='card-exercise mx-auto mb-3'>
            <Button variant='' href={exercise.href} className='pt-4'>
                <YouTube videoId={videoId} opts={{ height: '300px', width: '100%' }} onReady={(event) => event.target.pauseVideo()} />
                <Card.Body>
                    <Card.Title>{exercise.title}</Card.Title>
                    <Card.Text>{exercise.desc.slice(0, 200)}</Card.Text>
                </Card.Body>
            </Button>
        </Card>
    )
}