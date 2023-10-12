import React from 'react'
import { Row, Col } from 'react-bootstrap'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser, faUserNurse } from '@fortawesome/free-solid-svg-icons'
import Slider from "react-slick";
import { CardExercise, CardMedication } from './Cards.js'


const ReferenceList = (props) => {

    if (props.results_references == null)
        return null

    const results_references = props.results_references.flat()

    return (
        <ol start="0" className="reference-list">
            {results_references.length > 0 && results_references.map((elem, index) =>
                <li key={index} className="mb-1">
                    [{elem.id}] <a href={elem.url} className="reference-link">{elem.title}</a>
                </li>
            )}
        </ol>
    )
}

const Question = (props) => {
    const question = props.question

    return (
        <Row className={'message-block my-5'}>
            <Col xs={"auto"} className='my-auto'>
                <Row>
                    <FontAwesomeIcon icon={faUser} id='search-icon' className='user-icon me-5' />
                </Row>
            </Col>
            <Col className='my-auto'>
                <Row className='question'>
                    <p className='my-auto'>
                        {question}
                    </p>
                </Row>
            </Col>
        </Row>
    )
}


export const ShortMessage = (props) => {
    const message = props.message

    return (
        <>
            <Question question={message.question} />
            <Row className="message-block-small">
                <Col className='my-auto answer py-3 ms-auto' xs={11}>
                    <Row className="mb-3">
                        <p className='answer-summary my-auto'>{message.answer['text'] ?? "There is a problem with your query. Try another one"}</p>
                    </Row>
                </Col>
                <Col xs={"auto"} className='my-auto me-3'>
                    <Row>
                        <FontAwesomeIcon icon={faUserNurse} id='search-icon' className='bot-icon me-1' />
                    </Row>
                </Col>
            </Row>

        </>
    )
}


export const ExtendedMessage = (props) => {

    const message = props.message

    const settingsExercises = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: Math.min(2, message.exercises.length),
        slidesToScroll: Math.min(2, message.exercises.length),
    };

    const settingsMedications = {
        dots: true,
        infinite: true,
        speed: 500,
        slidesToShow: Math.min(2, message.medications.length),
        slidesToScroll: Math.min(2, message.medications.length),
    };

    return (
        <>
            <Question question={message.question} />
            <Row className="message-block ms-auto">
                <Col xs={"auto"} className='my-auto me-3'>
                    <Row>
                        <FontAwesomeIcon icon={faUserNurse} id='search-icon' className='bot-icon me-1' />
                    </Row>
                </Col>
                <Col className='my-auto answer py-3' xs={11}>
                    <Row className="mb-3">
                        <p className='answer-summary my-auto'>{message.answer.text}</p>
                    </Row>
                    <Row>
                        <Col>
                            <ReferenceList results_references={message.answer.urls} />
                        </Col>
                    </Row>
                    {message.exercises.length > 0 &&
                        <>
                            <hr />
                            <Row>
                                <p className='answer-summary my-auto mb-4'>Here are some exercises that might help you:</p>
                            </Row>
                        </>
                    }
                    <Row className="px-5 pb-4">
                        <Slider {...settingsExercises}>
                            {message.exercises.map((exercise, index) => <CardExercise key={index} exercise={exercise} />)}
                        </Slider>
                    </Row>
                    {message.medications.length > 0 &&
                        <>
                            <hr />
                            <Row>
                                <p className='answer-summary my-auto mb-4'>Here are some medications that might help you:*</p>
                            </Row>
                        </>
                    }
                    <Row className="px-5 pb-4">
                        <Slider {...settingsMedications}>
                            {message.medications.map((medication, index) => <CardMedication key={index} medication={medication} />)}
                        </Slider>
                    </Row>
                    {message.medications.length > 0 &&
                        <Row>
                            <Col className="text-center">
                                <small className="disclaimer">*Disclaimer: Physio is purely for research purposes and does not constitute medical advice. The author and the institution are not liable for any actions taken based on its content.</small>
                            </Col>
                        </Row>
                    }
                </Col>
            </Row>
        </>
    )
}