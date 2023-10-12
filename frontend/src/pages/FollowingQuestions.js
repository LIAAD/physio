import React from 'react'
import { useState } from 'react'
import { Container, Row, Navbar, Col, Image, Form, InputGroup, Spinner } from 'react-bootstrap'
import AlertError from './AlertError';
import logo from '../assets/images/logo.png'
import github from '../assets/images/github.png'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCircleRight } from '@fortawesome/free-solid-svg-icons'
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { ExtendedMessage, ShortMessage } from './Message.js'
import { processResponse, sendQuery } from './utils.js'


const MessageBlock = (props) => {

  const [question, setQuestion] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()

    props.setSpinning(true)

    sendQuery(question, props.messages).then(res => {

      props.setError('')

      const [answer, exercises, medications] = processResponse(res['result'])

      props.setMessages((messages) => [...messages, { 'question': question, 'answer': answer, 'exercises': exercises, 'medications': medications }])

    }).catch(err => {
      props.setError(err)
      props.setMessages((messages) => [...messages, { 'question': question, 'answer': {}, 'exercises': [], 'medications': [] }])
    }).finally(() => {
      setQuestion('')
      props.setSpinning(false)
    })

  }

  return (
    <Row className="w-100">
      <Col id="message-container" xs={9} className="mx-auto h-100">
        {props.messages.map((message, index) => {
          if (index === props.messages.length - 1 && message.answer.urls != null)
            return <ExtendedMessage key={index} message={message} />
          else
            return <ShortMessage key={index} message={message} />
        })}
        <Row className="mt-auto">
          <Col xs={10} md={5} className='mx-auto'>
            {props.spinning == false && <Form className='my-4' onSubmit={handleSubmit}>
              <InputGroup id='input-group-blue'>
                <Form.Control id='search-input-blue' className='text-center'
                  placeholder="Ask me anything!"
                  name='search'
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                />
                <InputGroup.Text id='group-text-blue'>
                  <FontAwesomeIcon icon={faCircleRight} id='search-icon-blue' />
                </InputGroup.Text>
              </InputGroup>
            </Form>
            }
          </Col>
        </Row>
      </Col>
    </Row>
  )
}

const FollowingQuestions = (props) => {

  const [spinning, setSpinning] = useState(false)

  const handleClickHomepage = (e) => {
    e.preventDefault()

    props.setMessages([])
  }


  return (
    <Container fluid>
      <Navbar id="navbar" className='mb-5'>
        <Row className="py-2">
          <Col xs={2} lg={1} className="text-center ms-3">
            <Image src={logo} fluid onClick={handleClickHomepage} />
          </Col>
          <Col className="mt-auto ms-3">
            <h2>AI Powered Physiotherapist</h2>
          </Col>
          <Col xs={1} className='ms-auto my-auto text-end'>
            <a href='https://github.com/liaad/physio'><Image id="github" fluid src={github} /></a>
          </Col>
        </Row>
      </Navbar>
      {spinning == false && <MessageBlock {...props} spinning={spinning} setSpinning={setSpinning} />}
      {spinning == true &&
        <Row className="justify-content-center">
          <Col xs="1">
            <h1>Waiting</h1>
          </Col>
          <Col xs="1" className="my-auto">
            <Spinner animation="border" variant="primary" size='xl' />
          </Col>
        </Row>
      }
    </Container>
  )
}

export default FollowingQuestions