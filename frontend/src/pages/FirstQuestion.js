import React from 'react'
import { useState } from 'react'
import { Container } from 'react-bootstrap'
import Image from 'react-bootstrap/Image';
import logo from '../assets/images/logo.png'
import github from '../assets/images/github.png'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMagnifyingGlass, faTrophy, faTriangleExclamation } from '@fortawesome/free-solid-svg-icons'
import { Spinner } from 'react-bootstrap'
import AlertError from './AlertError';
import { processResponse, sendQuery } from './utils.js'



const FirstQuestion = (props) => {

    const [spinning, setSpinning] = useState(false)

    const [question, setQuestion] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()

        setSpinning(true)

        props.setError('')

        sendQuery(question, []).then(res => {
            setSpinning(false)

            const [answer, exercises, medications] = processResponse(res['result'])

            props.setMessages((messages) => [...messages, { 'question': question, 'answer': answer, 'exercises': exercises, 'medications': medications }])

        }).catch(err => {
            setSpinning(false)
            props.setError(err)
        })
    }

    return (
        <Container fluid id="container-homepage">
            <Row>
                <Col xs={1} className='ms-auto text-end'>
                    <a href='https://github.com/liaad/physio'><Image id="github" fluid src={github} /></a>
                </Col>
            </Row>
            <Row className="vh-15" />
            <Row>
                <Col xs={4} xl={2} className="mx-auto">
                    <Image src={logo} fluid />
                </Col>
            </Row>
            <Row className="mt-5">
                <Col xs={7} xl={4} className="mx-auto">
                    <Form onSubmit={handleSubmit} >
                        <InputGroup id='input-group'>
                            <InputGroup.Text id='group-text'>
                                <FontAwesomeIcon icon={faMagnifyingGlass} id='search-icon' />
                            </InputGroup.Text>
                            <Form.Control id='search-input'
                                placeholder="Tell me about your problem"
                                onChange={(e) => setQuestion(e.target.value)}
                                disabled={spinning}
                            />
                            {spinning && <InputGroup.Text id='spinner'><Spinner animation="border" variant="primary" size='xl' /></InputGroup.Text>}
                        </InputGroup>
                    </Form>
                </Col>
            </Row>
            <Row className="mt-4">
                <Col className="text-center award">
                    <FontAwesomeIcon icon={faTrophy} className="me-1" />
                    Third Place in the <a href="https://swordhealth.notion.site/Sword-AI-Challenge-aad434ba8d184e27b12e6fc9b8c88c42">Sword AI Challenge</a>
                </Col>
            </Row>
            <Row id="disclaimer-container" className="mt-4 w-100">
                <Col xs={6} className="mx-auto text-center award">
                    <span className="danger-color">
                        <FontAwesomeIcon icon={faTriangleExclamation} className="me-1" />
                        Disclaimer:
                    </span> Physio is purely for research purposes and does not constitute medical advice.
                    The author and the institution are not liable for any actions taken based on its content.
                </Col>
            </Row>
        </Container>
    )
}

export default FirstQuestion