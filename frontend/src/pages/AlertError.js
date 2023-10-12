import React from 'react'
import { Alert } from 'react-bootstrap'

function AlertError(props) {
    return (
        <Alert variant="danger">
            {props.message}
        </Alert>
    )
}

export default AlertError